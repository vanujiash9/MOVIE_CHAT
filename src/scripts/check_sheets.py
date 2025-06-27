# scripts/check_sheets.py
import pandas as pd
import yaml
import os

def check_excel_sheets():
    """
    Script tiện ích để đọc và liệt kê tất cả các tên sheet từ file Excel
    được chỉ định trong config.
    """
    config_path = 'config/config.yaml'
    
    # --- Tải cấu hình ---
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file cấu hình tại '{config_path}'.")
        print("Vui lòng đảm bảo bạn đang chạy script từ thư mục gốc của dự án.")
        return

    excel_file_path = config.get('data', {}).get('excel_path')
    if not excel_file_path:
        print("LỖI: Không tìm thấy 'excel_path' trong file config.yaml.")
        return

    # --- Kiểm tra và đọc file Excel ---
    try:
        # Sử dụng pd.ExcelFile để chỉ lấy tên sheet mà không cần tải toàn bộ dữ liệu
        xls = pd.ExcelFile(excel_file_path)
        sheet_names = xls.sheet_names
        
        print("="*50)
        print(f"ĐÃ TÌM THẤY CÁC SHEET SAU TRONG FILE '{excel_file_path}':")
        print("="*50)
        
        # In ra từng tên sheet
        for name in sheet_names:
            print(f"- '{name}'")
            
        print("\n" + "="*50)
        print("HƯỚNG DẪN:")
        print("1. So sánh danh sách trên với các giá trị bạn đã khai báo trong 'config/config.yaml'.")
        print("   Ví dụ: knowledge_base_sheet, recommendations_sheet, ...")
        print("2. Đảm bảo tên trong file config.yaml PHẢI TRÙNG KHỚP 100% với tên sheet ở trên.")
        print("3. Nếu có sai lệch, hãy sao chép (copy) tên chính xác từ đây và dán (paste) vào file config.yaml.")
        print("="*50)

    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file Excel tại đường dẫn '{excel_file_path}'.")
        print("Vui lòng kiểm tra lại giá trị 'excel_path' trong file config.yaml.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi đọc file Excel: {e}")

if __name__ == "__main__":
    check_excel_sheets()