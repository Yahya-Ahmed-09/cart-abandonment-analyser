# dashboard/Home.py
# Run with: streamlit run Home.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_model_data, load_event_data, compute_predictions, load_model_and_features, FINAL_METRICS

st.set_page_config(page_title="Cart Abandonment Dashboard", page_icon="🛒", layout="wide")

model, feature_columns = load_model_and_features()
df = load_model_data()
df_preds = compute_predictions(df, feature_columns)
events = load_event_data()

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.title("🛒 Cart Abandonment Analysis Dashboard")
st.caption("Understand and predict cart abandonment using real customer behavior data.")

# ------------------------------------------------------------------
# KPI cards
# ------------------------------------------------------------------
total_sessions = events["reconstructed_session_id"].nunique()
cart_sessions = len(df_preds)
completed = int((df_preds["is_abandoned"] == 0).sum())
abandoned = int((df_preds["is_abandoned"] == 1).sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sessions", f"{total_sessions:,}")
col2.metric("Cart Sessions", f"{cart_sessions:,}")
col3.metric("Completed Carts", f"{completed:,}", f"{completed/cart_sessions:.1%}")
col4.metric("Abandoned Carts", f"{abandoned:,}", f"{abandoned/cart_sessions:.1%}", delta_color="inverse")

st.divider()

# ------------------------------------------------------------------
# Cart Outcomes donut + Event Distribution + Model Performance
# ------------------------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Cart Outcomes")
    fig, ax = plt.subplots()
    ax.pie(
        [completed, abandoned],
        labels=["Completed", "Abandoned"],
        autopct="%1.1f%%",
        colors=["#1f77b4", "#d62728"],
        wedgeprops=dict(width=0.4),
    )
    st.pyplot(fig)

with c2:
    st.subheader("Event Distribution (All Events)")
    event_counts = events["event_type"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.bar(event_counts.index, event_counts.values, color=["#1f77b4", "#2ca02c", "#d62728"])
    for i, v in enumerate(event_counts.values):
        ax2.text(i, v, f"{v:,}", ha="center", va="bottom")
    st.pyplot(fig2)

with c3:
    st.subheader("Model Performance (Gradient Boosting - Final)")
    for label, key in [
        ("Accuracy", "accuracy"), ("Precision", "precision"), ("Recall", "recall"),
        ("F1 Score", "f1"), ("ROC-AUC", "roc_auc"),
    ]:
        st.progress(FINAL_METRICS[key], text=f"{label}: {FINAL_METRICS[key]:.2%}")

st.divider()

# ------------------------------------------------------------------
# Recent abandoned carts table
# ------------------------------------------------------------------
st.subheader("Recent Abandoned Carts")
recent_abandoned = (
    df_preds[df_preds["predicted_label"] == 1]
    .sort_values("abandonment_probability", ascending=False)
    .head(10)
)
st.dataframe(
    recent_abandoned[
        ["reconstructed_session_id", "abandonment_probability", "avg_price_before_cart", "days_since_last_purchase"]
    ].rename(columns={
        "reconstructed_session_id": "Session ID",
        "abandonment_probability": "Predicted Prob.",
        "avg_price_before_cart": "Avg Price",
        "days_since_last_purchase": "Days Since Last Purchase",
    }),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Model accuracy is limited by available data (behavioral clickstream only, "
    "no checkout/payment signals). See project documentation for full root-cause analysis."
)