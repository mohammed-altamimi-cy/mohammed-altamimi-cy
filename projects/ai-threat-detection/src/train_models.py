"""
Train the stacking ensemble (Random Forest + XGBoost + TabNet -> Logistic Regression)
on the preprocessed UNSW-NB15 dataset.

Usage:
    python src/train_models.py --data data/UNSW-NB15-processed.csv

Outputs (in ./models):
    random_forest.joblib, xgboost.joblib, tabnet.joblib, meta_model.joblib,
    feature_columns.joblib, metrics.json
"""
import argparse
import json
import os

import joblib
import numpy as np
import pandas as pd
from pytorch_tabnet.tab_model import TabNetClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# Columns that must never be used as features:
#  - id: row identifier
#  - attack_cat / attack_ttp: derived from the ground truth, would leak the label
NON_FEATURES = ["id", "attack_cat", "attack_ttp", "label"]
SEED = 42


def load_dataset(path):
    df = pd.read_csv(path)
    # The processed file stores the label standardised (normal < 0, attack > 0)
    df["label"] = (df["label"] > 0).astype(int)
    df = df.drop_duplicates()
    X = df.drop(columns=[c for c in NON_FEATURES if c in df.columns])
    y = df["label"].to_numpy()
    return X, y


def evaluate(name, y_true, proba, threshold=0.5):
    pred = (proba >= threshold).astype(int)
    return {
        "model": name,
        "accuracy": round(accuracy_score(y_true, pred), 4),
        "precision": round(precision_score(y_true, pred), 4),
        "recall": round(recall_score(y_true, pred), 4),
        "f1": round(f1_score(y_true, pred), 4),
        "roc_auc": round(roc_auc_score(y_true, proba), 4),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/UNSW-NB15-processed.csv")
    parser.add_argument("--out", default="models")
    parser.add_argument("--tabnet-epochs", type=int, default=10)
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)

    X, y = load_dataset(args.data)
    print(f"Loaded {len(X):,} rows, {X.shape[1]} features, {y.mean():.1%} malicious")

    # 60% base-model training / 20% meta-model training / 20% held-out test.
    # The meta-model is trained on predictions for data the base models never saw,
    # and every reported metric comes from the untouched test split.
    X_tmp, X_test, y_tmp, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    X_train, X_meta, y_train, y_meta = train_test_split(X_tmp, y_tmp, test_size=0.25, stratify=y_tmp, random_state=SEED)

    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1)
    rf.fit(X_train, y_train)

    print("Training XGBoost...")
    xgb = XGBClassifier(eval_metric="logloss", random_state=SEED)
    xgb.fit(X_train, y_train)

    print("Training TabNet...")
    tabnet = TabNetClassifier(seed=SEED, verbose=0)
    tabnet.fit(
        X_train.values, y_train,
        eval_set=[(X_meta.values, y_meta)],
        max_epochs=args.tabnet_epochs, patience=5,
        batch_size=1024, virtual_batch_size=128,
    )

    def base_probs(data):
        return np.column_stack([
            rf.predict_proba(data)[:, 1],
            xgb.predict_proba(data)[:, 1],
            tabnet.predict_proba(data.values)[:, 1],
        ])

    print("Training meta-model (Logistic Regression)...")
    meta = LogisticRegression()
    meta.fit(base_probs(X_meta), y_meta)

    test_base = base_probs(X_test)
    results = [
        evaluate("Random Forest", y_test, test_base[:, 0]),
        evaluate("XGBoost", y_test, test_base[:, 1]),
        evaluate("TabNet", y_test, test_base[:, 2]),
        evaluate("Stacking Ensemble", y_test, meta.predict_proba(test_base)[:, 1]),
    ]
    print(pd.DataFrame(results).to_string(index=False))

    joblib.dump(rf, os.path.join(args.out, "random_forest.joblib"))
    joblib.dump(xgb, os.path.join(args.out, "xgboost.joblib"))
    joblib.dump(tabnet, os.path.join(args.out, "tabnet.joblib"))
    joblib.dump(meta, os.path.join(args.out, "meta_model.joblib"))
    joblib.dump(X.columns.tolist(), os.path.join(args.out, "feature_columns.joblib"))
    with open(os.path.join(args.out, "metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    # Small sample for the live demo / dashboard (features + ground truth)
    sample = X_test.head(500).copy()
    sample["label"] = y_test[:500]
    sample.to_csv(os.path.join(args.out, "demo_sample.csv"), index=False)
    print(f"Saved models and metrics to {args.out}/")


if __name__ == "__main__":
    main()
