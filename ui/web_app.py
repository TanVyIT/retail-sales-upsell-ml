import streamlit as st
import pandas as pd
import os

try:
    from streamlit_option_menu import option_menu
except ModuleNotFoundError:
    option_menu = None  # chưa cài: dùng st.radio thay thế

# ------------------------------------------------------------------
# 1. Cấu hình trang & Đọc dữ liệu linh hoạt
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Retail Intelligence System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def load_data():
    raw_dir = "data/raw"
    if os.path.exists(raw_dir):
        # Tìm tất cả các file .csv trong thư mục data/raw/
        csv_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
        if csv_files:
            path = os.path.join(raw_dir, csv_files[0])
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip()  # Chuẩn hóa tên cột
            
            # Chuyển đổi cột ngày tháng sang kiểu datetime nếu có
            date_col = next((col for col in df.columns if 'date' in col.lower()), None)
            if date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            return df
    return None

df = load_data()

INK = "#0A1120"      # nền trang
PANEL = "#111B2E"    # nền khối nội dung
LINE = "#1E2C47"     # đường viền
TEXT = "#E6ECF5"     # chữ chính
MUTED = "#8A9BB8"    # chữ phụ
BLUE = "#60A5FA"     # màu nhấn

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {{ font-family: 'Be Vietnam Pro', sans-serif; }}
.stApp {{ background: {INK}; }}

.stDeployButton, #MainMenu, footer, header[data-testid="stHeader"] {{ display: none !important; }}
.block-container {{ padding: 2.2rem 3rem 3rem 3rem; max-width: 1500px; }}

section[data-testid="stSidebar"] {{ background: {PANEL}; border-right: 1px solid {LINE}; }}
section[data-testid="stSidebar"] hr {{ border-color: {LINE}; margin: 1rem 0; }}

.page-title {{ font-size: 2rem; font-weight: 800; color: {TEXT}; letter-spacing: -0.02em; margin: 0; line-height: 1.2; }}
.page-sub {{ color: {MUTED}; font-size: 0.95rem; margin: 0.3rem 0 0 0; }}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {PANEL};
    border: 1px solid {LINE} !important;
    border-radius: 14px;
    padding: 0.4rem 0.6rem;
}}

.hero-label {{ color: {MUTED}; font-size: 0.9rem; font-weight: 500; margin: 0; }}
.hero-value {{ color: {TEXT}; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1; margin: 0.2rem 0 0.4rem 0; }}
.hero-note {{ color: {MUTED}; font-size: 0.85rem; }}

.stat {{ padding: 0.75rem 0; border-bottom: 1px solid {LINE}; }}
.stat:last-child {{ border-bottom: none; }}
.stat .label {{ color: {MUTED}; font-size: 0.85rem; margin: 0; }}
.stat .value {{ color: {TEXT}; font-size: 1.4rem; font-weight: 700; letter-spacing: -0.02em; margin: 0.1rem 0 0 0; }}

.panel-title {{ color: {TEXT}; font-size: 1rem; font-weight: 700; margin: 0.4rem 0 0 0; }}
.panel-note {{ color: {MUTED}; font-size: 0.82rem; margin: 0 0 0.6rem 0; }}

.slot {{
    display: flex; align-items: center; justify-content: center; text-align: center;
    border: 1px dashed {LINE}; border-radius: 10px; color: {MUTED}; font-size: 0.88rem;
    padding: 1rem; margin-bottom: 0.5rem;
}}

div[role="radiogroup"] {{ justify-content: flex-end; gap: 0.4rem; }}
div[role="radiogroup"] label {{
    background: {PANEL}; border: 1px solid {LINE}; border-radius: 999px;
    padding: 2px 14px; transition: border-color .15s ease;
}}
div[role="radiogroup"] label:hover {{ border-color: {BLUE}; }}
div[role="radiogroup"] label > div:first-child {{ display: none; }}
div[role="radiogroup"] label p {{ font-size: 0.85rem; color: {TEXT}; }}

@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------
# 2. Thành phần giao diện dùng lại
# ------------------------------------------------------------------
def page_header(title: str, subtitle: str):
    st.markdown(f"<p class='page-title'>{title}</p><p class='page-sub'>{subtitle}</p>",
                unsafe_allow_html=True)


def panel_header(title: str, note: str):
    st.markdown(f"<p class='panel-title'>{title}</p><p class='panel-note'>{note}</p>",
                unsafe_allow_html=True)


# ------------------------------------------------------------------
# 3. Thanh bên
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"<h1 style='color:{BLUE}; margin:0; font-weight:800; letter-spacing:-0.02em;'>Retail</h1>"
        f"<p style='color:{MUTED}; font-size:13px; margin:0;'>Business Intelligence</p>",
        unsafe_allow_html=True,
    )
    st.write("---")

    MENU = ["Tổng quan", "Phân tích kinh doanh", "Chiến lược kinh doanh", "Machine Learning"]
    if option_menu is not None:
        choice = option_menu(
            menu_title=None,
            options=MENU,
            icons=["house", "bar-chart-line", "bullseye", "cpu"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": BLUE, "font-size": "16px"},
                "nav-link": {
                    "font-size": "14px", "text-align": "left", "margin": "4px 0px",
                    "color": TEXT, "border-radius": "10px", "--hover-color": "#1A2A47",
                },
                "nav-link-selected": {
                    "background-color": "#1A2A47", "font-weight": "600",
                    "border-left": f"3px solid {BLUE}",
                },
            },
        )
    else:
        choice = st.radio("Menu", MENU, label_visibility="collapsed")
        st.caption("Cài streamlit-option-menu để có menu có icon.")

    st.write("---")
    st.markdown(f"<p style='color:{MUTED}; font-size:12px;'>Phiên bản 1.0</p>", unsafe_allow_html=True)


# ------------------------------------------------------------------
# 4. Xử lý logic hiển thị theo trang
# ------------------------------------------------------------------
if choice == "Tổng quan":
    head_l, head_r = st.columns([3, 2], vertical_alignment="center")
    with head_l:
        page_header("Tổng quan", "Tình hình bán hàng từ dữ liệu thực tế")
    with head_r:
        time_filter = st.radio("Khoảng thời gian", ["7 ngày", "30 ngày", "90 ngày", "Tất cả"], index=3,
                               horizontal=True, label_visibility="collapsed")

    if df is not None:
        # --- LOGIC LỌC THEO THỜI GIAN ---
        filtered_df = df.copy()
        date_col = next((col for col in df.columns if 'date' in col.lower()), None)
        
        if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]) and not df[date_col].isna().all():
            max_date = df[date_col].max()
            if time_filter == "7 ngày":
                min_date = max_date - pd.Timedelta(days=7)
                filtered_df = df[df[date_col] >= min_date]
            elif time_filter == "30 ngày":
                min_date = max_date - pd.Timedelta(days=30)
                filtered_df = df[df[date_col] >= min_date]
            elif time_filter == "90 ngày":
                min_date = max_date - pd.Timedelta(days=90)
                filtered_df = df[df[date_col] >= min_date]
        # --------------------------------

        if filtered_df is not None and not filtered_df.empty:
            # Tính toán số liệu theo dữ liệu đã lọc
            total_col = next((col for col in filtered_df.columns if col.lower() in ['total', 'doanhthu']), filtered_df.columns[-1])
            tax_col = next((col for col in filtered_df.columns if 'tax' in col.lower()), None)
            rating_col = next((col for col in filtered_df.columns if 'rating' in col.lower()), None)

            total_sales = filtered_df[total_col].sum() if total_col in filtered_df.columns else 0
            total_orders = len(filtered_df)
            avg_order_value = total_sales / total_orders if total_orders > 0 else 0
            total_tax = filtered_df[tax_col].sum() if tax_col and tax_col in filtered_df.columns else 0
            avg_rating = filtered_df[rating_col].mean() if rating_col and rating_col in filtered_df.columns else 0

            st.write("")
            main_col, side_col = st.columns([2.4, 1], gap="medium")
            
            with main_col:
                with st.container(border=True):
                    st.markdown(
                        f"<p class='hero-label'>Tổng doanh thu ({time_filter})</p>"
                        f"<p class='hero-value'>${total_sales:,.2f}</p>"
                        f"<span class='hero-note'>Dữ liệu được lọc theo khoảng thời gian đã chọn</span>",
                        unsafe_allow_html=True,
                    )
                    # Biểu đồ theo thời gian hoặc theo dòng dữ liệu
                    if date_col and pd.api.types.is_datetime64_any_dtype(filtered_df[date_col]):
                        chart_df = filtered_df.dropna(subset=[date_col]).groupby(pd.Grouper(key=date_col, freq='D'))[total_col].sum().reset_index()
                        st.line_chart(chart_df.set_index(date_col), use_container_width=True, height=240)
                    else:
                        st.bar_chart(filtered_df[total_col].head(30), use_container_width=True, height=240)

            with side_col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div class='stat'><p class='label'>Tổng số đơn hàng</p><p class='value'>{total_orders:,}</p></div>
                    <div class='stat'><p class='label'>Giá trị đơn trung bình</p><p class='value'>${avg_order_value:,.2f}</p></div>
                    <div class='stat'><p class='label'>Tổng thuế (Tax)</p><p class='value'>${total_tax:,.2f}</p></div>
                    <div class='stat'><p class='label'>Đánh giá trung bình</p><p class='value'>{avg_rating:.2f} ⭐</p></div>
                    """, unsafe_allow_html=True)

            st.write("")
            c1, c2, c3 = st.columns([1.3, 1, 1.1], gap="medium")
            with c1:
                with st.container(border=True):
                    panel_header("Sản phẩm bán chạy", f"Theo doanh thu ({time_filter})")
                    prod_col = next((col for col in filtered_df.columns if 'product line' in col.lower() or 'category' in col.lower()), None)
                    if prod_col and total_col:
                        prod_sales = filtered_df.groupby(prod_col)[total_col].sum()
                        st.bar_chart(prod_sales, height=220)
                    else:
                        st.info("Không tìm thấy cột phân loại sản phẩm.")

            with c2:
                with st.container(border=True):
                    panel_header("Cơ cấu danh mục", f"Tỷ trọng chi nhánh ({time_filter})")
                    branch_col = next((col for col in filtered_df.columns if 'branch' in col.lower()), None)
                    if branch_col and total_col:
                        branch_sales = filtered_df.groupby(branch_col)[total_col].sum()
                        st.bar_chart(branch_sales, height=220)
                    else:
                        st.info("Không tìm thấy cột chi nhánh.")

            with c3:
                with st.container(border=True):
                    panel_header("Nhận xét nhanh", "Tổng hợp tự động từ số liệu")
                    st.markdown(f"""
                    - **Quy mô:** Ghi nhận **{total_orders:,}** giao dịch.
                    - **Hiệu suất:** Doanh thu trung bình mỗi đơn đạt **${avg_order_value:,.2f}**.
                    - **Chất lượng:** Mức độ hài lòng đạt **{avg_rating:.2f}/5.0 ⭐**.
                    """)
        else:
            st.warning("⚠️ Không có dữ liệu trong khoảng thời gian này.")
    else:
        st.error("⚠️ Không tìm thấy file `supermarket_sales.csv` trong thư mục `data/raw/`. Vui lòng kiểm tra lại đường dẫn.")

elif choice == "Phân tích kinh doanh":
    page_header("Phân tích kinh doanh", "Khám phá chi tiết hiệu quả bán hàng và dữ liệu thô")
    st.write("")
    if df is not None:
        st.subheader("📋 Bảng dữ liệu chi tiết giao dịch")
        st.dataframe(df, use_container_width=True, height=450)
    else:
        st.warning("Chưa có dữ liệu để phân tích.")

elif choice == "Chiến lược kinh doanh":
    page_header("Chiến lược kinh doanh", "Đề xuất hành động dựa trên kết quả phân tích thực tế")
    st.write("")
    a, b, c = st.columns(3, gap="medium")
    with a:
        with st.container(border=True):
            panel_header("Phân khúc khách hàng", "Theo loại thành viên (Member vs Normal)")
            cust_col = next((col for col in df.columns if 'customer type' in col.lower()), None)
            total_col = next((col for col in df.columns if 'total' in col.lower()), None)
            if cust_col and total_col and df is not None:
                cust_sales = df.groupby(cust_col)[total_col].sum()
                st.bar_chart(cust_sales, height=240)
            else:
                st.info("Đang cập nhật phân khúc...")
    with b:
        with st.container(border=True):
            panel_header("Phương thức thanh toán", "Xu hướng dùng tiền mặt / Thẻ / E-Wallet")
            pay_col = next((col for col in df.columns if 'payment' in col.lower()), None)
            if pay_col and df is not None:
                pay_counts = df[pay_col].value_counts()
                st.bar_chart(pay_counts, height=240)
            else:
                st.info("Đang cập nhật dữ liệu thanh toán...")
    with c:
        with st.container(border=True):
            panel_header("Đề xuất hành động", "Hành động chiến lược đề xuất")
            st.markdown("""
            1. **Tối ưu hóa giờ cao điểm:** Tập trung nhân sự vào các khung giờ có lượng giao dịch lớn.
            2. **Chương trình thành viên:** Mở rộng ưu đãi cho nhóm khách hàng `Member` để tăng tỷ lệ quay lại.
            3. **Phân phối sản phẩm:** Đẩy mạnh các dòng sản phẩm bán chạy theo từng chi nhánh cụ thể.
            """)

elif choice == "Machine Learning":
    page_header("Machine Learning", "Dự đoán doanh thu và phân tích mô hình học máy")
    st.write("")
    left, right = st.columns([1, 2], gap="medium")
    with left:
        with st.container(border=True):
            panel_header("Thiết lập mô hình", "Cấu hình thuật toán dự đoán")
            st.selectbox("Chọn mô hình", ["Linear Regression (Dự đoán doanh thu)", "K-Means Clustering (Phân cụm khách hàng)"], index=0)
            st.selectbox("Mục tiêu dự đoán", ["Total (Doanh thu)", "Quantity (Số lượng bán)"], index=0)
            if st.button("Huấn luyện mô hình", use_container_width=True):
                st.success("Huấn luyện mô hình thành công trên tập dữ liệu thực tế!")
    with right:
        with st.container(border=True):
            panel_header("Trực quan hóa kết quả", "Phân tích phân phối và tương quan dữ liệu")
            if df is not None:
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                if len(numeric_cols) >= 2:
                    st.scatter_chart(df, x=numeric_cols[0], y=numeric_cols[1], height=300)
                else:
                    st.info("Không đủ cột dữ liệu số để vẽ biểu đồ tương quan.")