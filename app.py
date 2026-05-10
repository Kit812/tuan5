import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình Dashboard
st.set_page_config(page_title="Kit Shop - Superstore Analytics", layout="wide")
st.title("🚀 Dashboard Hoàn thiện - Tuần 5")

# 1. Đọc dữ liệu
df = pd.read_csv('SampleSuperstore.csv')

# 2. Bộ lọc tương tác (Slicers) - Đáp ứng phản hồi người dùng
st.sidebar.header("Bộ lọc dữ liệu")
regions = st.sidebar.multiselect("Chọn vùng:", df['Region'].unique(), default=df['Region'].unique())
segments = st.sidebar.multiselect("Phân khúc khách hàng:", df['Segment'].unique(), default=df['Segment'].unique())

filtered_df = df[df['Region'].isin(regions) & df['Segment'].isin(segments)]

# 3. Biểu đồ bản đồ (Yêu cầu bắt buộc)
st.subheader("📍 Bản đồ Lợi nhuận theo Bang (USA)")
state_map = filtered_df.groupby('State')['Profit'].sum().reset_index()
fig_map = px.choropleth(
    state_map,
    locations='State', locationmode="USA-states",
    color='Profit', scope="usa",
    color_continuous_scale="RdYlGn", # Thang màu Đỏ-Xanh theo góp ý người dùng
    title="Lợi nhuận phân bố theo địa lý"
)
st.plotly_chart(fig_map, use_container_width=True)

# 4. Biểu đồ doanh thu (Đã sắp xếp)
st.subheader("📊 Doanh thu theo Danh mục sản phẩm")
cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
fig_bar = px.bar(cat_sales, x='Sales', y='Category', orientation='h', color='Category', 
                 title="Doanh thu được sắp xếp giảm dần")
st.plotly_chart(fig_bar, use_container_width=True)

st.success("💡 **Data Story:** Giảm chiết khấu tại khu vực miền Trung (vùng màu đỏ trên bản đồ) để cứu vãn lợi nhuận.")
