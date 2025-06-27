# src/core/retriever.py
import faiss
import json
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from typing import Dict, List

class AnimeRetriever:
    def __init__(self, config: Dict):
        """
        Khởi tạo hệ thống truy xuất thông tin (Retriever) sử dụng FAISS và SentenceTransformer.

        Args:
            config (Dict): Dictionary cấu hình chung của ứng dụng.
        """
        print("[*] Đang khởi tạo Retriever...")
        self.config = config
        self.model_path = self.config['models']['embedding_local_path']
        self.index_path = self.config['data']['embeddings_path']
        self.id_map_path = self.config['data']['index_to_id_path']
        self.top_k = self.config['retriever']['top_k']
        
        self._load_resources()
        print("✅ Retriever đã sẵn sàng.")

    def _load_resources(self):
        """Tải các tài nguyên cần thiết: model embedding, FAISS index, và ID map."""
        # 1. Tải model embedding
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"LỖI: Model embedding không tồn tại tại '{self.model_path}'. Vui lòng chạy 'scripts/download_models.py'.")
        print(f"    - Đang tải model embedding từ '{self.model_path}'...")
        self.model = SentenceTransformer(self.model_path)
        
        # 2. Tải FAISS index
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"LỖI: FAISS index không tồn tại tại '{self.index_path}'. Vui lòng chạy 'scripts/build_index.py'.")
        print(f"    - Đang tải FAISS index từ '{self.index_path}'...")
        self.index = faiss.read_index(self.index_path)

        # 3. Tải bản đồ từ index sang ID
        if not os.path.exists(self.id_map_path):
            raise FileNotFoundError(f"LỖI: File ID map không tồn tại tại '{self.id_map_path}'. Vui lòng chạy 'scripts/build_index.py'.")
        with open(self.id_map_path, 'r', encoding='utf-8') as f:
            self.id_map = {int(k): v for k, v in json.load(f).items()}
        
    def search(self, query: str) -> List[int]:
        """
        Tìm kiếm các ID anime liên quan nhất đến một câu hỏi.

        Args:
            query (str): Câu hỏi của người dùng.

        Returns:
            List[int]: Danh sách các ID anime được truy xuất.
        """
        try:
            # Tạo vector cho câu hỏi
            query_vector = self.model.encode([query], convert_to_numpy=True)
            
            # Chuẩn hóa vector (quan trọng với IndexFlatIP)
            faiss.normalize_L2(query_vector)
            
            # Tìm kiếm trong index
            _, indices = self.index.search(query_vector.astype(np.float32), self.top_k)
            
            # Ánh xạ từ index của FAISS về ID thật của anime
            retrieved_ids = [self.id_map[i] for i in indices[0] if i != -1 and i in self.id_map]
            
            print(f"    - [Retriever] Đã truy xuất các ID: {retrieved_ids} cho câu hỏi '{query[:50]}...'")
            return retrieved_ids
        except Exception as e:
            print(f"Lỗi trong quá trình tìm kiếm của Retriever: {e}")
            return []