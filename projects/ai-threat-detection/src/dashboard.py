"""
Streamlit SOC dashboard: upload flow logs (CSV) or replay the demo sample,
score them through the API and review threats by risk level.

    streamlit run src/dashboard.py
"""
import pandas as pd
import requests
import streamlit as st

API = "http://127.0.0.1:5000/predict"

st.set_page_config(layout="wide", page_title="AI Threat Detection Dashboard")
st.title("AI Threat Detection Dashboard")
st.caption("Stacking ensemble (Random Forest + XGBoost + TabNet) scoring UNSW-NB15 network flows")

st.sidebar.header("Input")
uploaded = st.sidebar.file_uploader("Upload a CSV of network flows", type=["csv"])
use_demo = st.sidebar.checkbox("Use demo sample (models/demo_sample.csv)", value=uploaded is None)
min_score, max_score = st.sidebar.slider("Threat score range", 0.0, 1.0, (0.0, 1.0), 0.01)

if uploaded is not None:
    logs = pd.read_csv(uploaded)
elif use_demo:
    logs = pd.read_csv("models/demo_sample.csv")
else:
    st.info("Upload a CSV or enable the demo sample to start.")
    st.stop()

records = logs.drop(columns=["label"], errors="ignore").to_dict(orient="records")
try:
    results = pd.DataFrame(requests.post(API, json=records, timeout=60).json())
except requests.RequestException as exc:
    st.error(f"Could not reach the API at {API}. Start it with `python src/api.py`. ({exc})")
    st.stop()

results.insert(0, "flow", range(1, len(results) + 1))
if "label" in logs.columns:
    results["ground_truth"] = logs["label"].map({0: "normal", 1: "attack"}).values

view = results[(results.threat_score >= min_score) & (results.threat_score <= max_score)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Flows analysed", len(results))
c2.metric("Threats", int(results.predicted_label.sum()))
c3.metric("High risk", int((results.risk == "High").sum()))
c4.metric("Medium risk", int((results.risk == "Medium").sum()))

left, right = st.columns([2, 1])
with left:
    st.subheader("Scored flows")
    st.dataframe(view.drop(columns=["attack_context"], errors="ignore"), height=480, use_container_width=True)
with right:
    st.subheader("Risk distribution")
    st.bar_chart(results.risk.value_counts())
    st.subheader("Threat score by flow")
    st.line_chart(results.set_index("flow")["threat_score"])
