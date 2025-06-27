import os

# Sử dụng mã màu ANSI để làm cho output dễ đọc hơn
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_END = '\033[0m'

def _print_success(message):
    """In thông báo thành công màu xanh lá."""
    print(f"{C_GREEN}{message}{C_END}")

def _print_error(message):
    """In thông báo lỗi màu đỏ."""
    print(f"{C_RED}{message}{C_END}")

def _print_warning(message):
    """In cảnh báo màu vàng."""
    print(f"{C_YELLOW}{message}{C_END}")

def check_directory(model_name: str, model_path: str, required_files: list) -> bool:
    """
    Hàm chung để kiểm tra một thư mục model.

    Args:
        model_name (str): Tên của model để in ra (ví dụ: "LLM Model").
        model_path (str): Đường dẫn đến thư mục model.
        required_files (list): Danh sách các file bắt buộc phải có.

    Returns:
        bool: True nếu tất cả file đều tồn tại, ngược lại là False.
    """
    print(f"{C_BLUE}--- BẮT ĐẦU KIỂM TRA: {model_name} Tại '{model_path}' ---{C_END}")
    
    # 1. Kiểm tra sự tồn tại của thư mục chính
    if not os.path.isdir(model_path):
        _print_error(f"❌ LỖI NGHIÊM TRỌNG: Thư mục '{model_path}' không tồn tại!")
        return False

    missing_files = []
    
    # 2. Kiểm tra từng file bắt buộc
    for filename in required_files:
        file_path = os.path.join(model_path, filename)
        if os.path.exists(file_path):
            _print_success(f"  [PASS] Tìm thấy: {filename}")
        else:
            _print_error(f"  [FAIL] Thiếu file: {filename}")
            missing_files.append(filename)

    # 3. Đưa ra kết luận
    if not missing_files:
        _print_success(f"\n✅ TUYỆT VỜI! Tất cả các file cần thiết cho '{model_name}' đều ở đúng vị trí.")
        return True
    else:
        _print_error(f"\n❌ LỖI CẤU TRÚC! Thiếu {len(missing_files)} file quan trọng cho '{model_name}'.")
        _print_warning("👉 Hướng dẫn sửa lỗi: Hãy chắc chắn rằng bạn đã di chuyển tất cả các file model ra khỏi")
        _print_warning("   thư mục con (như '.cache' hoặc 'transformers') và đặt chúng trực tiếp bên trong")
        _print_warning(f"   thư mục '{model_path}'.")
        return False

def main():
    """Hàm chính để chạy tất cả các bài kiểm tra."""
    print("="*60)
    print("      SCRIPT KIỂM TRA CẤU TRÚC THƯ MỤC MODEL")
    print("="*60)

    # --- Danh sách các file bắt buộc cho mỗi model ---
    
    # Dành cho model embedding (sentence-transformers)
    embedding_required = [
        "config.json",
        "model.safetensors",
        "modules.json",
        "sentence_bert_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "vocab.txt"
    ]

    # Dành cho LLM (ví dụ: PhoGPT hoặc các model tương tự)
    # Lưu ý: Chúng ta chỉ kiểm tra file shard đầu tiên để xác nhận
    llm_required = [
        "config.json",
        "generation_config.json",
        "model.safetensors.index.json",
        "model-00001-of-00004.safetensors", # Thay đổi số shard nếu model của bạn khác
        "tokenizer.json"
    ]

    # --- Chạy kiểm tra ---
    embedding_ok = check_directory(
        model_name="Embedding Model", 
        model_path="models/embedding_model", 
        required_files=embedding_required
    )
    
    print() # In một dòng trống để ngăn cách

    llm_ok = check_directory(
        model_name="Large Language Model (LLM)", 
        model_path="models/llm_model", 
        required_files=llm_required
    )
    
    # --- Kết luận cuối cùng ---
    print("\n" + "="*60)
    if embedding_ok and llm_ok:
        _print_success("🎉 TẤT CẢ ĐÃ SẴN SÀNG! Cấu trúc thư mục model của bạn hoàn toàn chính xác.")
        _print_success("Bây giờ bạn có thể tự tin chạy 'python app.py'.")
    else:
        _print_error("🚫 KIỂM TRA THẤT BẠI! Vui lòng sửa các lỗi được báo ở trên trước khi tiếp tục.")
    print("="*60)


if __name__ == "__main__":
    main()