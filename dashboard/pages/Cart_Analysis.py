import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cart Analysis — CartSense",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = BASE_DIR / "data" / "synthetic-cart-data.csv"

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    html,
    body,
    [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
    }

    .stApp {
        background-color: #F7F8FA !important;
        color: #111827 !important;
    }

    .main {
        background-color: #F7F8FA !important;
    }

    .block-container {
        background-color: #F7F8FA !important;
        color: #111827 !important;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* =====================================================
       FORCE TEXT COLORS
       ===================================================== */

    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div,
    .stApp small {
        color: #111827;
    }

    .stApp p {
        color: #6B7280;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #111827 !important;
    }

    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937;
    }

    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #E5E7EB !important;
    }

    section[data-testid="stSidebar"] button {
        color: #E5E7EB !important;
    }

    /* =====================================================
       PAGE HEADER
       ===================================================== */

    .page-eyebrow {
        color: #6366F1 !important;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .page-title {
        color: #111827 !important;
        font-size: 38px;
        font-weight: 750;
        letter-spacing: -0.04em;
        margin: 0;
    }

    .page-description {
        color: #6B7280 !important;
        font-size: 15px;
        margin-top: 7px;
        margin-bottom: 25px;
    }

    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 16px !important;
        padding: 18px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    [data-testid="stMetricLabel"] {
        color: #6B7280 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #6B7280 !important;
    }

    /* =====================================================
       CONTAINERS / CARDS
       ===================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 18px !important;
        padding: 4px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    [data-testid="stVerticalBlockBorderWrapper"] h1,
    [data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stVerticalBlockBorderWrapper"] p {
        color: #111827 !important;
    }

    /* =====================================================
       CAPTIONS
       ===================================================== */

    [data-testid="stCaptionContainer"] {
        color: #6B7280 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #6B7280 !important;
    }

    /* =====================================================
       FILTER / EXPANDER
       ===================================================== */

    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
    }

    [data-testid="stExpander"] summary {
        color: #111827 !important;
    }

    [data-testid="stExpander"] summary span {
        color: #111827 !important;
    }

    /* =====================================================
       SELECTBOX / MULTISELECT
       ===================================================== */

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #D1D5DB !important;
    }

    div[data-baseweb="select"] span {
        color: #111827 !important;
    }

    /* =====================================================
       INPUTS
       ===================================================== */

    input {
        color: #111827 !important;
        background-color: #FFFFFF !important;
    }

    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        color: #FFFFFF !important;
        background-color: #4F46E5 !important;
        border: none !important;
        border-radius: 10px !important;
    }

    /* =====================================================
       INFO / WARNING
       ===================================================== */

    [data-testid="stAlert"] p {
        color: #374151 !important;
    }

    /* =====================================================
       DATAFRAME
       ===================================================== */

    [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
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
    return pd.read_csv(DATA_PATH)


df = load_data()

# ============================================================
# DATA VALIDATION
# ============================================================

required_columns = [
    "is_abandoned",
    "cart_value",
    "avg_price_before_cart",
    "device_type",
    "traffic_source",
    "payment_attempted",
    "checkout_page_visited",
    "payment_failed",
    "shipping_cost_shown",
    "coupon_code_attempted",
    "coupon_applied_successfully",
    "exit_intent_detected",
    "time_on_payment_page_seconds",
    "user_purchase_rate",
    "days_since_last_purchase"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The synthetic dataset is missing required columns."
    )

    st.code(
        "\n".join(missing_columns)
    )

    st.stop()

# ============================================================
# STATUS
# ============================================================

df["status"] = df["is_abandoned"].map(
    {
        0: "Completed",
        1: "Abandoned"
    }
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            padding:10px 4px 28px 4px;
        ">
            <div style="
                color:white;
                font-size:23px;
                font-weight:750;
                letter-spacing:-0.04em;
            ">
                CartSense
            </div>

            <div style="
                color:#9CA3AF;
                font-size:11px;
                margin-top:3px;
            ">
                Cart Abandonment Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Navigation")

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

    st.caption("Synthetic Simulation")
    st.caption("Cart behavior analysis")

# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    '<div class="page-eyebrow">Cart Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-title">Cart Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="page-description">
        Explore cart behavior, customer activity, pricing patterns,
        checkout signals, and the differences between completed
        and abandoned carts.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FILTERS
# ============================================================

with st.expander(
    "Filters",
    expanded=False
):

    f1, f2, f3, f4 = st.columns(4)

    with f1:

        status_filter = st.multiselect(
            "Cart Status",
            options=[
                "Completed",
                "Abandoned"
            ],
            default=[
                "Completed",
                "Abandoned"
            ]
        )

    with f2:

        device_options = sorted(
            df["device_type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        device_filter = st.multiselect(
            "Device",
            options=device_options,
            default=device_options
        )

    with f3:

        traffic_options = sorted(
            df["traffic_source"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        traffic_filter = st.multiselect(
            "Traffic Source",
            options=traffic_options,
            default=traffic_options
        )

    with f4:

        payment_filter = st.selectbox(
            "Payment Attempt",
            [
                "All",
                "Attempted",
                "Not Attempted"
            ]
        )

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["status"].isin(status_filter)
    &
    df["device_type"].isin(device_filter)
    &
    df["traffic_source"].isin(traffic_filter)
].copy()

if payment_filter == "Attempted":

    filtered_df = filtered_df[
        filtered_df["payment_attempted"] == 1
    ]

elif payment_filter == "Not Attempted":

    filtered_df = filtered_df[
        filtered_df["payment_attempted"] == 0
    ]

if filtered_df.empty:

    st.warning(
        "No sessions match the selected filters."
    )

    st.stop()

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_carts = len(filtered_df)

abandoned_count = int(
    filtered_df["is_abandoned"].sum()
)

completed_count = (
    total_carts - abandoned_count
)

abandonment_rate = (
    abandoned_count / total_carts * 100
)

avg_cart_value = (
    filtered_df["cart_value"].mean()
)

avg_product_price = (
    filtered_df["avg_price_before_cart"].mean()
)

# ============================================================
# KPI ROW
# ============================================================

st.markdown("### Cart Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Filtered Carts",
        f"{total_carts:,}"
    )

with k2:

    st.metric(
        "Abandonment Rate",
        f"{abandonment_rate:.1f}%",
        f"{abandoned_count:,} abandoned"
    )

with k3:

    st.metric(
        "Average Cart Value",
        f"${avg_cart_value:,.2f}"
    )

with k4:

    st.metric(
        "Average Product Price",
        f"${avg_product_price:,.2f}"
    )

st.markdown(
    '<div class="section-gap"></div>',
    unsafe_allow_html=True
)

# ============================================================
# CART OUTCOMES
# ============================================================

left, right = st.columns(
    [1, 1.2],
    gap="large"
)

# ------------------------------------------------------------
# CART OUTCOME
# ------------------------------------------------------------

with left:

    with st.container(border=True):

        st.subheader("Cart Outcomes")

        st.caption(
            "Completed versus abandoned carts."
        )

        outcome_data = pd.DataFrame({
            "Status": [
                "Completed",
                "Abandoned"
            ],
            "Sessions": [
                completed_count,
                abandoned_count
            ]
        })

        fig = px.pie(
            outcome_data,
            names="Status",
            values="Sessions",
            hole=0.68
        )

        fig.update_traces(
            textinfo="percent",
            textposition="inside"
        )

        fig.update_layout(
            height=330,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            legend=dict(
                orientation="h",
                y=-0.05
            ),
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# CART VALUE
# ------------------------------------------------------------

with right:

    with st.container(border=True):

        st.subheader("Cart Value by Outcome")

        st.caption(
            "Average cart value for completed and abandoned sessions."
        )

        value_data = (
            filtered_df
            .groupby("status")["cart_value"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            value_data,
            x="status",
            y="cart_value",
            text_auto=".2f"
        )

        fig.update_traces(
            marker_color="#4F46E5"
        )

        fig.update_layout(
            height=330,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            xaxis_title=None,
            yaxis_title="Average Cart Value",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


st.markdown("")


# ============================================================
# PRICE + PAYMENT PAGE TIME
# ============================================================

left, right = st.columns(
    2,
    gap="large"
)


# ------------------------------------------------------------
# PRODUCT PRICE
# ------------------------------------------------------------

with left:

    with st.container(border=True):

        st.subheader("Average Product Price")

        st.caption(
            "Average pre-cart product price by cart outcome."
        )

        price_data = (
            filtered_df
            .groupby("status")[
                "avg_price_before_cart"
            ]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            price_data,
            x="status",
            y="avg_price_before_cart",
            text_auto=".2f"
        )

        fig.update_traces(
            marker_color="#6366F1"
        )

        fig.update_layout(
            height=310,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            xaxis_title=None,
            yaxis_title="Average Price",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# PAYMENT PAGE TIME
# ------------------------------------------------------------

with right:

    with st.container(border=True):

        st.subheader("Payment Page Time")

        st.caption(
            "Average time spent on the payment page by cart outcome."
        )

        payment_time_data = (
            filtered_df
            .groupby("status")[
                "time_on_payment_page_seconds"
            ]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            payment_time_data,
            x="status",
            y="time_on_payment_page_seconds",
            text_auto=".1f"
        )

        fig.update_traces(
            marker_color="#818CF8"
        )

        fig.update_layout(
            height=310,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            xaxis_title=None,
            yaxis_title="Seconds",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


st.markdown("")


# ============================================================
# DEVICE + TRAFFIC SOURCE
# ============================================================

left, right = st.columns(
    2,
    gap="large"
)


# ------------------------------------------------------------
# DEVICE
# ------------------------------------------------------------

with left:

    with st.container(border=True):

        st.subheader("Cart Outcomes by Device")

        st.caption(
            "Completed and abandoned carts across device types."
        )

        device_data = (
            filtered_df
            .groupby(
                [
                    "device_type",
                    "status"
                ]
            )
            .size()
            .reset_index(
                name="Sessions"
            )
        )

        fig = px.bar(
            device_data,
            x="device_type",
            y="Sessions",
            color="status",
            barmode="group"
        )

        fig.update_layout(
            height=320,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            xaxis_title=None,
            yaxis_title=None,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# TRAFFIC SOURCE
# ------------------------------------------------------------

with right:

    with st.container(border=True):

        st.subheader("Cart Outcomes by Traffic Source")

        st.caption(
            "Completed and abandoned carts by acquisition source."
        )

        traffic_data = (
            filtered_df
            .groupby(
                [
                    "traffic_source",
                    "status"
                ]
            )
            .size()
            .reset_index(
                name="Sessions"
            )
        )

        fig = px.bar(
            traffic_data,
            x="traffic_source",
            y="Sessions",
            color="status",
            barmode="group"
        )

        fig.update_layout(
            height=320,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            xaxis_title=None,
            yaxis_title=None,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# CHECKOUT & PAYMENT BEHAVIOR
# ============================================================

st.markdown("")

with st.container(border=True):

    st.subheader("Checkout & Payment Behavior")

    st.caption(
        "Compare important behavioral signals between "
        "completed and abandoned carts."
    )

    behavior_columns = [
        "checkout_page_visited",
        "payment_attempted",
        "payment_failed",
        "shipping_cost_shown",
        "coupon_code_attempted",
        "coupon_applied_successfully",
        "exit_intent_detected"
    ]

    behavior_labels = {
        "checkout_page_visited": "Checkout Visited",
        "payment_attempted": "Payment Attempted",
        "payment_failed": "Payment Failed",
        "shipping_cost_shown": "Shipping Cost Shown",
        "coupon_code_attempted": "Coupon Attempted",
        "coupon_applied_successfully": "Coupon Applied",
        "exit_intent_detected": "Exit Intent"
    }

    behavior_rows = []

    for column in behavior_columns:

        for status in [
            "Completed",
            "Abandoned"
        ]:

            subset = filtered_df[
                filtered_df["status"] == status
            ]

            if len(subset) == 0:
                percentage = 0
            else:
                percentage = (
                    subset[column].mean() * 100
                )

            behavior_rows.append({
                "Behavior": behavior_labels[column],
                "Status": status,
                "Percentage": percentage
            })

    behavior_data = pd.DataFrame(
        behavior_rows
    )

    fig = px.bar(
        behavior_data,
        x="Behavior",
        y="Percentage",
        color="Status",
        barmode="group",
        text_auto=".1f"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        xaxis_title=None,
        yaxis_title="Sessions (%)",
        yaxis_range=[
            0,
            min(
                100,
                behavior_data["Percentage"].max() + 10
            )
        ],
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title=None
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PURCHASE BEHAVIOR
# ============================================================

st.markdown("")

left, right = st.columns(
    2,
    gap="large"
)


# ------------------------------------------------------------
# USER PURCHASE RATE
# ------------------------------------------------------------

with left:

    with st.container(border=True):

        st.subheader("User Purchase Rate")

        st.caption(
            "Historical purchase rate of users by cart outcome."
        )

        purchase_rate_data = (
            filtered_df
            .groupby("status")[
                "user_purchase_rate"
            ]
            .mean()
            .reset_index()
        )

        purchase_rate_data[
            "user_purchase_rate"
        ] = (
            purchase_rate_data[
                "user_purchase_rate"
            ] * 100
        )

        fig = px.bar(
            purchase_rate_data,
            x="status",
            y="user_purchase_rate",
            text_auto=".1f"
        )

        fig.update_traces(
            marker_color="#4F46E5"
        )

        fig.update_layout(
            height=310,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            xaxis_title=None,
            yaxis_title="Purchase Rate (%)",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# PURCHASE RECENCY
# ------------------------------------------------------------

with right:

    with st.container(border=True):

        st.subheader("Purchase Recency")

        st.caption(
            "Average days since the user's previous purchase."
        )

        recency_data = (
            filtered_df
            .groupby("status")[
                "days_since_last_purchase"
            ]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            recency_data,
            x="status",
            y="days_since_last_purchase",
            text_auto=".1f"
        )

        fig.update_traces(
            marker_color="#818CF8"
        )

        fig.update_layout(
            height=310,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            xaxis_title=None,
            yaxis_title="Days",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# KEY INSIGHT
# ============================================================

st.markdown("")

overall_abandonment = (
    df["is_abandoned"].mean() * 100
)

filtered_abandonment = (
    filtered_df["is_abandoned"].mean() * 100
)

if filtered_abandonment > overall_abandonment:

    insight_text = (
        f"The current filtered segment has an abandonment "
        f"rate of {filtered_abandonment:.1f}%, which is above "
        f"the overall dataset rate of "
        f"{overall_abandonment:.1f}%."
    )

elif filtered_abandonment < overall_abandonment:

    insight_text = (
        f"The current filtered segment has an abandonment "
        f"rate of {filtered_abandonment:.1f}%, which is below "
        f"the overall dataset rate of "
        f"{overall_abandonment:.1f}%."
    )

else:

    insight_text = (
        f"The current filtered segment has an abandonment "
        f"rate of {filtered_abandonment:.1f}%, matching the "
        f"overall dataset rate."
    )

st.info(
    insight_text
)


# ============================================================
# DATASET NOTE
# ============================================================

st.caption(
    "Synthetic Simulation — Cart analysis is based on the "
    "synthetic dataset and demonstrates the prediction and "
    "explainability workflow."
)