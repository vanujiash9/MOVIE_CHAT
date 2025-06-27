# src/scripts/download_models.py (Phiên bản đã sửa lỗi)

import os
import yaml
from huggingface_hub import snapshot_download

def download_models():
    """
    Tải cả embedding model và LLM từ Hugging Face Hub về các thư mục cục bộ
    được định nghĩa trong config.yaml.
    """
    config_path = 'config/config.yaml'
    
    # 1. Tải cấu hình
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ LỖI: Không tìm thấy file '{config_path}'.")
        return

    models_config = config.get('models', {})
    
    # === SỬA LỖI Ở ĐÂY: Dùng đúng tên key từ file config ===
    embedding_repo_id = models_config.get('embedding_repo_id')
    llm_repo_id = models_config.get('llm_repo_id')
    # ====================================================

    embedding_local_path = models_config.get('embedding_local_path')
    llm_local_path = models_config.get('llm_local_path')

    # 2. Tải Embedding Model
    if embedding_repo_id and embedding_local_path:
        print(f"\n--- Đang tải Embedding Model: {embedding_repo_id} ---")
        os.makedirs(embedding_local_path, exist_ok=True)
        snapshot_download(
            repo_id=embedding_repo_id, # Dùng biến đã sửa
            local_dir=embedding_local_path
        )
        print(f"✅ Đã tải xong Embedding Model vào '{embedding_local_path}'")
    else:
        print("⚠️ Không có thông tin 'embedding_repo_id' trong config, bỏ qua.")

    # 3. Tải LLM
    if llm_repo_id and llm_local_path:
        print(f"\n--- Đang tải LLM: {llm_repo_id} ---")
        print("Quá trình này có thể mất thời gian, vui lòng chờ...")
        os.makedirs(llm_local_path, exist_ok=True)
        snapshot_download(
            repo_id=llm_repo_id, # Dùng biến đã sửa
            local_dir=llm_local_path
        )
        print(f"✅ Đã tải xong LLM vào '{llm_local_path}'")
    else:
        print("⚠️ Không có thông tin 'llm_repo_id' trong config, bỏ qua.")


if __name__ == "__main__":
    print("===== BẮT ĐẦU QUÁ TRÌNH TẢI MODELS =====")
    download_models()
    print("\n===== KẾT THÚC QUÁ TRÌNH TẢI MODELS =====")