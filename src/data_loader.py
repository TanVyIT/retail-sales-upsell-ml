import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data(filepath="data/raw/supermarket_sales.csv"):
    df = pd.read_csv(filepath)

    # 1. Tạo biến mục tiêu Is_VIP: 1 nếu đơn hàng lớn hơn trung bình, 0 nếu ngược lại
    mean_total = df['Sales'].mean()
    df['Is_VIP'] = (df['Sales'] > mean_total).astype(int)
    
    # 2. Rút trích giờ từ cột Time (định dạng HH:MM)
    df['Hour'] = pd.to_datetime(df['Time']).dt.hour
    
    feature_cols = ['Hour', 'Gender', 'Customer type', 'Product line', 'Unit price', 'Quantity']
    
    # 3. Mã hóa LabelEncoder cho các thuộc tính dạng chuỗi
    encoders = {}
    for col in ['Gender', 'Customer type', 'Product line']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    X = df[feature_cols]
    y = df['Is_VIP']
    
    return X, y, encoders