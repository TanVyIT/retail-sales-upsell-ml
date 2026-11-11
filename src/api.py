from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import io

app = FastAPI(title="Supermarket VIP Predictor API")

# 1. Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Nạp mô hình AI & Encoders
MODEL_PATH = os.path.join("models", "model_vip.pkl")
ENCODER_PATH = os.path.join("models", "encoder.pkl")

model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
encoders = joblib.load(ENCODER_PATH) if os.path.exists(ENCODER_PATH) else None

# Định nghĩa cấu trúc dữ liệu JSON (cho request 1 khách hàng)
class CustomerData(BaseModel):
    Hour: int
    Gender: str
    Customer_type: str
    Product_line: str
    Unit_price: float
    Quantity: int

@app.get("/")
def root():
    return {"status": "online", "message": "API Supermarket VIP Predictor đang hoạt động"}

# ------------------------------------------------------------------
# Endpoint 1: Dự đoán 1 khách hàng đơn lẻ (Dạng JSON)
# ------------------------------------------------------------------
@app.post("/api/predict")
def predict_vip(data: CustomerData):
    if not model or not encoders:
        return {"status": "error", "message": "Chưa nạp được model hoặc encoder"}
    try:
        # Mã hóa dữ liệu theo encoder gốc
        gender_enc = encoders['Gender'].transform([data.Gender])[0]
        cust_enc = encoders['Customer type'].transform([data.Customer_type])[0]
        prod_enc = encoders['Product line'].transform([data.Product_line])[0]
        
        input_df = pd.DataFrame([{
            'Hour': data.Hour,
            'Gender': gender_enc,
            'Customer type': cust_enc,
            'Product line': prod_enc,
            'Unit price': data.Unit_price,
            'Quantity': data.Quantity
        }])
        
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

# ------------------------------------------------------------------
# Endpoint 2: Dự đoán hàng loạt từ file CSV (Dành riêng cho Streamlit)
# ------------------------------------------------------------------
@app.post("/api/predict-csv")
async def predict_csv(file: UploadFile = File(...)):
    if not model or not encoders:
        raise HTTPException(status_code=500, detail="Chưa nạp được model_vip.pkl hoặc encoder.pkl trong thư mục models/")
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        df.columns = df.columns.str.strip()
        
        processed_df = pd.DataFrame()
        
        # Xử lý cột Hour
        if 'Hour' in df.columns:
            processed_df['Hour'] = df['Hour']
        elif 'Time' in df.columns:
            processed_df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').dt.hour.fillna(12).astype(int)
        else:
            processed_df['Hour'] = 12

        # Encode các thuộc tính
        processed_df['Gender'] = encoders['Gender'].transform(df['Gender'].astype(str)) if 'Gender' in df.columns else 0
        processed_df['Customer type'] = encoders['Customer type'].transform(df['Customer type'].astype(str)) if 'Customer type' in df.columns else 0
        processed_df['Product line'] = encoders['Product line'].transform(df['Product line'].astype(str)) if 'Product line' in df.columns else 0
        processed_df['Unit price'] = df['Unit price'] if 'Unit price' in df.columns else 0
        processed_df['Quantity'] = df['Quantity'] if 'Quantity' in df.columns else 1

        # Dự đoán bằng AI model thật
        predictions = model.predict(processed_df)
        probabilities = model.predict_proba(processed_df)[:, 1]
        
        df['Prediction'] = predictions
        df['VIP_Probability'] = (probabilities * 100).round(2)
        df['Phân hạng'] = df['Prediction'].apply(lambda x: '⭐ Khách hàng VIP' if x == 1 else 'Khách hàng Thường')
        
        return {
            "status": "success",
            "total_records": len(df),
            "vip_count": int((df['Prediction'] == 1).sum()),
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý CSV: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)