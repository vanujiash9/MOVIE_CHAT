import pandas as pd
import os

def load_all_sheets_from_excel(file_path: str) -> dict[str, pd.DataFrame]:
    """Tải tất cả các sheet từ file Excel và trả về một dictionary."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")
    
    print(f"Đang tải dữ liệu từ '{file_path}'...")
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    
    # Dọn dẹp tên cột
    for sheet_name, df in all_sheets.items():
        df.columns = df.columns.str.strip()
        all_sheets[sheet_name] = df

    print(f"Đã tải {len(all_sheets)} sheet thành công.")
    return all_sheets