# src/chat_bot.py
import yaml
import json
import pandas as pd
import os
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

# Sử dụng import tương đối để code sạch hơn
from .data_utils.data_loader import load_all_sheets_from_excel
from .core.retriever import AnimeRetriever
from .core.model_handler import LLMHandler
from .core.prompt_manager import create_rag_prompt, create_direct_answer_prompt, create_general_prompt

class Chatbot:
    def __init__(self, config_path: str, model_config_path: str):
        print("\n" + "="*50)
        print("🤖 BẮT ĐẦU KHỞI TẠO ANIBOT 🤖")
        print("="*50)
        
        with open(config_path, 'r', encoding='utf-8') as f: self.config = yaml.safe_load(f)
        with open(model_config_path, 'r', encoding='utf-8') as f: self.model_config = json.load(f)

        self._load_data_sources()
        
        self.retriever = AnimeRetriever(self.config)
        self.llm_handler = LLMHandler(
            model_path=self.config['models']['llm_local_path'], 
            model_config=self.model_config['llm_params']
        )
        print("\n" + "="*50)
        print("✨ AniBot đã khởi tạo thành công và sẵn sàng phục vụ! ✨")
        print("="*50 + "\n")

    def _load_data_sources(self):
        """Tải tất cả dữ liệu từ file Excel."""
        print("[*] Đang tải các nguồn dữ liệu từ Excel...")
        excel_path = self.config['data']['excel_path']
        self.all_data = load_all_sheets_from_excel(excel_path)
        
        # Thiết lập các DataFrame chính
        self.anime_info_df = self.all_data.get(self.config['data']['knowledge_base_sheet'])
        if self.anime_info_df is not None:
            self.anime_info_df = self.anime_info_df.set_index('ID')
            print("    - Đã tải và thiết lập Knowledge Base.")
        
        self.recommendations_df = self.all_data.get(self.config['data']['recommendations_sheet'])
        self.faq_df = self.all_data.get(self.config['data']['faq_sheet'])
        self.quick_answers_df = self.all_data.get(self.config['data']['quick_answers_sheet'])
        self.watch_order_df = self.all_data.get(self.config['data']['watch_order_sheet'])
        print("✅ Đã tải xong dữ liệu.")

    def answer(self, query: str, chat_history: List[Tuple[str, str]] = None) -> str:
        """
        Xử lý câu hỏi của người dùng qua nhiều lớp logic để đưa ra câu trả lời phù hợp nhất.

        Args:
            query (str): Câu hỏi của người dùng.
            chat_history (List[Tuple[str, str]]): Lịch sử cuộc trò chuyện.

        Returns:
            str: Câu trả lời của bot.
        """
        if chat_history is None:
            chat_history = []
            
        print(f"\n[QUERY] Người dùng: '{query}' (Lịch sử: {len(chat_history)} lượt)")
        response = ""
        log_type = "UNKNOWN"

        # Lớp 1: Các quy tắc cứng và nhanh
        response, log_type = self._handle_hard_rules(query)
        if response:
            self._save_conversation(query, response, log_type)
            return response
            
        # Lớp 2: Các quy tắc mềm dựa trên template (cần LLM diễn giải)
        response, log_type = self._handle_soft_rules(query, chat_history)
        if response:
            self._save_conversation(query, response, log_type)
            return response

        # Lớp 3: RAG - Truy xuất và tạo sinh
        print("[LOG] Không khớp quy tắc, chuyển sang RAG...")
        context = self._get_context_from_ids(self.retriever.search(query))
        if context:
            log_type = "RAG"
            prompt = create_rag_prompt(query, context, chat_history)
            response = self.llm_handler.generate(prompt)
            print(f"[LOG] Trả lời từ RAG.")
        
        # Lớp 4: Fallback - Dùng kiến thức chung của LLM
        else:
            log_type = "GENERAL_KNOWLEDGE"
            print("[LOG] Không tìm thấy context, dùng kiến thức chung của LLM.")
            prompt = create_general_prompt(query, chat_history)
            response = self.llm_handler.generate(prompt)

        self._save_conversation(query, response, log_type)
        return response

    def _handle_hard_rules(self, query: str) -> Tuple[Optional[str], str]:
        """Xử lý các câu hỏi có câu trả lời cố định."""
        query_lower = query.lower().strip()
        
        # Chào hỏi
        greetings = ['hi', 'hello', 'chào bạn', 'xin chào']
        if query_lower in greetings:
            return "Chào bạn, tôi là AniBot. Tôi có thể giúp gì cho bạn về thế giới anime?", "GREETING"
        
        # Giới thiệu bản thân
        if "bạn là ai" in query_lower or "tên bạn là gì" in query_lower:
            return "Tôi là AniBot, một trợ lý AI được tạo ra để giúp bạn khám phá thế giới anime.", "PERSONA"

        # FAQ
        faq_answer = self._find_answer_in_sheet(query, self.faq_df, 'Keywords', 'Solution')
        if faq_answer:
            print("[LOG] Tìm thấy trong FAQ.")
            return faq_answer, "FAQ"

        return None, ""
        
    def _handle_soft_rules(self, query: str, history: List[Tuple[str, str]]) -> Tuple[Optional[str], str]:
        """Xử lý các câu hỏi dựa trên template và cần LLM diễn giải."""
        # Thứ tự xem
        if "thứ tự xem" in query.lower() or "watch order" in query.lower():
            for _, row in self.watch_order_df.iterrows():
                if str(row['Series Name']).lower() in query.lower():
                    info = f"Thứ tự xem cho {row['Series Name']} là: {row['Watch Order']}. Ghi chú: {row['Note']}"
                    prompt = create_direct_answer_prompt(query, info, history)
                    return self.llm_handler.generate(prompt), "WATCH_ORDER"
        
        # Gợi ý anime tương tự
        if "giống" in query.lower() or "tương tự" in query.lower():
            for _, row in self.recommendations_df.iterrows():
                if str(row['User Likes']).lower() in query.lower():
                    info = f"Nếu bạn thích {row['User Likes']}, bạn có thể sẽ thích {row['Recommend']} vì {row['Reason']}."
                    prompt = create_direct_answer_prompt(query, info, history)
                    return self.llm_handler.generate(prompt), "RECOMMENDATION"
        
        return None, ""

    def _find_answer_in_sheet(self, query: str, df: Optional[pd.DataFrame], keyword_col: str, answer_col: str) -> Optional[str]:
        if df is None: return None
        for _, row in df.iterrows():
            if pd.isna(row[keyword_col]): continue
            keywords = [kw.strip().lower() for kw in str(row[keyword_col]).split(',')]
            if any(kw in query.lower() for kw in keywords if kw):
                return row[answer_col]
        return None

    def _get_context_from_ids(self, ids: List[int]) -> str:
        """Tạo chuỗi context từ danh sách ID anime."""
        if not ids or self.anime_info_df is None: return ""
        
        context_parts = []
        valid_ids = [id_val for id_val in ids if id_val in self.anime_info_df.index]
        
        if not valid_ids: return ""
        
        for _, row in self.anime_info_df.loc[valid_ids].iterrows():
            context_parts.append(f"Tên: {row['Title']}\nMô tả: {row['Short Description']}")
        
        return "\n---\n".join(context_parts)

    def _save_conversation(self, query: str, response: str, log_type: str):
        """Lưu lại cuộc trò chuyện vào file log."""
        log_dir = self.config.get('logging', {}).get('log_dir', 'logs')
        log_file = self.config.get('logging', {}).get('chat_history_file', 'chat_history.txt')
        
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_file)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] - Method: {log_type}\n")
            f.write(f"  USER: {query}\n")
            f.write(f"  BOT: {response}\n")
            f.write(f"{'-'*60}\n")