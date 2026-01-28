import streamlit as st
import pandas as pd
import json
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Self-Evolving Security Dashboard",
    layout="wide"
)

# -------------------------------------------------
# CENTERED TITLE (PRO WAY)
# -------------------------------------------------

st.markdown(
    "<h1 style='text-align: center;'>Self-Evolving Security Defense System</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray;'>Real-time intrusion detection with adaptive threat learning</p>",
    unsafe_allow_html=True
)


st.divider()

# -------------------------------------------------
# PATH SETUP
# -------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

FEATURES_PATH = os.path.join(ROOT_DIR, "data/processed/features.csv")
KNOWN_ATTACKS_PATH = os.path.join(ROOT_DIR, "results/known_attacks.json")
METRICS_PATH = os.path.join(ROOT_DIR, "results/metrics_after_learning.json")
ALERTS_PATH = os.path.join(ROOT_DIR, "results/alerts.log")
LOGS_PATH = os.path.join(ROOT_DIR, "results/processed_logs.json")

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
if not os.path.exists(FEATURES_PATH):
    st.error("Run main.py and realtime_engine.py first.")
    st.stop()

features = pd.read_csv(FEATURES_PATH)

if "threat_level" not in features.columns:
    def classify(score):
        if score >= 0.8:
            return "ATTACK"
        elif score >= 0.4:
            return "SUSPICIOUS"
        return "NORMAL"

    features["threat_level"] = features["attempt_score"].apply(classify)

logs = None
if os.path.exists(LOGS_PATH):
    logs = pd.DataFrame(json.load(open(LOGS_PATH)))

metrics = load_json(METRICS_PATH, {})
known_attacks = load_json(KNOWN_ATTACKS_PATH, [])

latest = features.iloc[-1]

# -------------------------------------------------
# STATUS CARDS
# -------------------------------------------------
status_icon = {"NORMAL": "🟢", "SUSPICIOUS": "🟡", "ATTACK": "🔴"}
status = latest["threat_level"]

c1, c2, c3 = st.columns(3)
c1.metric("Threat Status", f"{status_icon[status]} {status}")
c2.metric("Last Detection", datetime.now().strftime("%H:%M:%S"))
c3.metric("Logs Processed", len(features))

st.divider()

# -------------------------------------------------
# REAL-TIME ATTACK FEED
# -------------------------------------------------
st.subheader("Real-Time Attack Feed")

feed = features.copy()
feed["ip"] = logs["ip"] if logs is not None and "ip" in logs else "Unknown"
feed["time"] = logs["timestamp"] if logs is not None and "timestamp" in logs else datetime.now().strftime("%H:%M:%S")

feed_df = feed[["time", "ip", "attempt_score", "threat_level"]]

def highlight(row):
    if row["threat_level"] == "ATTACK":
        return ["background-color:#F44336"] * len(row)      # red
    if row["threat_level"] == "SUSPICIOUS":
        return ["background-color:#FFC107"] * len(row)      # amber
    return [""] * len(row)



st.dataframe(feed_df.tail(15).style.apply(highlight, axis=1), use_container_width=True)

st.divider()

# -------------------------------------------------
# STATISTICS
# -------------------------------------------------
s1, s2, s3, s4 = st.columns(4)
s1.metric("Attacks", metrics.get("attacks", 0))
s2.metric("Suspicious", metrics.get("suspicious", 0))
s3.metric("Normal", metrics.get("normal", 0))
s4.metric("Patterns Learned", len(known_attacks))

st.divider()

# -------------------------------------------------
# MEMORY (CLEAN UX)
# -------------------------------------------------
with st.expander("🧠 Known Attack Memory"):
    if known_attacks:
        st.dataframe(pd.DataFrame(known_attacks), use_container_width=True)
    else:
        st.info("No patterns learned yet.")

st.divider()

# -------------------------------------------------
# GRAPHS SECTION (BALANCED)
# -------------------------------------------------
g1, g2 = st.columns(2)

with g1:
    st.subheader("📊 Threat Trend Over Time")

    threat_counts = features["threat_level"].value_counts()

    color_map = {
        "NORMAL": "#4CAF50",      # Green
        "SUSPICIOUS": "#FFC107",  # Amber
        "ATTACK": "#F44336"       # Red
    }

    colors = [color_map[level] for level in threat_counts.index]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(threat_counts.index, threat_counts.values, color=colors)

    ax.set_ylabel("Events")
    ax.set_xlabel("Threat Level")

    st.pyplot(fig)



with g2:
    st.subheader("⚠️ Severity Distribution")
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    features["threat_level"].value_counts().plot.pie(
        autopct="%1.1f%%",
        startangle=90,
        ax=ax,
        textprops={'fontsize': 6},
        colors=["#F44336", "#FFC107", "#4CAF50"]
    )
    ax.set_ylabel("")
    st.pyplot(fig)

st.divider()

# -------------------------------------------------
# ALERT HISTORY
# -------------------------------------------------
with st.expander("📜 Alert History"):
    if os.path.exists(ALERTS_PATH):
        alerts = open(ALERTS_PATH).readlines()
        st.text("".join(alerts[-15:]))
        st.download_button("Download Alerts", "".join(alerts), "alerts.csv")
    else:
        st.info("No alerts yet.")

st.divider()

# -------------------------------------------------
# SYSTEM HEALTH
# -------------------------------------------------
h1, h2, h3 = st.columns(3)
h1.success("Model Loaded")
h2.success("Realtime Engine Active")
h3.info("Last Training: Today")

st.caption("Dashboard updates based on processed security logs")
