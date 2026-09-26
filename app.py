import streamlit as st
import pandas as pd
import plotly.express as px

# ========================================
# SETTING UP THE DASHBOARD
# ========================================
st.set_page_config(page_title="Sales Data Analytics Dashboard", layout="wide")

st.title("📊 Sales Data Analytics Dashboard")
st.caption("Data Source: UCI Online Retail Dataset")
st.write("Welcome to my data analytics portfolio project! This dashboard analyzes real-world online retail transactions.")

# ========================================
# STEP 1: LOAD THE CLEANED DATASET
# ========================================
@st.cache_data
def load_data():
    # Load the cleaned dataset (original remains untouched in 'Online Retail.xlsx')
    df = pd.read_csv("data/cleaned_online_retail.csv")
    # Ensure Date column is a datetime object
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# ========================================
# STEP 2: SIDEBAR FILTERS
# ========================================
st.sidebar.header("🎯 Filter Data")

# Filter by Country
country_options = ["All"] + list(df["Country"].unique())
selected_country = st.sidebar.selectbox("Select Country", country_options)

# Filter the dataframe based on the selected country
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

# ========================================
# STEP 3: KPI SECTION (Key Performance Indicators)
# ========================================
# Calculate the totals using the filtered data
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_quantity = filtered_df["Quantity"].sum()
unique_customers = filtered_df["CustomerID"].nunique()
unique_products = filtered_df["StockCode"].nunique()

# Average Order Value = Total Revenue / Total Orders
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

st.markdown("### 🏆 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    st.metric(label="Total Orders", value=f"{total_orders:,}")
with col3:
    st.metric(label="Avg Order Value", value=f"${avg_order_value:,.2f}")
with col4:
    st.metric(label="Total Quantity Sold", value=f"{total_quantity:,}")
with col5:
    st.metric(label="Unique Customers", value=f"{unique_customers:,}")
with col6:
    st.metric(label="Unique Products", value=f"{unique_products:,}")

st.divider()

# ========================================
# STEP 4: SALES ANALYSIS (CHARTS)
# ========================================
st.markdown("### 📈 Revenue & Order Analysis")

# 1. Monthly Revenue (Line Chart)
# We group the data by YearMonth and sum the revenue
revenue_by_month = filtered_df.groupby("YearMonth")["Revenue"].sum().reset_index()

fig_monthly_rev = px.line(
    revenue_by_month, 
    x="YearMonth", 
    y="Revenue", 
    title="Monthly Revenue Trends",
    markers=True
)
st.plotly_chart(fig_monthly_rev, use_container_width=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # 2. Top 10 Products by Revenue (Bar Chart)
    top_products = filtered_df.groupby("Description")["Revenue"].sum().reset_index()
    top_products = top_products.sort_values(by="Revenue", ascending=False).head(10)
    
    fig_top_prod = px.bar(
        top_products, 
        x="Revenue", 
        y="Description", 
        orientation="h",
        title="Top 10 Products by Revenue",
        color="Revenue",
        color_continuous_scale="Blues"
    )
    fig_top_prod.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top_prod, use_container_width=True)

with col_chart2:
    # 3. Top 10 Countries by Revenue (Bar Chart) - only show if "All" countries is selected
    if selected_country == "All":
        top_countries = filtered_df.groupby("Country")["Revenue"].sum().reset_index()
        top_countries = top_countries.sort_values(by="Revenue", ascending=False).head(10)
        
        fig_top_countries = px.bar(
            top_countries, 
            x="Revenue", 
            y="Country", 
            orientation="h",
            title="Top 10 Countries by Revenue",
            color="Revenue",
            color_continuous_scale="Greens"
        )
        fig_top_countries.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_countries, use_container_width=True)
    else:
        # If a specific country is selected, let's show Quantity Sold by Top 10 Products instead
        top_qty_products = filtered_df.groupby("Description")["Quantity"].sum().reset_index()
        top_qty_products = top_qty_products.sort_values(by="Quantity", ascending=False).head(10)
        
        fig_qty_prod = px.bar(
            top_qty_products, 
            x="Quantity", 
            y="Description", 
            orientation="h",
            title="Top 10 Products by Quantity Sold",
            color="Quantity",
            color_continuous_scale="Oranges"
        )
        fig_qty_prod.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_qty_prod, use_container_width=True)

st.divider()

# ========================================
# STEP 5: KEY BUSINESS INSIGHTS
# ========================================
st.markdown("### 💡 Key Business Insights")

if not filtered_df.empty:
    # Safely get the top product
    best_product_name = top_products.iloc[0]["Description"]
    best_product_revenue = top_products.iloc[0]["Revenue"]
    
    # Safely get the best month
    best_month_row = revenue_by_month.sort_values(by="Revenue", ascending=False).iloc[0]
    best_month = best_month_row["YearMonth"]
    best_month_revenue = best_month_row["Revenue"]

    st.success(f"🌟 **Top Generating Product:** {best_product_name} (${best_product_revenue:,.2f})")
    st.info(f"📅 **Most Lucrative Month:** {best_month} (${best_month_revenue:,.2f})")
    
    if selected_country == "All":
        best_country_name = top_countries.iloc[0]["Country"]
        st.warning(f"🌍 **Highest Revenue Country:** {best_country_name}")
else:
    st.write("No data available for the selected filters.")

st.divider()

# ========================================
# STEP 6: DATA TABLE
# ========================================
st.markdown("### 🔍 Raw Dataset Explorer")
st.write("Explore the cleaned dataset used for this analysis. (Note: Cancelled orders and missing prices/quantities were removed during the cleaning phase).")
st.dataframe(filtered_df)
