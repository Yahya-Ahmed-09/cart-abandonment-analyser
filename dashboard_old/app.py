# dashboard/app.py
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Cart Abandonment Dashboard", layout="wide")

# ------------------------------------------------------------------
# Load model, feature list, and data (cached so it only loads once)
# ------------------------------------------------------------------
@st.cache_resource
def load_model_and_features():
    model = joblib.load("../models/final_model.pkl")
    feature_columns = joblib.load("../models/feature_columns.pkl")
    return model, feature_columns

@st.cache_data
def load_data():
    df = pd.read_csv("../data/model_ready_cart_sessions_final.csv")
    return df

model, feature_columns = load_model_and_features()
df = load_data()

# ------------------------------------------------------------------
# Compute predictions for every session (done once, cached)
# ------------------------------------------------------------------
@st.cache_data
def compute_predictions(_df, _feature_columns):
    X = _df[_feature_columns]
    probabilities = model.predict_proba(X)[:, 1]
    result = _df.copy()
    result["abandonment_probability"] = probabilities
    result["predicted_label"] = (probabilities >= 0.5).astype(int)
    return result

df_with_preds = compute_predictions(df, feature_columns)

# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.header("Filters")
min_prob, max_prob = st.sidebar.slider(
    "Abandonment probability range", 0.0, 1.0, (0.0, 1.0), 0.05
)
show_only = st.sidebar.selectbox(
    "Show", ["All sessions", "Predicted Abandoned", "Predicted Completed"]
)

filtered = df_with_preds[
    (df_with_preds["abandonment_probability"] >= min_prob)
    & (df_with_preds["abandonment_probability"] <= max_prob)
]
if show_only == "Predicted Abandoned":
    filtered = filtered[filtered["predicted_label"] == 1]
elif show_only == "Predicted Completed":
    filtered = filtered[filtered["predicted_label"] == 0]

# ------------------------------------------------------------------
# Main page
# ------------------------------------------------------------------
st.title("Cart Abandonment Prediction Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Sessions", len(df_with_preds))
col2.metric("Predicted Abandoned", int((df_with_preds["predicted_label"] == 1).sum()))
col3.metric("Predicted Completed", int((df_with_preds["predicted_label"] == 0).sum()))

st.subheader(f"Sessions ({len(filtered)} shown)")
st.dataframe(
    filtered[["reconstructed_session_id", "abandonment_probability", "predicted_label"]]
    .sort_values("abandonment_probability", ascending=False)
    .reset_index(drop=True),
    use_container_width=True,
)




# ------------------------------------------------------------------
# Session detail view with SHAP explanation
# ------------------------------------------------------------------
import shap
import matplotlib.pyplot as plt
import numpy as np

st.divider()
st.header("Session Detail & Explanation")

session_ids = filtered["reconstructed_session_id"].tolist()
if len(session_ids) == 0:
    st.warning("No sessions match the current filters.")
else:
    selected_session = st.selectbox("Select a session to explain", session_ids)

    session_row = df_with_preds[
        df_with_preds["reconstructed_session_id"] == selected_session
    ].iloc[0]

    st.metric(
        "Predicted Abandonment Probability",
        f"{session_row['abandonment_probability']:.1%}",
    )

    # Compute SHAP values for this single session (fast, tree-based model)
    explainer = shap.TreeExplainer(model)
    X_row = session_row[feature_columns].to_frame().T
    shap_values_row = explainer.shap_values(X_row)[0]

    case_shap = pd.Series(shap_values_row, index=feature_columns).sort_values(
        key=abs, ascending=False
    )

    st.subheader("Top factors contributing to this prediction")
    st.caption(
        "These show what contributed to the model's prediction, not what "
        "caused the customer's decision. Given the model's overall accuracy "
        "(~59%), treat these as directional signals, not confident conclusions."
    )

    top_features = case_shap.head(8)
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#d62728" if v > 0 else "#1f77b4" for v in top_features.values]
    ax.barh(top_features.index[::-1], top_features.values[::-1], color=colors[::-1])
    ax.set_xlabel("SHAP value (impact on prediction)")
    ax.axvline(0, color="black", linewidth=0.8)
    st.pyplot(fig)

    with st.expander("See raw feature values for this session"):
        st.dataframe(session_row[feature_columns].to_frame(name="value"))

# ------------------------------------------------------------------
# Overall model performance summary
# ------------------------------------------------------------------
st.divider()
st.header("Model Performance Overview")

perf_col1, perf_col2, perf_col3 = st.columns(3)
perf_col1.metric("Accuracy", "59.11%")
perf_col2.metric("ROC-AUC", "62.04%")
perf_col3.metric("Recall", "46.65%")

st.caption(
    "This model's accuracy is limited by the available data (behavioral "
    "clickstream only, no checkout/payment signals). See project "
    "documentation for the full root-cause analysis."
)

@st.cache_data
def compute_global_shap(_df_sample, _feature_columns):
    explainer = shap.TreeExplainer(model)
    X_sample = _df_sample[_feature_columns]
    shap_vals = explainer.shap_values(X_sample)
    importance = pd.Series(
        np.abs(shap_vals).mean(axis=0), index=_feature_columns
    ).sort_values(ascending=False)
    return importance

sample_for_global = df_with_preds.sample(
    n=min(1000, len(df_with_preds)), random_state=42
)
global_importance = compute_global_shap(sample_for_global, feature_columns)

st.subheader("Global Feature Importance")
fig2, ax2 = plt.subplots(figsize=(7, 5))
top_global = global_importance.head(10)
ax2.barh(top_global.index[::-1], top_global.values[::-1], color="#2ca02c")
ax2.set_xlabel("Mean |SHAP value|")
st.pyplot(fig2)