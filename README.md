# Self-Evolving Security Defense System

An adaptive intrusion detection system that analyzes log-based attack behavior,
classifies threats in real time, and continuously learns recurring attack patterns
to improve future detection accuracy.

---

## 🚨 Problem Statement
Traditional intrusion detection systems rely on static rules or fixed datasets.
They fail to adapt when new or unknown attack patterns appear.

This project addresses that limitation by introducing a **self-evolving security engine**
that updates its threat memory as new attacks are detected.

---

## ⚙️ Key Features
- Threat classification: **NORMAL / SUSPICIOUS / ATTACK**
- Real-time log monitoring and visualization
- Attack pattern memory learning
- Severity-based analytics dashboard
- Continuous evaluation before and after learning

---

## 🧠 System Workflow
1. System logs are ingested continuously
2. Features are extracted from log data
3. ML model classifies traffic behavior
4. Unknown attacks are stored in threat memory
5. Model performance improves over time
6. Dashboard visualizes live and historical metrics

---

## 🛠 Tech Stack
- Python
- Machine Learning (Scikit-learn)
- Pandas & NumPy
- Streamlit (Dashboard)
- Matplotlib (Visualizations)

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
python main.py
python realtime_engine.py
streamlit run dashboards/app.py
