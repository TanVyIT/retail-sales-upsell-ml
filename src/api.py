from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Supermarket VIP Predictor API")

# Cấu hình CORS để cho phép Web của Hiệp (localhost:3000) gửi request tới
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể đổi thành ["http://localhost:3000"] để bảo mật hơn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nạp mô hình AI
model = joblib.load(os.path.join("models", "model_vip.pkl"))
encoders = joblib.load(os.path.join("models", "encoder.pkl"))

# Định nghĩa cấu trúc dữ liệu Hiệp sẽ gửi lên
class CustomerData(BaseModel):
    Hour: int
    Gender: str
    Customer_type: str
    Product_line: str
    Unit_price: float
    Quantity: int

@app.post("/api/predict")
def predict_vip(data: CustomerData):
    try:
        # Mã hóa dữ liệu
        gender_enc = encoders['Gender'].transform([data.Gender])[0]
        cust_enc = encoders['Customer type'].transform([data.Customer_type])[0]
        prod_enc = encoders['Product line'].transform([data.Product_line])[0]
        
        # Đưa vào DataFrame
        input_df = pd.DataFrame([{
            'Hour': data.Hour,
            'Gender': gender_enc,
            'Customer type': cust_enc,
            'Product line': prod_enc,
            'Unit price': data.Unit_price,
            'Quantity': data.Quantity
        }])
        
        # AI Dự đoán
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        return {
            "status": "success",
            "is_vip": int(prediction),
            "vip_probability": round(probability * 100, 2),
            "message": "Khách hàng VIP" if prediction == 1 else "Khách hàng tiêu chuẩn"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Chạy thử nghiệm file api trực tiếp (nếu cần)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)