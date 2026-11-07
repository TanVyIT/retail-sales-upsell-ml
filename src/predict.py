import joblib
import pandas as pd
import os

def load_models():
    # Nạp mô hình và bộ mã hóa từ thư mục models/
    model = joblib.load(os.path.join("models", "model_vip.pkl"))
    encoders = joblib.load(os.path.join("models", "encoder.pkl"))
    return model, encoders

def predict_single(hour, gender, customer_type, product_line, unit_price, quantity):
    model, encoders = load_models()
    
    # Mã hóa dữ liệu chuỗi thành số
    gender_enc = encoders['Gender'].transform([gender])[0]
    cust_enc = encoders['Customer type'].transform([customer_type])[0]
    prod_enc = encoders['Product line'].transform([product_line])[0]
    
    input_data = pd.DataFrame([{
        'Hour': int(hour),
        'Gender': gender_enc,
        'Customer type': cust_enc,
        'Product line': prod_enc,
        'Unit price': float(unit_price),
        'Quantity': int(quantity)
    }])
    
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    return prediction, probability

def predict_batch(filepath):
    model, encoders = load_models()
    df = pd.read_csv(filepath)
    
    # Xử lý giờ tương tự như lúc train
    if 'Time' in df.columns:
        df['Hour'] = pd.to_datetime(df['Time']).dt.hour
    else:
        raise ValueError("File CSV thiếu cột 'Time'")
        
    # Mã hóa
    for col in ['Gender', 'Customer type', 'Product line']:
        if col in df.columns:
            df[col] = encoders[col].transform(df[col])
        else:
            raise ValueError(f"File CSV thiếu cột '{col}'")
            
    # Dự đoán
    feature_cols = ['Hour', 'Gender', 'Customer type', 'Product line', 'Unit price', 'Quantity']
    predictions = model.predict(df[feature_cols])
    
    # Giải mã lại các cột chữ để xuất báo cáo cho Giám đốc dễ đọc
    for col in ['Gender', 'Customer type', 'Product line']:
        df[col] = encoders[col].inverse_transform(df[col])
        
    # Thêm cột kết quả
    df['Is_VIP_Predict'] = predictions
    df['VIP_Status'] = df['Is_VIP_Predict'].apply(lambda x: "VIP" if x == 1 else "Normal")
    
    # Xuất file kết quả
    output_path = filepath.replace(".csv", "_VIP_Report.csv")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    vip_count = sum(predictions)
    total_count = len(predictions)
    return output_path, vip_count, total_count