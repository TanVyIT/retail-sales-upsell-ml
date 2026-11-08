import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from data_loader import load_and_preprocess_data

def train_model():
    print("Đang nạp và xử lý dữ liệu...")
    X, y, encoders = load_and_preprocess_data("data/raw/supermarket_sales.csv")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Đang huấn luyện mô hình Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Đánh giá
    y_pred = model.predict(X_test)
    print("\n=== KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print(classification_report(y_test, y_pred))
    
    # Lưu file
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model_vip.pkl")
    joblib.dump(encoders, "models/encoder.pkl")
    print("-> Đã lưu mô hình thành công vào thư mục models/")

if __name__ == "__main__":
    train_model()