import streamlit as st
import pandas as pd
import numpy as np
import joblib

from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Prediction — CartSense",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "synthetic_final_model.pkl"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .stApp {
        background-color: #F7F8FA;
    }

    .main {
        background-color: #F7F8FA;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: #111827 !important;
    }

    .stApp p {
        color: #6B7280;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] p {
        color: #9CA3AF !important;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 16px !important;
        padding: 18px !important;
    }

    [data-testid="stMetricLabel"] {
        color: #6B7280 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 18px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="select"] span {
        color: #111827 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return joblib.load(
        MODEL_PATH
    )


model = load_model()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## CartSense"
    )

    st.caption(
        "Cart Abandonment Intelligence"
    )

    st.markdown(
        "### Navigation"
    )

    st.page_link(
        "app.py",
        label="Overview",
        icon="🏠"
    )

    st.page_link(
        "pages/Cart_Analysis.py",
        label="Cart Analysis",
        icon="🛒"
    )

    st.page_link(
        "pages/Abandoned_Carts.py",
        label="Abandoned Carts",
        icon="⚠️"
    )

    st.page_link(
        "pages/Prediction.py",
        label="Prediction",
        icon="🎯"
    )

    st.page_link(
        "pages/Explainability.py",
        label="Explainability",
        icon="💡"
    )

    st.page_link(
        "pages/Model_Performance.py",
        label="Model Performance",
        icon="📊"
    )

    st.page_link(
        "pages/Data_Explorer.py",
        label="Data Explorer",
        icon="🔎"
    )

    st.divider()

    st.caption(
        "CART PREDICTION"
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.caption(
    "CART PREDICTION"
)

st.title(
    "Predict Cart Outcome"
)

st.write(
    "Enter the available cart and customer behavior "
    "information to estimate whether the cart is likely "
    "to be abandoned."
)

st.markdown("")


# ============================================================
# CART INFORMATION
# ============================================================

st.subheader(
    "Cart Information"
)

c1, c2 = st.columns(2)

with c1:

    cart_value = st.number_input(
        "Cart Value ($)",
        min_value=0.0,
        value=80.0,
        step=5.0
    )

with c2:

    avg_price_before_cart = st.number_input(
        "Average Product Price ($)",
        min_value=0.0,
        value=50.0,
        step=5.0
    )


# ============================================================
# CUSTOMER HISTORY
# ============================================================

st.markdown("")

st.subheader(
    "Customer History"
)

c1, c2, c3 = st.columns(3)

with c1:

    previous_purchase_count = st.number_input(
        "Previous Purchases",
        min_value=0,
        value=0,
        step=1
    )

with c2:

    user_purchase_rate = st.number_input(
        "Purchase Rate",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01,
        format="%.2f"
    )

with c3:

    days_since_last_purchase = st.number_input(
        "Days Since Last Purchase",
        min_value=-1,
        value=-1,
        step=1
    )


# ============================================================
# CHECKOUT BEHAVIOR
# ============================================================

st.markdown("")

st.subheader(
    "Checkout & Payment"
)

c1, c2 = st.columns(2)

with c1:

    checkout_page_visited = st.checkbox(
        "Checkout page visited",
        value=True
    )

    payment_attempted = st.checkbox(
        "Payment attempted",
        value=True
    )

    payment_failed = st.checkbox(
        "Payment failed",
        value=False
    )

    shipping_cost_shown = st.number_input(
        "Shipping Cost Shown ($)",
        min_value=0.0,
        value=5.0,
        step=1.0
    )


with c2:

    coupon_code_attempted = st.checkbox(
        "Coupon code attempted",
        value=False
    )

    coupon_applied_successfully = st.checkbox(
        "Coupon applied successfully",
        value=False
    )

    exit_intent_detected = st.checkbox(
        "Exit behavior detected",
        value=False
    )

    time_on_payment_page_seconds = st.number_input(
        "Time on Payment Page (seconds)",
        min_value=0.0,
        value=45.0,
        step=5.0
    )


# ============================================================
# DEVICE & TRAFFIC
# ============================================================

st.markdown("")

st.subheader(
    "Session Information"
)

c1, c2 = st.columns(2)

with c1:

    device_type = st.selectbox(
        "Device",
        [
            "mobile",
            "desktop",
            "tablet"
        ]
    )

with c2:

    traffic_source = st.selectbox(
        "Traffic Source",
        [
            "organic",
            "paid_ad",
            "social",
            "direct",
            "email"
        ]
    )


# ============================================================
# INPUT VALIDATION
# ============================================================

if not checkout_page_visited:

    payment_attempted = False
    payment_failed = False

if not payment_attempted:

    payment_failed = False

if not coupon_code_attempted:

    coupon_applied_successfully = False


# ============================================================
# BUILD MODEL INPUT
# ============================================================

input_data = pd.DataFrame(
    [
        {
            "cart_value":
                cart_value,

            "avg_price_before_cart":
                avg_price_before_cart,

            "previous_purchase_count":
                previous_purchase_count,

            "user_purchase_rate":
                user_purchase_rate,

            "days_since_last_purchase":
                days_since_last_purchase,

            "checkout_page_visited":
                int(checkout_page_visited),

            "payment_attempted":
                int(payment_attempted),

            "payment_failed":
                int(payment_failed),

            "shipping_cost_shown":
                shipping_cost_shown,

            "coupon_code_attempted":
                int(coupon_code_attempted),

            "coupon_applied_successfully":
                int(
                    coupon_applied_successfully
                ),

            "exit_intent_detected":
                int(exit_intent_detected),

            "time_on_payment_page_seconds":
                time_on_payment_page_seconds,

            "device_type":
                device_type,

            "traffic_source":
                traffic_source
        }
    ]
)


# ============================================================
# PREDICT BUTTON
# ============================================================

st.markdown("")

predict_button = st.button(
    "Predict Cart Outcome",
    type="primary",
    use_container_width=True
)


# ============================================================
# END PART 1
# ============================================================

if predict_button:

    prediction = model.predict(
        input_data
    )[0]

    probabilities = model.predict_proba(
        input_data
    )[0]

    abandonment_probability = (
        probabilities[1]
    )

    completion_probability = (
        probabilities[0]
    )

# ============================================================
# PREDICTION RESULT
# ============================================================

    st.markdown("")

    st.subheader(
        "Prediction Result"
    )


    # ========================================================
    # ABANDONED RESULT
    # ========================================================

    if prediction == 1:

        st.error(
            "This cart is likely to be abandoned."
        )

        r1, r2 = st.columns(2)

        with r1:

            st.metric(
                "Abandonment Probability",
                f"{abandonment_probability * 100:.1f}%"
            )

        with r2:

            st.metric(
                "Completion Probability",
                f"{completion_probability * 100:.1f}%"
            )


        st.markdown("")

        st.subheader(
            "What this means"
        )

        st.write(
            "Based on the information provided, this cart "
            "has a higher likelihood of being abandoned "
            "than completed."
        )


        # ----------------------------------------------------
        # SIMPLE RISK LEVEL
        # ----------------------------------------------------

        if abandonment_probability >= 0.80:

            risk_level = "High"

        elif abandonment_probability >= 0.60:

            risk_level = "Medium"

        else:

            risk_level = "Low"


        st.metric(
            "Abandonment Risk",
            risk_level
        )


        # ----------------------------------------------------
        # EXPLAINABILITY
        # ----------------------------------------------------

        st.markdown("")

        st.subheader(
            "Understand Why"
        )

        st.write(
            "You can review the behavioral factors associated "
            "with this prediction."
        )

        if st.button(
            "View Abandonment Reasons",
            type="primary",
            use_container_width=True
        ):

            # Save the prediction input so the next page
            # can use the same session information.

            st.session_state[
                "prediction_input"
            ] = input_data.copy()

            st.session_state[
                "prediction_result"
            ] = int(prediction)

            st.session_state[
                "abandonment_probability"
            ] = float(
                abandonment_probability
            )

            st.session_state[
                "completion_probability"
            ] = float(
                completion_probability
            )

            st.switch_page(
                "pages/Explainability.py"
            )


    # ========================================================
    # COMPLETED RESULT
    # ========================================================

    else:

        st.success(
            "This cart is likely to be completed."
        )

        r1, r2 = st.columns(2)

        with r1:

            st.metric(
                "Completion Probability",
                f"{completion_probability * 100:.1f}%"
            )

        with r2:

            st.metric(
                "Abandonment Probability",
                f"{abandonment_probability * 100:.1f}%"
            )


        st.markdown("")

        st.subheader(
            "What this means"
        )

        st.write(
            "Based on the information provided, this cart "
            "has a higher likelihood of being completed "
            "than abandoned."
        )


        # ----------------------------------------------------
        # COMPLETION STATUS
        # ----------------------------------------------------

        if completion_probability >= 0.80:

            completion_level = "High"

        elif completion_probability >= 0.60:

            completion_level = "Medium"

        else:

            completion_level = "Low"


        st.metric(
            "Completion Likelihood",
            completion_level
        )


    # ========================================================
    # INPUT SUMMARY
    # ========================================================

    st.markdown("")

    st.subheader(
        "Prediction Input"
    )

    input_summary = pd.DataFrame(
        {
            "Input": [
                "Cart Value",
                "Average Product Price",
                "Previous Purchases",
                "Purchase Rate",
                "Days Since Last Purchase",
                "Checkout Visited",
                "Payment Attempted",
                "Payment Failed",
                "Shipping Cost",
                "Coupon Attempted",
                "Coupon Applied",
                "Exit Behavior",
                "Payment Page Time",
                "Device",
                "Traffic Source"
            ],

            "Value": [
                f"${cart_value:,.2f}",

                f"${avg_price_before_cart:,.2f}",

                str(
                    previous_purchase_count
                ),

                f"{user_purchase_rate * 100:.1f}%",

                (
                    "No previous purchase"
                    if days_since_last_purchase < 0
                    else f"{days_since_last_purchase} days"
                ),

                (
                    "Yes"
                    if checkout_page_visited
                    else "No"
                ),

                (
                    "Yes"
                    if payment_attempted
                    else "No"
                ),

                (
                    "Yes"
                    if payment_failed
                    else "No"
                ),

                f"${shipping_cost_shown:,.2f}",

                (
                    "Yes"
                    if coupon_code_attempted
                    else "No"
                ),

                (
                    "Yes"
                    if coupon_applied_successfully
                    else "No"
                ),

                (
                    "Detected"
                    if exit_intent_detected
                    else "Not detected"
                ),

                f"{time_on_payment_page_seconds:.1f} sec",

                device_type,

                traffic_source
            ]
        }
    )

    st.dataframe(
        input_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# NO PREDICTION YET
# ============================================================

else:

    st.info(
        "Enter the cart information above and click "
        "\"Predict Cart Outcome\" to see the result."
    )