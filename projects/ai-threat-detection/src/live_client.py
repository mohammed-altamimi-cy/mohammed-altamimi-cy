"""
Replay sample flows against the running API, one per second, like a live log feed.

    python src/live_client.py --sample models/demo_sample.csv --limit 25
"""
import argparse
import time
from datetime import datetime

import pandas as pd
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", default="models/demo_sample.csv")
    parser.add_argument("--api", default="http://127.0.0.1:5000/predict")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()

    df = pd.read_csv(args.sample).head(args.limit)
    print("Starting live threat simulation...")
    for i, row in df.iterrows():
        record = row.drop(labels=["label"], errors="ignore").to_dict()
        result = requests.post(args.api, json=record, timeout=10).json()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "THREAT" if result["predicted_label"] else "safe  "
        truth = "attack" if row.get("label", 0) == 1 else "normal"
        print(f"{ts} | flow #{i + 1:>3} | {status} | score {result['threat_score']:.4f} "
              f"| risk {result['risk']:<6} | ground truth: {truth}")
        time.sleep(args.delay)


if __name__ == "__main__":
    main()
