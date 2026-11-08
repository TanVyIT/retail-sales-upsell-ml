# 🛍️ Retail Sales & Customer VIP Prediction System
Hệ thống phân tích dữ liệu bán lẻ kết hợp Trí tuệ Nhân tạo (Machine Learning) hỗ trợ chiến lược Up-sell và nhận diện khách hàng VIP.

---

## 👥 Thành viên Nhóm
- **Tăng Tấn Vỹ** (Phát triển mô hình ML & Backend FastAPI)
- **Hiệp** (Phát triển giao diện Web Frontend & Tích hợp hệ thống)

---

## 🚀 Giới thiệu dự án
Đồ án tập trung giải quyết bài toán kinh doanh thực tế trong ngành bán lẻ dựa trên bộ dữ liệu `supermarket-sales`. Hệ thống cung cấp một giải pháp toàn diện (Full-stack Data App) gồm:
1. **Business Intelligence Dashboard:** Khám phá dữ liệu trực quan, theo dõi doanh thu, xu hướng và cơ cấu danh mục.
2. **Machine Learning Model:** Mô hình **Random Forest Classifier** dự đoán và phân loại khách hàng tiềm năng đạt độ chính xác cao (98.5%).
3. **API & Web Interface:** Kiến trúc Client-Server tách biệt giữa Backend **FastAPI** (cổng `8000`) và Frontend **Streamlit** (cổng `8501`).

---

## 🛠️ Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.10+
- **Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib
- **Backend API:** FastAPI, Uvicorn
- **Frontend UI:** Streamlit, Streamlit-Option-Menu
- **Quản lý mã nguồn:** Git & GitHub

---

## 📂 Cấu trúc Thư mục
```text
retail-sales-upsell-ml/
│
├── .streamlit/
│   └── config.toml            # File cấu hình giao diện Streamlit
├── data/
│   └── raw/                   # Chứa dataset gốc (supermarket-sales.csv)
├── models/                    # Chứa mô hình đã train (model_vip.pkl)
├── src/
│   └── api.py                 # Mã nguồn Backend FastAPI
├── ui/
│   └── app.py                 # Mã nguồn Frontend Streamlit Dashboard
├── requirements.txt           # Danh sách thư viện phụ thuộc
└── README.md                  # Tài liệu hướng dẫn dự án

## Hướng dẫn Cài đặt & Chạy Dự án
* Tạo và kích hoạt môi trường ảo
python -m venv .venv
.venv\Scripts\activate

* Cài đặt các thư viện cần thiết
pip install -r requirements.txt

*Khởi chạy hệ thống
Trạm 1: Khởi động Backend FastAPI (Cổng 8000): 
uvicorn src.api:app --reload
Trạm 2: Khởi động Frontend Streamlit (Giao diện Web - Cổng mặc định 8501): 
streamlit run ui/app.py