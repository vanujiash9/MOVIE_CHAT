import yaml
import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import sys

# Thêm thư mục gốc của dự án vào sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Import các module từ src
from src.data_utils.data_loader import load_all_sheets_from_excel
from src.data_utils.data_processor import create_knowledge_documents

def main():
    # Chuyển thư mục làm việc về gốc để đường dẫn tương đối hoạt động
    os.chdir(project_root)
    print(f"Đã chuyển thư mục làm việc về: {os.getcwd()}")

    print("\n===== BẮT ĐẦU QUÁ TRÌNH TẠO INDEX =====")
    
    config_path = 'config/config.yaml'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file '{config_path}'.")
        return

    all_data = load_all_sheets_from_excel(config['data']['excel_path'])
    anime_info_df = all_data.get(config['data']['knowledge_base_sheet'])
    if anime_info_df is None:
        raise KeyError(f"Sheet '{config['data']['knowledge_base_sheet']}' không tìm thấy.")
    knowledge_base = create_knowledge_documents(anime_info_df)
    
    embedding_model_path = config['models']['embedding_local_path']
    if not os.path.exists(embedding_model_path) or not os.listdir(embedding_model_path):
        raise FileNotFoundError(f"Thư mục model embedding trống hoặc không tồn tại tại '{embedding_model_path}'.")
        
    print(f"Đang tải model embedding từ: {embedding_model_path}...")
    model = SentenceTransformer(embedding_model_path)

    print("Đang tạo embeddings...")
    corpus = knowledge_base['knowledge'].tolist()
    embeddings = model.encode(corpus, convert_to_numpy=True, show_progress_bar=True)
    
    embeddings_np = np.asarray(embeddings).astype('float32')
    faiss.normalize_L2(embeddings_np)
    index = faiss.IndexFlatIP(embeddings_np.shape[1])
    index.add(embeddings_np)
    
    output_dir = os.path.dirname(config['data']['embeddings_path'])
    os.makedirs(output_dir, exist_ok=True)
    faiss.write_index(index, config['data']['embeddings_path'])
    print(f"Đã lưu FAISS index vào: {config['data']['embeddings_path']}")

    index_to_id = {i: int(id_val) for i, id_val in enumerate(knowledge_base['ID'])}
    with open(config['data']['index_to_id_path'], 'w', encoding='utf-8') as f:
        json.dump(index_to_id, f)
    print(f"Đã lưu bản đồ ID vào: {config['data']['index_to_id_path']}")

    print("\n===== QUÁ TRÌNH TẠO INDEX HOÀN TẤT! =====")

if __name__ == "__main__":
    main()