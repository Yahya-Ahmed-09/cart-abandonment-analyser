# dashboard/pages/3_🛒_Abandoned_Carts.py
# Clean version: shows abandoned carts, their products, and clear reasons why.

import streamlit as st
import pandas as pd
from utils import (
    load_model_data,
    compute_predictions,
    load_model_and_features,
    get_shap_explainer,
    load_cart_item_identity,
    load_all_cart_events,
    explain_feature_plain_language,
    FEATURE_ICONS,
)

st.set_page_config(page_title="Abandoned Carts", page_icon="🛒", layout="wide")

# ====================================================================
# LOAD DATA
# ====================================================================
model, feature_columns = load_model_and_features()
df = load_model_data()
df_preds = compute_predictions(df, feature_columns)

item_identity = load_cart_item_identity()
df_preds = df_preds.merge(item_identity, on="reconstructed_session_id", how="left")

abandoned = df_preds[df_preds["predicted_label"] == 1].sort_values(
    "abandonment_probability", ascending=False
)

# ====================================================================
# HEADER + SUMMARY METRICS
# ====================================================================
st.title("🛒 Abandoned Carts")
st.caption("Carts the model predicts the customer will NOT complete.")

m1, m2, m3 = st.columns(3)
m1.metric("Total Abandoned Carts", f"{len(abandoned):,}")
m2.metric("Average Cart Price", f"${abandoned['avg_price_before_cart'].mean():.2f}")
m3.metric("Average Abandonment Chance", f"{abandoned['abandonment_probability'].mean():.1%}")

st.divider()

# ====================================================================
# TABLE OF ABANDONED CARTS
# ====================================================================
st.subheader("All Abandoned Carts")

table_view = abandoned[
    ["reconstructed_session_id", "category_code", "brand", "avg_price_before_cart", "abandonment_probability"]
].head(50).copy()

table_view["abandonment_probability"] = (table_view["abandonment_probability"] * 100).round(1)

st.dataframe(
    table_view.rename(columns={
        "reconstructed_session_id": "Session ID",
        "category_code": "Category",
        "brand": "Brand",
        "avg_price_before_cart": "Price ($)",
        "abandonment_probability": "Abandonment Chance (%)",
    }),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ====================================================================
# INSPECT ONE SPECIFIC CART
# ====================================================================
st.subheader("🔍 Inspect a Specific Cart")

selected_session = st.selectbox("Choose a Session ID", abandoned["reconstructed_session_id"].tolist())
session = df_preds[df_preds["reconstructed_session_id"] == selected_session].iloc[0]
probability = session["abandonment_probability"]

# --- Probability shown clearly, with color ---
st.markdown("#### Abandonment Chance")
risk_color = "🔴" if probability >= 0.7 else "🟠" if probability >= 0.4 else "🟢"
st.markdown(f"### {risk_color} {probability:.1%}")
st.progress(probability)

st.markdown("---")

# --- ALL products added to cart in this session ---
st.markdown("#### 🛍️ Products Added to Cart in This Session")

all_cart_events = load_all_cart_events()
session_products = all_cart_events[
    all_cart_events["reconstructed_session_id"] == selected_session
]

st.dataframe(
    session_products[["product_id", "category_code", "brand", "price"]].rename(columns={
        "product_id": "Product ID",
        "category_code": "Category",
        "brand": "Brand",
        "price": "Price ($)",
    }),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# --- WHY this cart was predicted as abandoned ---
st.markdown("#### 💡 Why Was This Cart Predicted as Abandoned?")
st.caption(
    "These reasons come from the model's decision process. Given the model's "
    "overall accuracy (~59%), treat these as helpful signals, not certainties."
)

explainer = get_shap_explainer()
X_row = session[feature_columns].to_frame().T
shap_values = explainer.shap_values(X_row)[0]

shap_series = pd.Series(shap_values, index=feature_columns)
top_reasons = shap_series[shap_series > 0].sort_values(ascending=False).head(3)

context = {
    "product_id": session["product_id"],
    "category_code": session["category_code"],
    "brand": session["brand"],
}

if len(top_reasons) == 0:
    st.info("No single factor stood out strongly for this cart.")
else:
    for rank, (feature_name, shap_value) in enumerate(top_reasons.items(), start=1):
        icon = FEATURE_ICONS.get(feature_name, "▪️")
        reason_text = explain_feature_plain_language(
            feature_name, session[feature_name], shap_value, context
        )
        st.markdown(f"**{rank}. {icon} {reason_text}**")