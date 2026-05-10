import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang Dashboard
st.set_page_config(page_title="Superstore Analytics - Tuần 5", layout="wide")
st.title("📊 Dashboard Quản trị Kinh doanh - Phiên bản Hoàn thiện")

# Đọc dữ liệu
df = pd.read_csv('SampleSuperstore.csv')

# --- THANH BÊN (SIDEBAR) ---
st.sidebar.header("Bộ lọc Dữ liệu")
# Bộ lọc Vùng miền
region = st.sidebar.multiselect(
    "Chọn Vùng (Region):", 
    options=df['Region'].unique(), 
    default=df['Region'].unique()
)
# Bộ lọc Phân khúc khách hàng (Cải tiến theo phản hồi người dùng)
segment = st.sidebar.multiselect(
    "Chọn Phân khúc (Segment):", 
    options=df['Segment'].unique(), 
    default=df['Segment'].unique()
)

# Lọc dữ liệu theo lựa chọn
filtered_df = df[df['Region'].isin(region) & df['Segment'].isin(segment)]

# --- NỘI DUNG CHÍNH ---
col1, col2 = st.columns([2, 1])

with col1:
    # 1. BIỂU ĐỒ ĐỊA LÝ (Bắt buộc)
    st.subheader("📍 Bản đồ Lợi nhuận theo Tiểu bang (USA)")
    state_data = filtered_df.groupby('State')['Profit'].sum().reset_index()
    fig_map = px.choropleth(
        state_data, 
        locations='State', 
        locationmode="USA-states", 
        color='Profit', 
        scope="usa", 
        color_continuous_scale="RdYlGn", # Đỏ (Lỗ) - Vàng - Xanh (Lãi)
        title="Phân bố Lợi nhuận theo khu vực địa lý"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    # 2. BIỂU ĐỒ DOANH THU (Đã sắp xếp theo yêu cầu người dùng)
    st.subheader("📦 Doanh thu theo Danh mục")
    cat_data = filtered_df.groupby('Category')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
    fig_bar = px.bar(
        cat_data, 
        x='Category', 
        y='Sales', 
        color='Category',
        text_auto='.2s',
        title="Tổng doanh thu từng ngành hàng"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 3. PHÂN TÍCH DATA STORY
st.divider()
st.subheader("💡 Câu chuyện dữ liệu (Data Story)")
st.info("""
**Vấn đề:** Các bang thuộc khu vực 'Central' (như Texas) đang có mức lợi nhuận âm nặng nhất dù doanh thu rất cao.  
**Nguyên nhân:** Tỷ lệ chiết khấu (Discount) trung bình tại đây vượt ngưỡng 35%.  
**Khuyến nghị:** Cần thắt chặt chính sách khuyến mãi và đặt trần chiết khấu 15% để bảo vệ lợi nhuận biên.
""")
