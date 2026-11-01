"""
Offline MITRE ATT&CK technique lookup.

Download the Enterprise ATT&CK STIX bundle once:
    https://github.com/mitre-attack/attack-stix-data -> enterprise-attack/enterprise-attack.json
and save it as data/enterprise-attack.json (or set ATTACK_JSON).
"""
import json
import os
from functools import lru_cache

ATTACK_JSON = os.environ.get("ATTACK_JSON", "data/enterprise-attack.json")


@lru_cache(maxsize=1)
def _techniques():
    if not os.path.exists(ATTACK_JSON):
        return {}
    with open(ATTACK_JSON, encoding="utf-8") as f:
        bundle = json.load(f)
    techniques = {}
    for obj in bundle.get("objects", []):
        if obj.get("type") != "attack-pattern" or obj.get("revoked"):
            continue
        ref = next((r for r in obj.get("external_references", [])
                    if r.get("source_name") == "mitre-attack"), None)
        if not ref:
            continue
        techniques[ref["external_id"]] = {
            "id": ref["external_id"],
            "name": obj.get("name"),
            "tactics": [p["phase_name"] for p in obj.get("kill_chain_phases", [])],
            "description": (obj.get("description") or "").split("\n")[0],
            "url": ref.get("url"),
        }
    return techniques


def get_attack_info(ttp_id):
    """Return name, tactics, description and URL for an ATT&CK ID such as T1595, or None."""
    if not ttp_id or ttp_id == "Unknown":
        return None
    return _techniques().get(ttp_id)


if __name__ == "__main__":
    import sys
    print(get_attack_info(sys.argv[1] if len(sys.argv) > 1 else "T1595"))
