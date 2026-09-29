import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap

from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cart Details — CartSense",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "synthetic-cart-data.csv"
)

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
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        DATA_PATH
    )


@st.cache_resource
def load_model():

    return joblib.load(
        MODEL_PATH
    )


df = load_data()

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
        "CART DETAILS"
    )


# ============================================================
# HEADER
# ============================================================

st.caption(
    "CART DETAILS"
)

st.title(
    "Cart Details"
)

st.write(
    "Review an individual cart session and, for abandoned "
    "carts, see the most likely reasons for abandonment."
)

st.markdown("")


# ============================================================
# STATUS FILTER
# ============================================================

st.subheader(
    "Cart Status"
)

status_filter = st.radio(
    "Show",
    [
        "Abandoned",
        "Completed"
    ],
    horizontal=True,
    index=0
)


# ============================================================
# FILTER DATA
# ============================================================

if status_filter == "Abandoned":

    filtered_df = df[
        df["is_abandoned"] == 1
    ].copy()

else:

    filtered_df = df[
        df["is_abandoned"] == 0
    ].copy()


# ============================================================
# SESSION SELECTOR
# ============================================================

if filtered_df.empty:

    st.warning(
        "No sessions are available for this status."
    )

    st.stop()


session_ids = (
    filtered_df["session_id"]
    .astype(str)
    .tolist()
)

selected_session = st.selectbox(
    "Select Session",
    session_ids
)


# ============================================================
# SELECT SESSION
# ============================================================

selected_mask = (
    filtered_df["session_id"]
    .astype(str)
    == selected_session
)

selected_index = (
    filtered_df.index[selected_mask][0]
)

selected_row = df.loc[
    selected_index
]


# ============================================================
# BASIC DETAILS
# ============================================================

st.markdown("")

st.subheader(
    "Session Overview"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Session",
        str(selected_row["session_id"])
    )

with c2:

    st.metric(
        "Cart Value",
        f"${float(selected_row['cart_value']):,.2f}"
    )

with c3:

    st.metric(
        "Average Product Price",
        f"${float(selected_row['avg_price_before_cart']):,.2f}"
    )

with c4:

    st.metric(
        "Device",
        str(selected_row["device_type"])
    )


# ============================================================
# TRAFFIC / CUSTOMER DETAILS
# ============================================================

st.markdown("")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Traffic Source",
        str(selected_row["traffic_source"])
    )

with c2:

    st.metric(
        "Previous Purchases",
        int(
            selected_row[
                "previous_purchase_count"
            ]
        )
    )

with c3:

    st.metric(
        "Purchase Rate",
        f"{float(selected_row['user_purchase_rate']) * 100:.1f}%"
    )

with c4:

    previous_days = float(
        selected_row[
            "days_since_last_purchase"
        ]
    )

    if previous_days < 0:

        recency_text = "No previous purchase"

    else:

        recency_text = (
            f"{previous_days:.0f} days"
        )

    st.metric(
        "Last Purchase",
        recency_text
    )


# ============================================================
# ABANDONMENT REASON ENGINE
# ============================================================

def get_abandonment_reasons(row, data):

    reasons = []

    # --------------------------------------------------------
    # REFERENCE VALUES
    # --------------------------------------------------------

    cart_value = float(
        row["cart_value"]
    )

    avg_price = float(
        row["avg_price_before_cart"]
    )

    shipping_cost = float(
        row["shipping_cost_shown"]
    )

    purchase_rate = float(
        row["user_purchase_rate"]
    )

    previous_purchases = int(
        row["previous_purchase_count"]
    )

    payment_time = float(
        row["time_on_payment_page_seconds"]
    )

    median_cart_value = float(
        data["cart_value"].median()
    )

    median_avg_price = float(
        data["avg_price_before_cart"].median()
    )

    median_shipping = float(
        data["shipping_cost_shown"].median()
    )

    median_payment_time = float(
        data[
            "time_on_payment_page_seconds"
        ].median()
    )

    # --------------------------------------------------------
    # 1. PAYMENT FAILURE
    # --------------------------------------------------------

    if int(row["payment_failed"]) == 1:

        reasons.append(
            (
                1,
                "Payment failed",
                "The payment failed during the session."
            )
        )

    # --------------------------------------------------------
    # 2. EXIT BEHAVIOR
    # --------------------------------------------------------

    if int(row["exit_intent_detected"]) == 1:

        reasons.append(
            (
                2,
                "The customer showed exit behavior",
                "The session showed signs that the customer "
                "was about to leave the shopping session."
            )
        )

    # --------------------------------------------------------
    # 3. CHECKOUT NOT REACHED
    # --------------------------------------------------------

    if int(row["checkout_page_visited"]) == 0:

        reasons.append(
            (
                3,
                "Checkout was not reached",
                "The customer added items to the cart but "
                "did not reach the checkout stage."
            )
        )

    # --------------------------------------------------------
    # 4. HIGH CART VALUE
    # --------------------------------------------------------

    if cart_value >= median_cart_value * 1.50:

        reasons.append(
            (
                4,
                "The cart value was high",
                f"The cart was worth ${cart_value:,.2f}, "
                "which was considerably higher than a typical "
                "cart value."
            )
        )

    # --------------------------------------------------------
    # 5. HIGH PRODUCT PRICE
    # --------------------------------------------------------

    if avg_price >= median_avg_price * 1.50:

        reasons.append(
            (
                5,
                "The products were relatively expensive",
                f"The average product price was ${avg_price:,.2f}, "
                "which was considerably higher than the typical "
                "product price."
            )
        )

    # --------------------------------------------------------
    # 6. HIGH SHIPPING COST
    # --------------------------------------------------------

    if (
        shipping_cost > 0
        and shipping_cost >= max(
            15,
            median_shipping * 2
        )
    ):

        reasons.append(
            (
                6,
                "The shipping cost was relatively high",
                f"A shipping cost of ${shipping_cost:,.2f} "
                "was shown during the session."
            )
        )

    # --------------------------------------------------------
    # 7. COUPON NOT SUCCESSFULLY APPLIED
    # --------------------------------------------------------

    coupon_attempted = int(
        row["coupon_code_attempted"]
    )

    coupon_success = int(
        row["coupon_applied_successfully"]
    )

    if (
        coupon_attempted == 1
        and coupon_success == 0
    ):

        reasons.append(
            (
                7,
                "The coupon was not successfully applied",
                "The customer tried to use a coupon, "
                "but it was not successfully applied."
            )
        )

    # --------------------------------------------------------
    # 8. LOW PURCHASE HISTORY
    # --------------------------------------------------------

    if (
        purchase_rate <= 0.10
        and previous_purchases <= 1
    ):

        reasons.append(
            (
                8,
                "The customer had limited purchase history",
                "The customer had little previous purchase "
                "activity."
            )
        )

    # --------------------------------------------------------
    # 9. LONG PAYMENT PAGE TIME
    # --------------------------------------------------------

    if (
        payment_time > 0
        and payment_time >= median_payment_time * 1.75
    ):

        reasons.append(
            (
                9,
                "The customer spent a long time on the payment page",
                f"The customer spent {payment_time:.1f} seconds "
                "on the payment page before the session ended."
            )
        )

    # --------------------------------------------------------
    # 10. MOBILE SESSION
    # --------------------------------------------------------

    if str(row["device_type"]).lower() == "mobile":

        reasons.append(
            (
                10,
                "The customer was shopping on a mobile device",
                "The session was made from a mobile device, "
                "which was associated with higher abandonment "
                "rates."
            )
        )

    # --------------------------------------------------------
    # SORT BY IMPORTANCE
    # --------------------------------------------------------

    reasons = sorted(
        reasons,
        key=lambda x: x[0]
    )

    return reasons




# ============================================================
# CART CONTENTS
# ============================================================

st.markdown("")

st.subheader(
    "Cart Contents"
)

st.caption(
    "Available cart information for this session."
)

cart_col1, cart_col2, cart_col3 = st.columns(3)

with cart_col1:

    st.metric(
        "Total Cart Value",
        f"${float(selected_row['cart_value']):,.2f}"
    )

with cart_col2:

    st.metric(
        "Average Product Price",
        f"${float(selected_row['avg_price_before_cart']):,.2f}"
    )

with cart_col3:

    st.metric(
        "Product-Level Data",
        "Not Available"
    )






# ============================================================
# DISPLAY ABANDONMENT REASONS
# ============================================================

if status_filter == "Abandoned":

    st.markdown("")

    st.subheader(
        "Why was this cart possibly abandoned?"
    )

    st.caption(
        "These are the most relevant behavioral reasons "
        "identified for this session."
    )

    reasons = get_abandonment_reasons(
        selected_row,
        df
    )

    # --------------------------------------------------------
    # SHOW REASONS
    # --------------------------------------------------------

    if reasons:

        # Show maximum 5 reasons
        reasons_to_show = reasons[:5]

        for number, (
            priority,
            title,
            description
        ) in enumerate(
            reasons_to_show,
            start=1
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### {number}. {title}"
                )

                st.write(
                    description
                )

    else:

        st.info(
            "No clear behavioral reason was identified "
            "for this cart."
        )


# ============================================================
# COMPLETED CART DETAILS
# ============================================================

else:

    st.markdown("")

    st.subheader(
        "Order Details"
    )

    st.caption(
        "Details for this completed purchase session."
    )

    order_col1, order_col2 = st.columns(
        2,
        gap="large"
    )

    # --------------------------------------------------------
    # CUSTOMER / CART
    # --------------------------------------------------------

    with order_col1:

        with st.container(
            border=True
        ):

            st.subheader(
                "Cart Information"
            )

            order_details = pd.DataFrame(
                {
                    "Detail": [
                        "Cart Value",
                        "Average Product Price",
                        "Previous Purchases",
                        "Purchase Rate",
                        "Device",
                        "Traffic Source"
                    ],
                    "Value": [
                        f"${float(selected_row['cart_value']):,.2f}",
                        f"${float(selected_row['avg_price_before_cart']):,.2f}",
                        str(
                            int(
                                selected_row[
                                    "previous_purchase_count"
                                ]
                            )
                        ),
                        f"{float(selected_row['user_purchase_rate']) * 100:.1f}%",
                        str(
                            selected_row["device_type"]
                        ),
                        str(
                            selected_row["traffic_source"]
                        )
                    ]
                }
            )

            st.dataframe(
                order_details,
                use_container_width=True,
                hide_index=True
            )


    # --------------------------------------------------------
    # CHECKOUT / PAYMENT
    # --------------------------------------------------------

    with order_col2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Purchase Activity"
            )

            purchase_details = pd.DataFrame(
                {
                    "Activity": [
                        "Checkout Visited",
                        "Payment Attempted",
                        "Payment Failed",
                        "Shipping Cost Shown",
                        "Coupon Attempted",
                        "Coupon Applied",
                        "Payment Page Time"
                    ],
                    "Status": [
                        (
                            "Yes"
                            if int(
                                selected_row[
                                    "checkout_page_visited"
                                ]
                            ) == 1
                            else "No"
                        ),
                        (
                            "Yes"
                            if int(
                                selected_row[
                                    "payment_attempted"
                                ]
                            ) == 1
                            else "No"
                        ),
                        (
                            "Yes"
                            if int(
                                selected_row[
                                    "payment_failed"
                                ]
                            ) == 1
                            else "No"
                        ),
                        (
                            f"${float(selected_row['shipping_cost_shown']):,.2f}"
                        ),
                        (
                            "Yes"
                            if int(
                                selected_row[
                                    "coupon_code_attempted"
                                ]
                            ) == 1
                            else "No"
                        ),
                        (
                            "Yes"
                            if int(
                                selected_row[
                                    "coupon_applied_successfully"
                                ]
                            ) == 1
                            else "No"
                        ),
                        (
                            f"{float(selected_row['time_on_payment_page_seconds']):,.1f} sec"
                        )
                    ]
                }
            )

            st.dataframe(
                purchase_details,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# SESSION BEHAVIOR
# ============================================================

st.markdown("")

st.subheader(
    "Session Behavior"
)

behavior_data = pd.DataFrame(
    {
        "Behavior": [
            "Checkout Page",
            "Payment Attempt",
            "Payment Failure",
            "Shipping Cost",
            "Coupon Attempt",
            "Coupon Applied",
            "Exit Behavior"
        ],
        "Observed": [
            (
                "Yes"
                if int(
                    selected_row[
                        "checkout_page_visited"
                    ]
                ) == 1
                else "No"
            ),
            (
                "Yes"
                if int(
                    selected_row[
                        "payment_attempted"
                    ]
                ) == 1
                else "No"
            ),
            (
                "Yes"
                if int(
                    selected_row[
                        "payment_failed"
                    ]
                ) == 1
                else "No"
            ),
            (
                f"${float(selected_row['shipping_cost_shown']):,.2f}"
            ),
            (
                "Yes"
                if int(
                    selected_row[
                        "coupon_code_attempted"
                    ]
                ) == 1
                else "No"
            ),
            (
                "Yes"
                if int(
                    selected_row[
                        "coupon_applied_successfully"
                    ]
                ) == 1
                else "No"
            ),
            (
                "Detected"
                if int(
                    selected_row[
                        "exit_intent_detected"
                    ]
                ) == 1
                else "Not detected"
            )
        ]
    }
)

st.dataframe(
    behavior_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("")

st.caption(
    "CartSense • Cart Details"
)