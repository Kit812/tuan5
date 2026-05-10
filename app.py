import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang Dashboard rộng để chụp ảnh đẹp hơn
st.set_page_config(page_title="Nhóm 14 - Dashboard Tuần 5", layout="wide")

# Tựa đề chính
st.title("📊 Hệ thống Quản trị Kinh doanh Superstore - Nhóm 14")
st.markdown("---")

# 1. Đọc dữ liệu
try:
    df = pd.read_csv('SampleSuperstore.csv')
except FileNotFoundError:
    st.error("Không tìm thấy file SampleSuperstore.csv. Vui lòng kiểm tra lại thư mục!")
    st.stop()

# --- SIDEBAR: CÁC THÀNH PHẦN TƯƠNG TÁC ---
st.sidebar.header("🕹️ Bộ lọc Tương tác")
st.sidebar.info("Cải tiến: Thêm bộ lọc Segment theo yêu cầu người dùng")

region_list = st.sidebar.multiselect(
    "Chọn Vùng (Region):", 
    options=df['Region'].unique(), 
    default=df['Region'].unique()
)

segment_list = st.sidebar.multiselect(
    "Chọn Phân khúc (Segment):", 
    options=df['Segment'].unique(), 
    default=df['Segment'].unique()
)

# Lọc dữ liệu theo lựa chọn của người dùng
filtered_df = df[df['Region'].isin(region_list) & df['Segment'].isin(segment_list)]

# --- HÀNG 1: CÁC CHỈ SỐ KPI (Cải tiến theo yêu cầu người dùng B) ---
k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Tổng Doanh thu", f"${filtered_df['Sales'].sum():,.0f}", delta="Sales")
with k2:
    profit = filtered_df['Profit'].sum()
    st.metric("Tổng Lợi nhuận", f"${profit:,.0f}", delta="Profit", delta_color="normal")
with k3:
    avg_discount = filtered_df['Discount'].mean() * 100
    st.metric("Tỷ lệ Chiết khấu TB", f"{avg_discount:.1f}%", delta="-Discount", delta_color="inverse")

st.markdown("---")

# --- HÀNG 2: BIỂU ĐỒ ĐỊA LÝ VÀ BIỂU ĐỒ CỘT ---
col1, col2 = st.columns([1.6, 1])

with col1:
    # 2. BIỂU ĐỒ ĐỊA LÝ (Yêu cầu bắt buộc)
    st.subheader("📍 Bản đồ Nhiệt Lợi nhuận theo Bang")
    state_profit = filtered_df.groupby('State')['Profit'].sum().reset_index()
    
    # Sử dụng thang màu RdYlGn (Đỏ - Vàng - Xanh) theo góp ý người dùng A
    fig_map = px.choropleth(
        state_profit, 
        locations='State', 
        locationmode="USA-states", 
        color='Profit', 
        scope="usa", 
        color_continuous_scale="RdYlGn",
        title="Định vị rủi ro lợi nhuận trên không gian"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    # 3. BIỂU ĐỒ CỘT (Cải tiến sắp xếp theo yêu cầu người dùng C)
    st.subheader("📦 Doanh thu theo Danh mục")
    cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
    
    fig_bar = px.bar(
        cat_sales, 
        x='Sales', 
        y='Category', 
        orientation='h', 
        color='Category',
        text_auto='.2s',
        title="Thứ tự doanh thu ngành hàng"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- PHẦN 4: CÂU CHUYỆN DỮ LIỆU ---
st.divider()
st.subheader("💡 Câu chuyện dữ liệu & Quyết định quản trị")
if profit < 0:
    st.error(f"CẢNH BÁO: Lợi nhuận hiện tại đang âm (${profit:,.0f}).")
else:
    st.success("Tình hình lợi nhuận đang ở mức ổn định.")

st.write("""
**Phân tích chiến lược:** Qua bản đồ, chúng ta thấy **Texas** và **Ohio** đang chịu mức lỗ nặng nề nhất. 
Khi kết hợp với bộ lọc, dữ liệu cho thấy nhóm hàng **Furniture** đang bị lạm dụng chiết khấu quá cao. 
**Quyết định:** Đề xuất áp dụng mức trần chiết khấu 15% cho vùng Central để phục hồi biên lợi nhuận.
""")
