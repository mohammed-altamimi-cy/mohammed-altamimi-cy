"""
Flask API that scores network-flow records with the stacking ensemble.

    python src/api.py            # serves on http://127.0.0.1:5000

POST /predict  with one JSON record or a list of records (UNSW-NB15 feature names).
Missing features are filled with 0. An optional "attack_ttp" field is passed through
and enriched with MITRE ATT&CK context when data/enterprise-attack.json is present.
"""
import os

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

from attack_lookup import get_attack_info

MODEL_DIR = os.environ.get("MODEL_DIR", "models")
THRESHOLD = float(os.environ.get("THREAT_THRESHOLD", 0.5))

rf = joblib.load(os.path.join(MODEL_DIR, "random_forest.joblib"))
xgb = joblib.load(os.path.join(MODEL_DIR, "xgboost.joblib"))
tabnet = joblib.load(os.path.join(MODEL_DIR, "tabnet.joblib"))
meta = joblib.load(os.path.join(MODEL_DIR, "meta_model.joblib"))
FEATURES = joblib.load(os.path.join(MODEL_DIR, "feature_columns.joblib"))

app = Flask(__name__)


def risk_level(score):
    if score > 0.9:
        return "High"
    if score >= 0.7:
        return "Medium"
    return "Low"


def score(records):
    df = pd.DataFrame(records)
    X = df.reindex(columns=FEATURES, fill_value=0).astype(float)
    base = np.column_stack([
        rf.predict_proba(X)[:, 1],
        xgb.predict_proba(X)[:, 1],
        tabnet.predict_proba(X.values)[:, 1],
    ])
    return meta.predict_proba(base)[:, 1]


@app.route("/health")
def health():
    return jsonify({"status": "ok", "features": len(FEATURES)})


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be JSON"}), 400
    records = payload if isinstance(payload, list) else [payload]

    try:
        scores = score(records)
    except Exception as exc:  # bad types, empty list, etc.
        return jsonify({"error": str(exc)}), 400

    results = []
    for record, s in zip(records, scores):
        ttp = record.get("attack_ttp")
        results.append({
            "threat_score": round(float(s), 4),
            "predicted_label": int(s >= THRESHOLD),
            "risk": risk_level(s),
            "attack_ttp": ttp,
            "attack_context": get_attack_info(ttp) if ttp else None,
        })
    return jsonify(results if isinstance(payload, list) else results[0])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
