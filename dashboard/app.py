import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CartSense — Cart Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "synthetic-cart-data.csv"
MODEL_PATH = BASE_DIR / "models" / "synthetic_final_model.pkl"


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* -----------------------------
       Hide Streamlit defaults
    ----------------------------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* -----------------------------
       Main application
    ----------------------------- */

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


    /* -----------------------------
       Typography
    ----------------------------- */

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {
        color: #111827 !important;
    }

    .stApp p {
        color: #6B7280;
    }


    /* -----------------------------
       Sidebar
    ----------------------------- */

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


    /* -----------------------------
       Native metric cards
    ----------------------------- */

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


    /* -----------------------------
       Native bordered containers
    ----------------------------- */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 18px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }


    /* -----------------------------
       Expander
    ----------------------------- */

    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
    }

    [data-testid="stExpander"] summary {
        color: #111827 !important;
    }


    /* -----------------------------
       Inputs
    ----------------------------- */

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #D1D5DB !important;
    }

    div[data-baseweb="select"] span {
        color: #111827 !important;
    }

    input {
        color: #111827 !important;
        background-color: #FFFFFF !important;
    }


    /* -----------------------------
       Captions
    ----------------------------- */

    [data-testid="stCaptionContainer"] {
        color: #6B7280 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #6B7280 !important;
    }


    /* -----------------------------
       Info box
    ----------------------------- */

    [data-testid="stAlert"] p {
        color: #374151 !important;
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


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


df = load_data()
model = load_model()


# ============================================================
# BASIC CALCULATIONS
# ============================================================

total_sessions = len(df)

abandoned = int(
    df["is_abandoned"].sum()
)

completed = total_sessions - abandoned

abandonment_rate = (
    abandoned / total_sessions * 100
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## CartSense")

    # st.caption(
    #     "Cart Abandonment Intelligence"
    # )

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

    st.caption("ACTIVE MODEL")

    st.write(
        "Synthetic Logistic Regression"
    )

    st.caption(
        "Synthetic simulation"
    )

    st.success(
        "Model Online"
    )


# ============================================================
# HEADER
# ============================================================

st.caption("CART INTELLIGENCE")

st.title(
    "Understand your carts."
)

st.write(
    "Monitor abandonment patterns, predict cart outcomes, "
    "and understand what drives each prediction."
)

st.markdown("")


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Total Sessions",
        f"{total_sessions:,}"
    )

with k2:

    st.metric(
        "Abandoned Carts",
        f"{abandoned:,}",
        f"{abandonment_rate:.1f}%"
    )

with k3:

    st.metric(
        "Completed Carts",
        f"{completed:,}"
    )

with k4:

    st.metric(
        "Model Accuracy",
        "90.30%"
    )


st.markdown("")


# ============================================================
# MAIN ANALYTICS
# ============================================================

left, right = st.columns(
    [1.15, 1],
    gap="large"
)


# ============================================================
# CART OUTCOMES
# ============================================================

with left:

    with st.container(border=True):

        st.subheader(
            "Cart Outcomes"
        )

        st.caption(
            "Distribution of completed and abandoned carts."
        )

        chart_data = pd.DataFrame(
            {
                "Status": [
                    "Abandoned",
                    "Completed"
                ],
                "Sessions": [
                    abandoned,
                    completed
                ]
            }
        )

        fig = px.bar(
            chart_data,
            x="Status",
            y="Sessions",
            text="Sessions"
        )

        fig.update_traces(
            marker_color="#4F46E5",
            textposition="outside"
        )

        fig.update_layout(
            height=330,
            margin=dict(
                l=10,
                r=10,
                t=15,
                b=10
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# MODEL SNAPSHOT
# ============================================================

with right:

    with st.container(border=True):

        st.subheader(
            "Model Snapshot"
        )

        st.caption(
            "Current synthetic model benchmark."
        )

        m1, m2 = st.columns(2)

        with m1:

            st.metric(
                "Accuracy",
                "90.30%"
            )

            st.metric(
                "Recall",
                "91.96%"
            )

            st.metric(
                "ROC-AUC",
                "96.94%"
            )

        with m2:

            st.metric(
                "Precision",
                "93.13%"
            )

            st.metric(
                "F1 Score",
                "92.54%"
            )

            st.metric(
                "CV Accuracy",
                "90.30%"
            )


# ============================================================
# SYNTHETIC DATASET NOTICE
# ============================================================

st.markdown("")

st.info(
    "Synthetic Simulation — This dashboard currently uses "
    "the synthetic simulation dataset to demonstrate "
    "cart-abandonment prediction and explainability. "
    "These model metrics should not be interpreted as "
    "real-world performance on the original clickstream dataset."
)


# ============================================================
# QUICK INSIGHTS
# ============================================================

st.markdown("")

st.subheader(
    "Quick Insights"
)

q1, q2, q3 = st.columns(3)

with q1:

    with st.container(border=True):

        st.metric(
            "Abandonment Share",
            f"{abandonment_rate:.1f}%"
        )

        st.caption(
            "Share of synthetic sessions classified "
            "as abandoned."
        )


with q2:

    with st.container(border=True):

        avg_cart_value = df[
            "cart_value"
        ].mean()

        st.metric(
            "Average Cart Value",
            f"${avg_cart_value:,.2f}"
        )

        st.caption(
            "Average cart value across all sessions."
        )


with q3:

    with st.container(border=True):

        avg_price = df[
            "avg_price_before_cart"
        ].mean()

        st.metric(
            "Average Product Price",
            f"${avg_price:,.2f}"
        )

        st.caption(
            "Average product price before cart creation."
        )


# ============================================================
# TOP MODEL SIGNALS
# ============================================================

st.markdown("")

st.subheader(
    "Key Model Signals"
)

signal_data = pd.DataFrame(
    {
        "Feature": [
            "Checkout Page Visited",
            "Coupon Applied",
            "Payment Attempted",
            "Mobile Device",
            "Payment Failed",
            "Exit Intent"
        ],
        "SHAP Importance": [
            3.744,
            1.590,
            1.298,
            1.079,
            1.074,
            1.038
        ]
    }
)

fig = px.bar(
    signal_data.sort_values(
        "SHAP Importance"
    ),
    x="SHAP Importance",
    y="Feature",
    orientation="h",
    text="SHAP Importance"
)

fig.update_traces(
    marker_color="#4F46E5",
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    height=360,
    margin=dict(
        l=10,
        r=30,
        t=10,
        b=10
    ),
    xaxis_title="Mean |SHAP Value|",
    yaxis_title=None,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# FOOTER NOTE
# ============================================================

st.caption(
    "CartSense • Cart Abandonment Intelligence • "
    "Synthetic Simulation"
)