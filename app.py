# app.py

import os
import sys
import threading
from flask import Flask, render_template, request, jsonify

# ======================================================================
# PHẦN 1: THIẾT LẬP MÔI TRƯỜNG & KHỞI TẠO CHATBOT
# ======================================================================

# Thêm thư mục gốc vào Python path để có thể import từ 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Khai báo các biến toàn cục để quản lý trạng thái chatbot
app_state = {
    "chatbot_instance": None,
    "chatbot_error": None,
    "is_initializing": True,
}

def initialize_chatbot():
    """Tải model trong một luồng riêng để không chặn server Flask."""
    global app_state
    print("="*60)
    print("🤖 Bắt đầu khởi tạo AniBot trong luồng riêng...")
    print("   (Quá trình này có thể mất vài phút để tải model vào VRAM)")
    
    try:
        from src.chat_bot import Chatbot
        chatbot = Chatbot(
            config_path='config/config.yaml',
            model_config_path='config/model_config.json'
        )
        app_state["chatbot_instance"] = chatbot
        print("✅ AniBot đã sẵn sàng phục vụ!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ LỖI NGHIÊM TRỌNG KHI KHỞI TẠO CHATBOT: {e}\n")
        import traceback
        traceback.print_exc()
        app_state["chatbot_error"] = str(e)
    finally:
        app_state["is_initializing"] = False

# ======================================================================
# PHẦN 2: KHỞI TẠO ỨNG DỤNG FLASK VÀ CÁC ROUTE
# ======================================================================

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # Hỗ trợ tiếng Việt

@app.route("/")
def home():
    """Route để hiển thị trang chat chính (templates/index.html)."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint để nhận câu hỏi và trả về câu trả lời."""
    # Kiểm tra trạng thái của chatbot
    if app_state["is_initializing"]:
        return jsonify({"answer": "⏳ Xin lỗi, AniBot vẫn đang khởi động. Vui lòng chờ một chút rồi thử lại..."}), 503
    
    if app_state["chatbot_error"]:
        return jsonify({"answer": f"❌ Đã xảy ra lỗi nghiêm trọng khi khởi động Bot: {app_state['chatbot_error']}"}), 500
        
    data = request.json
    user_message = data.get("message")
    chat_history = data.get("history", [])
    
    if not user_message:
        return jsonify({"error": "Không có tin nhắn nào được cung cấp."}), 400

    try:
        bot_response = app_state["chatbot_instance"].answer(user_message, chat_history)
        return jsonify({"answer": bot_response})
    except Exception as e:
        print(f"Lỗi khi xử lý câu hỏi '{user_message}': {e}")
        return jsonify({"answer": "Rất xin lỗi, đã có sự cố xảy ra khi tôi đang xử lý câu hỏi của bạn."}), 500

# ======================================================================
# PHẦN 3: CHẠY SERVER
# ======================================================================

if __name__ == "__main__":
    print("🚀 Bắt đầu khởi chạy server Flask cho AniBot...")
    
    # 1. Khởi tạo chatbot trong một luồng riêng
    chatbot_thread = threading.Thread(target=initialize_chatbot)
    chatbot_thread.daemon = True
    chatbot_thread.start()

    # 2. Cấu hình cổng và chạy Flask app
    port = 5000
    print("="*60)
    print(f"🏠 Giao diện web sẽ có tại:")
    print(f"👉 http://127.0.0.1:{port}")
    print("   (Vui lòng chờ thông báo 'AniBot đã sẵn sàng' trước khi truy cập)")
    print("="*60)
    
    # Chạy server, debug=False là quan trọng
    app.run(host='0.0.0.0', port=7860, debug=False)
