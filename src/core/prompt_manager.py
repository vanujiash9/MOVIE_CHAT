# src/core/prompt_manager.py (Phiên bản tăng cường sự sáng tạo)

from typing import List, Tuple

def _format_chat_history(chat_history: List[Tuple[str, str]]) -> str:
    """
    Định dạng lịch sử chat thành một chuỗi văn bản rõ ràng cho model.
    Hàm này không thay đổi.
    """
    if not chat_history:
        return ""
    
    # Chuyển đổi định dạng của Gradio (list of lists) sang định dạng text
    formatted_history = "\n\nLịch sử hội thoại trước đó để tham khảo ngữ cảnh:\n"
    for user_msg, bot_msg in chat_history:
        # Đảm bảo bot_msg không phải là None trước khi thêm vào
        if user_msg and bot_msg:
            formatted_history += f"- Người dùng: {user_msg}\n"
            formatted_history += f"- Trợ lý: {bot_msg}\n"
    return formatted_history

def create_rag_prompt(query: str, context: str, chat_history: List[Tuple[str, str]]) -> str:
    """
    Tạo prompt cho kịch bản RAG, nhưng cho phép model linh hoạt và sáng tạo hơn.
    Đây là hàm đã được thay đổi.
    """
    history_str = _format_chat_history(chat_history)
    
    # --- PROMPT MỚI ĐÃ ĐƯỢC NỚI LỎNG ---
    prompt = f"""Bạn là AniBot, một trợ lý AI chuyên gia, thân thiện và am hiểu sâu sắc về anime.
    
Nhiệm vụ của bạn là trả lời câu hỏi của người dùng một cách đầy đủ và hấp dẫn nhất.

Dưới đây là một số thông tin tham khảo từ cơ sở dữ liệu có thể liên quan đến câu hỏi. Hãy ưu tiên sử dụng thông tin này làm nền tảng, nhưng bạn hoàn toàn có thể bổ sung thêm kiến thức chung sâu rộng của mình để làm cho câu trả lời hay hơn, chi tiết hơn và tự nhiên hơn.

--- Thông Tin Tham Khảo (Context) ---
{context}
--- Hết Thông Tin Tham Khảo ---
{history_str}
Câu hỏi hiện tại của người dùng: {query}

Hãy tổng hợp tất cả thông tin và kiến thức của bạn để đưa ra một câu trả lời xuất sắc, mạch lạc và tự nhiên bằng tiếng Việt.
Câu trả lời của bạn:"""
    # ------------------------------------

    return prompt

def create_direct_answer_prompt(query: str, information: str, chat_history: List[Tuple[str, str]]) -> str:
    """
    Tạo prompt khi đã có sẵn thông tin (từ các quy tắc cứng/mềm).
    Hàm này không thay đổi.
    """
    history_str = _format_chat_history(chat_history)
    
    prompt = f"""Bạn là AniBot, một trợ lý AI thân thiện. Bạn đã tìm thấy thông tin sau đây để trả lời người dùng. Hãy diễn đạt lại thông tin này một cách tự nhiên và mạch lạc nhất bằng tiếng Việt.

--- Thông Tin Có Sẵn ---
{information}
--- Hết Thông Tin ---
{history_str}
Câu hỏi của người dùng: {query}

Câu trả lời tự nhiên của bạn:"""
    return prompt

def create_general_prompt(query: str, chat_history: List[Tuple[str, str]]) -> str:
    """
    Tạo prompt cho kịch bản fallback, khi không có context.
    Hàm này không thay đổi.
    """
    history_str = _format_chat_history(chat_history)

    prompt = f"""Bạn là AniBot, một trợ lý AI am hiểu sâu sắc về anime và các chủ đề liên quan. Hãy trả lời câu hỏi của người dùng một cách thân thiện, hữu ích và hấp dẫn bằng tiếng Việt.
{history_str}
Câu hỏi của người dùng: {query}

Câu trả lời của bạn:"""
    return prompt