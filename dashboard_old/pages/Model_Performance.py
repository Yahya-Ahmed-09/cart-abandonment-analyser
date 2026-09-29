# dashboard/pages/4_📈_Model_Performance.py

import streamlit as st
import pandas as pd
from utils import FINAL_METRICS, FINAL_CONFUSION_MATRIX, PERFORMANCE_JOURNEY

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")

st.title("📈 Model Performance")
st.caption("How well the model predicts cart abandonment, and how it improved over time.")

st.divider()

# ====================================================================
# SECTION 1: KEY METRICS
# ====================================================================
st.subheader("Final Model Metrics")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Accuracy", f"{FINAL_METRICS['accuracy']:.1%}")
c2.metric("Precision", f"{FINAL_METRICS['precision']:.1%}")
c3.metric("Recall", f"{FINAL_METRICS['recall']:.1%}")
c4.metric("F1 Score", f"{FINAL_METRICS['f1']:.1%}")
c5.metric("ROC-AUC", f"{FINAL_METRICS['roc_auc']:.1%}")

st.info(
    "📌 The model correctly classifies about **59% of carts** — better than "
    "random guessing (54%), but not highly reliable. This is a data "
    "limitation, not a modeling flaw (see Root-Cause Analysis in project docs)."
)

st.divider()

# ====================================================================
# SECTION 2: CONFUSION MATRIX (plain-language version)
# ====================================================================
st.subheader("Confusion Matrix — How Predictions Break Down")

tn, fp = FINAL_CONFUSION_MATRIX[0]
fn, tp = FINAL_CONFUSION_MATRIX[1]

col1, col2 = st.columns(2)
with col1:
    st.success(f"✅ **Correctly predicted Completed:** {tn:,}")
    st.error(f"❌ **Wrongly predicted Abandoned (false alarm):** {fp:,}")
with col2:
    st.success(f"✅ **Correctly predicted Abandoned:** {tp:,}")
    st.error(f"❌ **Wrongly predicted Completed (missed it):** {fn:,}")

st.caption(
    "A 'false alarm' means the model flagged a cart as abandoned but the "
    "customer actually completed the purchase. A 'missed it' means the model "
    "thought the customer would complete the purchase, but they abandoned it."
)

st.divider()

# ====================================================================
# SECTION 3: HOW WE GOT HERE (improvement journey)
# ====================================================================
st.subheader("How the Model Improved Over Time")

journey_df = pd.DataFrame(PERFORMANCE_JOURNEY).set_index("stage")
journey_df.columns = ["Accuracy", "ROC-AUC"]

st.line_chart(journey_df)

st.markdown(
    """
    - **Original model** had a bug in how it defined "abandoned" (only checked the same browsing session).
    - **Fixing the bug** made the label more accurate, but didn't change performance much.
    - **New features** (like category-level abandonment history) gave a small boost.
    - **Final tuning** squeezed out the last bit of improvement.
    """
)

st.info(
    "📌 Every reasonable improvement was tried. The remaining gap to a higher "
    "accuracy is explained by missing data (checkout and payment signals are "
    "not available in this dataset), not by the modeling approach."
)