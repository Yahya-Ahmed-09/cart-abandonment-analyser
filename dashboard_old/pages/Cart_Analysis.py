# dashboard/pages/2_📊_Cart_Analysis.py
# Shows WHERE and WHEN abandonment happens most — by category, time, and price.

import streamlit as st
import pandas as pd
from utils import load_model_data, load_cart_item_identity

st.set_page_config(page_title="Cart Analysis", page_icon="📊", layout="wide")

st.title("📊 Cart Analysis")
st.caption("Patterns in when and where cart abandonment happens most.")

# ====================================================================
# LOAD DATA
# ====================================================================
df = load_model_data()
item_identity = load_cart_item_identity()
df = df.merge(item_identity, on="reconstructed_session_id", how="left")

st.divider()

# ====================================================================
# SECTION 1: ABANDONMENT BY CATEGORY
# ====================================================================
st.subheader("🏷️ Abandonment Rate by Category")
st.caption("Only categories with at least 50 cart sessions are shown, to avoid misleading small-sample results.")

category_stats = (
    df.groupby("category_code")["is_abandoned"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "abandonment_rate", "count": "num_sessions"})
)
category_stats = category_stats[category_stats["num_sessions"] >= 50]
top_categories = category_stats.sort_values("abandonment_rate", ascending=False).head(10)

st.bar_chart(top_categories["abandonment_rate"])

if len(top_categories) > 0:
    worst_category = top_categories.index[0]
    worst_rate = top_categories.iloc[0]["abandonment_rate"]
    st.info(f"📌 **{worst_category}** has the highest abandonment rate at **{worst_rate:.1%}**.")

st.divider()

# ====================================================================
# SECTION 2: ABANDONMENT BY TIME OF DAY
# ====================================================================
st.subheader("🕐 Abandonment Rate by Hour of Day")

hourly_stats = df.groupby("cart_hour")["is_abandoned"].mean()
st.bar_chart(hourly_stats)

worst_hour = hourly_stats.idxmax()
worst_hour_rate = hourly_stats.max()
st.info(f"📌 Carts started around **{worst_hour}:00** are abandoned most often (**{worst_hour_rate:.1%}**).")

st.divider()

# ====================================================================
# SECTION 3: ABANDONMENT BY DAY OF WEEK
# ====================================================================
st.subheader("📅 Abandonment Rate by Day of Week")

day_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
daily_stats = df.groupby("cart_day_of_week")["is_abandoned"].mean()
daily_stats.index = daily_stats.index.map(day_names)

st.bar_chart(daily_stats)

worst_day = daily_stats.idxmax()
worst_day_rate = daily_stats.max()
st.info(f"📌 **{worst_day}** has the highest abandonment rate (**{worst_day_rate:.1%}**).")

st.divider()

# ====================================================================
# SECTION 4: ABANDONMENT BY PRICE RANGE
# ====================================================================
st.subheader("💰 Abandonment Rate by Price Range")

price_bins = [0, 50, 150, 300, 600, float("inf")]
price_labels = ["$0-50", "$50-150", "$150-300", "$300-600", "$600+"]
df["price_bucket"] = pd.cut(df["avg_price_before_cart"], bins=price_bins, labels=price_labels)

price_stats = df.groupby("price_bucket", observed=True)["is_abandoned"].mean()
st.bar_chart(price_stats)

worst_price = price_stats.idxmax()
worst_price_rate = price_stats.max()
st.info(f"📌 Carts priced **{worst_price}** have the highest abandonment rate (**{worst_price_rate:.1%}**).")