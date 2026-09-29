# dashboard/utils.py

import streamlit as st
import pandas as pd
import joblib
import shap

MODEL_PATH = "../models/final_model.pkl"
FEATURES_PATH = "../models/feature_columns.pkl"
MODEL_DATA_PATH = "../data/model_ready_cart_sessions_final.csv"
EVENTS_PATH = "../data/reconstructed_events_v3.csv"

# Final, CORRECTED model metrics (do not use old V3 numbers anywhere)
FINAL_METRICS = {
    "accuracy": 0.5911,
    "precision": 0.5624,
    "recall": 0.4665,
    "f1": 0.5010,
    "roc_auc": 0.6204,
}

# Final confusion matrix: [[True Negative, False Positive], [False Negative, True Positive]]
FINAL_CONFUSION_MATRIX = [[3242, 1419], [2086, 1824]]

# Performance across each stage of the project (for the journey chart)
PERFORMANCE_JOURNEY = {
    "stage": ["Original (Buggy Target)", "Fixed Target", "+ New Features", "Final (Tuned)"],
    "accuracy": [0.5869, 0.5837, 0.5886, 0.5911],
    "roc_auc": [0.6132, 0.6080, 0.6187, 0.6204],
}

@st.cache_resource
def load_model_and_features():
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
    return model, feature_columns


@st.cache_data
def load_model_data():
    return pd.read_csv(MODEL_DATA_PATH)


@st.cache_data
def load_event_data():
    events = pd.read_csv(EVENTS_PATH)
    events["event_time"] = pd.to_datetime(events["event_time"], utc=True)
    return events


@st.cache_data
def compute_predictions(_df, feature_columns):
    model, _ = load_model_and_features()
    X = _df[feature_columns]
    probabilities = model.predict_proba(X)[:, 1]
    result = _df.copy()
    result["abandonment_probability"] = probabilities
    result["predicted_label"] = (probabilities >= 0.5).astype(int)
    return result


@st.cache_resource
def get_shap_explainer():
    model, _ = load_model_and_features()
    return shap.TreeExplainer(model)


@st.cache_data
def load_cart_item_identity():
    """Get the exact product/category/brand that was added to cart in each session."""
    events = load_event_data()
    first_cart_events = (
        events[events["event_type"] == "cart"]
        .sort_values("event_time")
        .drop_duplicates(subset="reconstructed_session_id", keep="first")
        [["reconstructed_session_id", "product_id", "category_code", "brand", "price"]]
        .rename(columns={"price": "cart_item_price"})
    )
    return first_cart_events


def explain_feature_plain_language(feature, value, shap_value, context=None):
    """Convert a technical feature + SHAP value into a plain-language reason.
    context is a dict with product_id, category_code, brand for this session."""
    context = context or {}
    category = context.get("category_code", "unknown")
    brand = context.get("brand", "unknown")
    product_id = context.get("product_id", "unknown")

    if feature == "days_since_last_purchase":
        if value == -1:
            return "This is a new or first-time customer with no purchase history"
        return f"It has been {value:.0f} days since this customer's last purchase"

    if feature == "avg_price_before_cart":
        direction = "expensive" if shap_value > 0 else "inexpensive"
        return f"The item (brand: {brand}, category: {category}) is relatively {direction} at ${value:.2f}"

    if feature == "category_historical_abandon_rate":
        direction = "high" if shap_value > 0 else "low"
        return f"The category '{category}' has a historically {direction} abandonment rate ({value:.1%})"

    if feature == "product_prior_cart_count":
        popularity = "very popular" if value > 100 else "less common"
        return f"Product {product_id} (brand: {brand}) is a {popularity} item, cart-added {value:.0f} times before"

    if feature == "view_to_cart_minutes":
        if value < 1:
            return f"The {brand} item in '{category}' was added to cart almost instantly after viewing — an impulsive add"
        return f"The customer spent about {value:.1f} minutes viewing the {brand} item before adding to cart"

    if feature == "previous_cart_session_count":
        tendency = "more likely" if shap_value > 0 else "less likely"
        return f"This customer has added items to cart {value:.0f} times before, making abandonment {tendency} based on their history"

    if feature == "price_range_before_cart":
        direction = "wide" if shap_value > 0 else "narrow"
        return f"There was a {direction} price range (${value:.2f}) among items viewed in category '{category}'"

    if feature == "duration_before_cart":
        return f"The customer browsed for {value:.1f} minutes before adding this {brand} item to cart"

    if feature == "cart_hour":
        hour = int(value)
        if 5 <= hour < 12:
            time_label = "morning"
        elif 12 <= hour < 17:
            time_label = "afternoon"
        elif 17 <= hour < 21:
            time_label = "evening"
        else:
            time_label = "late night"
        tendency = "higher" if shap_value > 0 else "lower"
        return f"Carts started in the {time_label} (around {hour}:00) tend to show a {tendency} abandonment rate in this data"

    if feature == "previous_purchase_count":
        return f"This customer has completed {value:.0f} purchases in the past"

    if feature == "user_purchase_rate":
        return f"This customer historically completes {value:.0%} of their cart sessions"

    return f"{feature.replace('_', ' ').title()}: {value:.2f}"


# Add this function to dashboard/utils.py

@st.cache_data
def load_session_user_mapping():
    """Map each reconstructed_session_id back to its user_id."""
    events = load_event_data()
    mapping = (
        events[["reconstructed_session_id", "user_id"]]
        .drop_duplicates(subset="reconstructed_session_id")
    )
    return mapping


# Add this to dashboard/utils.py

@st.cache_data
def load_all_cart_events():
    """Get every cart-add event (not just the first) with product details."""
    events = load_event_data()
    cart_events = events[events["event_type"] == "cart"][
        ["reconstructed_session_id", "event_time", "product_id", "category_code", "brand", "price"]
    ].sort_values("event_time")
    return cart_events


# Icons to make each reason visually clear at a glance
FEATURE_ICONS = {
    "days_since_last_purchase": "🕐",
    "avg_price_before_cart": "💰",
    "category_historical_abandon_rate": "📊",
    "product_prior_cart_count": "🔥",
    "view_to_cart_minutes": "⚡",
    "previous_cart_session_count": "🛒",
    "price_range_before_cart": "💵",
    "duration_before_cart": "⏱️",
    "cart_hour": "🕐",
    "previous_purchase_count": "✅",
    "user_purchase_rate": "📈",
}