import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("🚀 Superstore Analytics Dashboard - Tuần 5")
st.markdown("Dashboard tương tác hỗ trợ ra quyết định kinh doanh dựa trên dữ liệu SampleSuperstore.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('SampleSuperstore.csv')

df = load_data()

# Sidebar Filters
st.sidebar.header("Bộ lọc")
region = st.sidebar.multiselect("Vùng (Region)", options=df['Region'].unique(), default=df['Region'].unique())
segment = st.sidebar.multiselect("Phân khúc (Segment)", options=df['Segment'].unique(), default=df['Segment'].unique())

filtered_df = df[df['Region'].isin(region) & df['Segment'].isin(segment)]

# Key Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Tổng Doanh Thu", f"${filtered_df['Sales'].sum():,.0f}")
m2.metric("Tổng Lợi Nhuận", f"${filtered_df['Profit'].sum():,.0f}")
m3.metric("Số đơn hàng", f"{len(filtered_df):,}")

# --- BIỂU ĐỒ BẢN ĐỒ (YÊU CẦU BẮT BUỘC) ---
st.subheader("📍 Bản đồ Lợi nhuận theo Bang")
state_map = filtered_df.groupby('State')['Profit'].sum().reset_index()
fig_map = px.choropleth(
    state_map,
    locations='State',
    locationmode="USA-states",
    color='Profit',
    scope="usa",
    color_continuous_scale="RdYlGn", # Red for loss, Green for profit
    title="Phân bố Lợi nhuận theo không gian"
)
st.plotly_chart(fig_map, use_container_width=True)

# --- BIỂU ĐỒ TƯƠNG TÁC KHÁC ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Doanh thu theo Danh mục")
    fig_cat = px.bar(filtered_df.groupby('Category')['Sales'].sum().reset_index().sort_values('Sales'), 
                     x='Sales', y='Category', orientation='h', color='Category')
    st.plotly_chart(fig_cat)

with c2:
    st.subheader("📉 Mối liên hệ Discount & Profit")
    fig_scatter = px.scatter(filtered_df, x='Discount', y='Profit', color='Category', 
                             hover_data=['Sub-Category'], title="Ảnh hưởng của Chiết khấu")
    st.plotly_chart(fig_scatter)

st.info("💡 **Gợi ý từ Data Story:** Giảm chiết khấu ở các bang màu đỏ trên bản đồ để cải thiện lợi nhuận tổng thể.")
