import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Abandoned Carts — CartSense",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = BASE_DIR / "data" / "synthetic-cart-data.csv"


# ============================================================
# GLOBAL STYLE
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
        max-width: 1500px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {
        color: #111827 !important;
    }

    .stApp p {
        color: #6B7280;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] p {
        color: #9CA3AF !important;
    }

    section[data-testid="stSidebar"] button {
        color: #E5E7EB !important;
    }

    /* Metrics */

    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
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

    /* Containers */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 18px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    /* Expander */

    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
    }

    [data-testid="stExpander"] summary {
        color: #111827 !important;
    }

    /* Selects */

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #D1D5DB !important;
    }

    div[data-baseweb="select"] span {
        color: #111827 !important;
    }

    /* Caption */

    [data-testid="stCaptionContainer"] {
        color: #6B7280 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #6B7280 !important;
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
# VALIDATION
# ============================================================

required_columns = [
    "is_abandoned",
    "cart_value",
    "avg_price_before_cart",
    "device_type",
    "traffic_source",
    "payment_attempted",
    "payment_failed",
    "checkout_page_visited",
    "exit_intent_detected",
    "coupon_code_attempted",
    "coupon_applied_successfully",
    "shipping_cost_shown",
    "time_on_payment_page_seconds"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "Required columns are missing from the synthetic dataset."
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

abandoned_df = df[
    df["is_abandoned"] == 1
].copy()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## CartSense")

    st.caption(
        "Cart Abandonment Intelligence"
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

    st.caption("CURRENT DATASET")

    st.write(
        "Synthetic Simulation"
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.caption("CART INTELLIGENCE")

st.title(
    "Abandoned Carts"
)

st.write(
    "Explore abandoned sessions, understand their behavior, "
    "and identify the patterns associated with cart abandonment."
)

st.markdown("")


# ============================================================
# TOP METRICS
# ============================================================

total_abandoned = len(
    abandoned_df
)

abandonment_rate = (
    total_abandoned / len(df) * 100
)

avg_abandoned_cart_value = (
    abandoned_df["cart_value"].mean()
)

avg_abandoned_price = (
    abandoned_df["avg_price_before_cart"].mean()
)


m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Abandoned Carts",
        f"{total_abandoned:,}"
    )

with m2:

    st.metric(
        "Abandonment Rate",
        f"{abandonment_rate:.1f}%"
    )

with m3:

    st.metric(
        "Average Cart Value",
        f"${avg_abandoned_cart_value:,.2f}"
    )

with m4:

    st.metric(
        "Average Product Price",
        f"${avg_abandoned_price:,.2f}"
    )


st.markdown("")


# ============================================================
# FILTERS
# ============================================================

st.subheader(
    "Filter Abandoned Carts"
)

f1, f2, f3 = st.columns(3)


with f1:

    device_options = sorted(
        abandoned_df["device_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_devices = st.multiselect(
        "Device",
        device_options,
        default=device_options
    )


with f2:

    traffic_options = sorted(
        abandoned_df["traffic_source"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_traffic = st.multiselect(
        "Traffic Source",
        traffic_options,
        default=traffic_options
    )


with f3:

    min_cart_value = float(
        abandoned_df["cart_value"].min()
    )

    max_cart_value = float(
        abandoned_df["cart_value"].max()
    )

    cart_range = st.slider(
        "Cart Value Range",
        min_value=min_cart_value,
        max_value=max_cart_value,
        value=(
            min_cart_value,
            max_cart_value
        )
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_abandoned = abandoned_df[
    abandoned_df["device_type"].isin(
        selected_devices
    )
    &
    abandoned_df["traffic_source"].isin(
        selected_traffic
    )
    &
    abandoned_df["cart_value"].between(
        cart_range[0],
        cart_range[1]
    )
].copy()


# ============================================================
# FILTER RESULT
# ============================================================

st.markdown("")

st.subheader(
    "Filtered Results"
)

st.write(
    f"{len(filtered_abandoned):,} abandoned carts match the selected filters."
)


# ============================================================
# ABANDONED CART VALUE DISTRIBUTION
# ============================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    with st.container(border=True):

        st.subheader(
            "Cart Value Distribution"
        )

        st.caption(
            "Distribution of cart values among abandoned sessions."
        )

        fig = px.histogram(
            filtered_abandoned,
            x="cart_value",
            nbins=30
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
            xaxis_title="Cart Value",
            yaxis_title="Abandoned Carts",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


with right:

    with st.container(border=True):

        st.subheader(
            "Abandoned Carts by Device"
        )

        st.caption(
            "How abandoned sessions are distributed across devices."
        )

        device_data = (
            filtered_abandoned
            .groupby("device_type")
            .size()
            .reset_index(
                name="Abandoned Carts"
            )
        )

        fig = px.bar(
            device_data,
            x="device_type",
            y="Abandoned Carts",
            text="Abandoned Carts"
        )

        fig.update_traces(
            marker_color="#6366F1",
            textposition="outside"
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

st.subheader(
    "Checkout & Payment Behavior"
)

st.caption(
    "Behavioral signals observed across abandoned cart sessions."
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

    if column not in filtered_abandoned.columns:
        continue

    percentage = (
        filtered_abandoned[column].mean() * 100
    )

    behavior_rows.append(
        {
            "Behavior": behavior_labels[column],
            "Percentage": percentage
        }
    )

behavior_data = pd.DataFrame(
    behavior_rows
)

if not behavior_data.empty:

    with st.container(border=True):

        fig = px.bar(
            behavior_data.sort_values(
                "Percentage"
            ),
            x="Percentage",
            y="Behavior",
            orientation="h",
            text_auto=".1f"
        )

        fig.update_traces(
            marker_color="#4F46E5",
            textposition="outside"
        )

        fig.update_layout(
            height=400,
            margin=dict(
                l=10,
                r=40,
                t=20,
                b=10
            ),
            xaxis_title="Abandoned Sessions (%)",
            yaxis_title=None,
            xaxis_range=[
                0,
                min(
                    100,
                    behavior_data["Percentage"].max() + 10
                )
            ],
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# COUPON & PAYMENT INSIGHTS
# ============================================================

st.markdown("")

left, right = st.columns(
    2,
    gap="large"
)


# ------------------------------------------------------------
# PAYMENT FAILURE
# ------------------------------------------------------------

with left:

    with st.container(border=True):

        st.subheader(
            "Payment Failure"
        )

        st.caption(
            "Payment failure behavior among abandoned carts."
        )

        payment_failure_rate = (
            filtered_abandoned[
                "payment_failed"
            ].mean() * 100
        )

        st.metric(
            "Payment Failure Rate",
            f"{payment_failure_rate:.1f}%"
        )

        payment_attempt_rate = (
            filtered_abandoned[
                "payment_attempted"
            ].mean() * 100
        )

        st.metric(
            "Payment Attempt Rate",
            f"{payment_attempt_rate:.1f}%"
        )


# ------------------------------------------------------------
# COUPON BEHAVIOR
# ------------------------------------------------------------

with right:

    with st.container(border=True):

        st.subheader(
            "Coupon Behavior"
        )

        st.caption(
            "Coupon interaction among abandoned carts."
        )

        coupon_attempt_rate = (
            filtered_abandoned[
                "coupon_code_attempted"
            ].mean() * 100
        )

        coupon_success_rate = (
            filtered_abandoned[
                "coupon_applied_successfully"
            ].mean() * 100
        )

        st.metric(
            "Coupon Attempt Rate",
            f"{coupon_attempt_rate:.1f}%"
        )

        st.metric(
            "Successful Coupon Rate",
            f"{coupon_success_rate:.1f}%"
        )


# ============================================================
# PAYMENT PAGE TIME
# ============================================================

st.markdown("")

with st.container(border=True):

    st.subheader(
        "Payment Page Engagement"
    )

    st.caption(
        "Time spent on the payment page across abandoned carts."
    )

    payment_time = filtered_abandoned[
        "time_on_payment_page_seconds"
    ]

    p1, p2, p3 = st.columns(3)

    with p1:

        st.metric(
            "Average",
            f"{payment_time.mean():.1f} sec"
        )

    with p2:

        st.metric(
            "Median",
            f"{payment_time.median():.1f} sec"
        )

    with p3:

        st.metric(
            "Maximum",
            f"{payment_time.max():.1f} sec"
        )


# ============================================================
# TRAFFIC SOURCE
# ============================================================

st.markdown("")

with st.container(border=True):

    st.subheader(
        "Abandoned Carts by Traffic Source"
    )

    st.caption(
        "Traffic sources generating the highest number of abandoned carts."
    )

    traffic_abandoned = (
        filtered_abandoned
        .groupby("traffic_source")
        .size()
        .reset_index(
            name="Abandoned Carts"
        )
        .sort_values(
            "Abandoned Carts",
            ascending=False
        )
    )

    fig = px.bar(
        traffic_abandoned,
        x="traffic_source",
        y="Abandoned Carts",
        text="Abandoned Carts"
    )

    fig.update_traces(
        marker_color="#6366F1",
        textposition="outside"
    )

    fig.update_layout(
        height=330,
        margin=dict(
            l=10,
            r=10,
            t=20,
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
# ABANDONED CART TABLE
# ============================================================

st.markdown("")

st.subheader(
    "Abandoned Cart Records"
)

st.caption(
    "Browse the filtered abandoned-cart sessions."
)

table_columns = [
    "session_id",
    "cart_value",
    "avg_price_before_cart",
    "device_type",
    "traffic_source",
    "checkout_page_visited",
    "payment_attempted",
    "payment_failed",
    "coupon_code_attempted",
    "coupon_applied_successfully",
    "exit_intent_detected"
]

available_table_columns = [
    column
    for column in table_columns
    if column in filtered_abandoned.columns
]

display_df = filtered_abandoned[
    available_table_columns
].copy()


# Rename columns for UI

rename_columns = {
    "session_id": "Session ID",
    "cart_value": "Cart Value",
    "avg_price_before_cart": "Avg Product Price",
    "device_type": "Device",
    "traffic_source": "Traffic Source",
    "checkout_page_visited": "Checkout",
    "payment_attempted": "Payment Attempted",
    "payment_failed": "Payment Failed",
    "coupon_code_attempted": "Coupon Attempted",
    "coupon_applied_successfully": "Coupon Applied",
    "exit_intent_detected": "Exit Intent"
}

display_df = display_df.rename(
    columns=rename_columns
)

if "Cart Value" in display_df.columns:

    display_df["Cart Value"] = (
        display_df["Cart Value"]
        .round(2)
    )

if "Avg Product Price" in display_df.columns:

    display_df["Avg Product Price"] = (
        display_df["Avg Product Price"]
        .round(2)
    )


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=460
)


# ============================================================
# HIGH-VALUE ABANDONED CARTS
# ============================================================

st.markdown("")

st.subheader(
    "Highest-Value Abandoned Carts"
)

st.caption(
    "Abandoned sessions with the highest cart values."
)

high_value_columns = [
    column
    for column in [
        "session_id",
        "cart_value",
        "avg_price_before_cart",
        "device_type",
        "traffic_source"
    ]
    if column in filtered_abandoned.columns
]

high_value_df = (
    filtered_abandoned[
        high_value_columns
    ]
    .sort_values(
        "cart_value",
        ascending=False
    )
    .head(10)
    .copy()
)

high_value_df = high_value_df.rename(
    columns=rename_columns
)

if "Cart Value" in high_value_df.columns:

    high_value_df["Cart Value"] = (
        high_value_df["Cart Value"]
        .round(2)
    )

if "Avg Product Price" in high_value_df.columns:

    high_value_df["Avg Product Price"] = (
        high_value_df["Avg Product Price"]
        .round(2)
    )

st.dataframe(
    high_value_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DATASET NOTE
# ============================================================

st.markdown("")

st.info(
    "Synthetic Simulation — These abandoned-cart records "
    "come from the synthetic dataset and are used to demonstrate "
    "cart-abandonment analysis and explainability."
)