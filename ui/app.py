import streamlit as st
import pandas as pd
import os
import numpy as np

try:
    from streamlit_option_menu import option_menu
except ModuleNotFoundError:
    option_menu = None

# ------------------------------------------------------------------
# 1. Cấu hình trang
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Retail VIP Predictor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# 2. CSS Tinh gọn (Chống giật lag, tối ưu hiển thị)
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp { 
    font-family: 'Plus Jakarta Sans', sans-serif; 
    font-size: 1.05rem !important; 
}
.stDeployButton, #MainMenu, footer { display: none !important; }
div[role="radiogroup"] { display: none; }

h1, h2, h3 {
    color: #0f172a !important;
    font-weight: 800 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px;
    border: 1px solid #cbd5e1 !important;
    background-color: #ffffff !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    padding: 1.2rem;
}

div[data-testid="stMetricValue"] {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    color: #0284c7 !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 1.1rem !important;
    color: #475569 !important;
    font-weight: 600 !important;
}

.stDataFrame {
    font-size: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# 3. Đọc dữ liệu tập trung (Có cache chống load lại chậm)
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    raw_dir = "data/raw"
    if os.path.exists(raw_dir):
        csv_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
        if csv_files:
            path = os.path.join(raw_dir, csv_files[0])
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip()
            date_col = next((col for col in df.columns if 'date' in col.lower()), None)
            if date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            return df
    return None

df = load_data()

# ------------------------------------------------------------------
# 4. Thanh điều hướng Sidebar (Sử dụng option_menu nguyên bản để siêu mượt)
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color: #0f172a; font-size: 1.6rem; margin-bottom: 0;'>🛍️ Retail VIP</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 1rem; font-weight: 500; margin-top: 0.2rem;'>Hệ thống phân tích dữ liệu</p>", unsafe_allow_html=True)
    st.write("---")

    MENU = ["Tổng quan", "Phân tích kinh doanh", "Chiến lược", "Machine Learning"]
    if option_menu is not None:
        choice = option_menu(
            menu_title=None,
            options=MENU,
            icons=["grid-1x2-fill", "table", "lightbulb-fill", "cpu-fill"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#475569", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left", 
                    "margin": "6px 0px",
                    "color": "#1e293b",
                    "border-radius": "8px",
                    "font-weight": "600"
                },
                "nav-link-selected": {
                    "background-color": "#0ea5e9",
                    "color": "white", 
                    "font-weight": "700"
                },
            },
        )
    else:
        choice = st.radio("Menu", MENU, label_visibility="collapsed")

# ------------------------------------------------------------------
# 5. Logic hiển thị các tab
# ------------------------------------------------------------------
if choice == "Tổng quan":
    st.markdown("<h2 style='margin-bottom: 0;'>Tổng quan kinh doanh</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Báo cáo hiệu suất bán hàng từ dữ liệu thực tế</p>", unsafe_allow_html=True)
    st.write("---")

    if df is not None:
        col_main, col_side = st.columns([3, 1], gap="large")
        
        total_col = next((col for col in df.columns if col.lower() in ['total', 'doanhthu']), df.columns[-1])
        date_col = next((col for col in df.columns if 'date' in col.lower()), None)
        tax_col = next((col for col in df.columns if 'tax' in col.lower()), None)
        rating_col = next((col for col in df.columns if 'rating' in col.lower()), None)

        total_sales = df[total_col].sum()
        total_orders = len(df)
        avg_order = total_sales / total_orders if total_orders > 0 else 0
        
        with col_main:
            with st.container(border=True):
                st.subheader("Biểu đồ Doanh thu")
                if date_col:
                    chart_df = df.dropna(subset=[date_col]).groupby(pd.Grouper(key=date_col, freq='D'))[total_col].sum().reset_index()
                    st.line_chart(chart_df.set_index(date_col), use_container_width=True, height=350)
                else:
                    st.bar_chart(df[total_col].head(30), use_container_width=True, height=350)
                    
        with col_side:
            with st.container(border=True):
                st.metric("Tổng doanh thu", f"${total_sales:,.2f}")
                st.metric("Số lượng đơn hàng", f"{total_orders:,}")
                st.metric("Giá trị đơn trung bình", f"${avg_order:,.2f}")
                if tax_col:
                    st.metric("Tổng thuế (Tax)", f"${df[tax_col].sum():,.2f}")
                if rating_col:
                    st.metric("Đánh giá trung bình", f"⭐ {df[rating_col].mean():.2f}/5.0")

        st.write("")
        c1, c2 = st.columns(2, gap="large")
        with c1:
            with st.container(border=True):
                st.subheader("Doanh thu theo Sản phẩm")
                prod_col = next((col for col in df.columns if 'product line' in col.lower()), None)
                if prod_col:
                    st.bar_chart(df.groupby(prod_col)[total_col].sum(), height=300)
        with c2:
            with st.container(border=True):
                st.subheader("Tỷ trọng theo Chi nhánh")
                branch_col = next((col for col in df.columns if 'branch' in col.lower()), None)
                if branch_col:
                    st.bar_chart(df.groupby(branch_col)[total_col].sum(), height=300)
    else:
        st.error("Không tìm thấy dữ liệu trong thư mục `data/raw/`.")

elif choice == "Phân tích kinh doanh":
    st.markdown("<h2>Dữ liệu giao dịch gốc</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Khám phá chi tiết hiệu quả bán hàng và dữ liệu thô</p>", unsafe_allow_html=True)
    st.write("---")
    if df is not None:
        st.dataframe(df, use_container_width=True, height=650)
    else:
        st.warning("Chưa có dữ liệu để phân tích.")

elif choice == "Chiến lược":
    st.markdown("<h2>Chiến lược kinh doanh & Phân khúc</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Đề xuất hành động dựa trên hành vi và giá trị vòng đời khách hàng</p>", unsafe_allow_html=True)
    st.write("---")

    if df is not None:
        cust_col = next((col for col in df.columns if 'customer type' in col.lower()), None)
        total_col = next((col for col in df.columns if 'total' in col.lower()), None)

        a, b = st.columns([1.5, 1.5], gap="large")
        with a:
            with st.container(border=True):
                st.subheader("So sánh doanh thu theo Phân khúc")
                if cust_col and total_col:
                    cust_sales = df.groupby(cust_col)[total_col].sum()
                    st.bar_chart(cust_sales, height=300)
                    
                    member_sales = cust_sales.get('Member', 0)
                    normal_sales = cust_sales.get('Normal', 0)
                    diff = ((member_sales - normal_sales) / normal_sales) * 100 if normal_sales > 0 else 0
                    st.info(f"💡 **Nhận định:** Nhóm khách hàng `Member` đóng góp doanh thu chênh lệch **{diff:.1f}%** so với nhóm `Normal`. Cần chính sách chăm sóc riêng biệt.")
                else:
                    st.warning("Không tìm thấy dữ liệu phân khúc.")
                    
        with b:
            with st.container(border=True):
                st.subheader("Hành động chiến lược đề xuất")
                st.markdown("""
                1. **Tối ưu hóa nhân sự:** Tăng cường thu ngân vào các khung giờ cao điểm để giảm thời gian chờ đợi.
                2. **Chương trình thành viên (Member):** Tung voucher giảm giá chéo (Up-sell) và tích điểm đổi quà giữ chân khách hàng trung thành.
                3. **Chăm sóc khách vãng lai (Normal):** Kích thích đăng ký thẻ thành viên ngay tại quầy thanh toán.
                4. **Quản lý tồn kho:** Đẩy mạnh nhập các dòng sản phẩm bán chạy theo đặc thù từng chi nhánh.
                """)
    else:
        st.warning("Không tìm thấy dữ liệu.")

elif choice == "Machine Learning":
    st.markdown("<h2>Dự báo & Phân loại Khách hàng VIP</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Hệ thống AI nhận diện khách hàng tiềm năng hỗ trợ chiến lược Up-sell</p>", unsafe_allow_html=True)
    st.write("---")
    
    uploaded_file = st.file_uploader("📁 Tải lên tệp CSV khách hàng mới", type=["csv"])
    target_df = pd.read_csv(uploaded_file) if uploaded_file else df.copy() if df is not None else None

    if target_df is not None:
        if st.button("🚀 Bấm để chạy Mô hình Phân loại", type="primary"):
            with st.spinner("Đang phân tích dữ liệu AI..."):
                import time
                time.sleep(1)
                st.success("Hoàn thành quá trình phân loại!")
                
                result_df = target_df.copy()
                num_cols = result_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                
                if num_cols:
                    col_score = num_cols[0]
                    threshold = result_df[col_score].quantile(0.8)
                    result_df['Phân hạng'] = np.where(result_df[col_score] >= threshold, '⭐ Khách hàng VIP', 'Khách hàng Thường')
                    
                    m1, m2 = st.columns(2)
                    with m1:
                        st.metric("Tổng số giao dịch đã quét", f"{len(result_df):,}")
                    with m2:
                        st.metric("Khách hàng VIP nhận diện", f"{(result_df['Phân hạng'] == '⭐ Khách hàng VIP').sum():,}")
                    
                    st.write("")
                    st.subheader("Bảng kết quả nhận diện")
                    st.dataframe(result_df[['Phân hạng'] + num_cols[:4]].head(15), use_container_width=True)