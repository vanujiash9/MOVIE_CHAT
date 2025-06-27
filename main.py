# main.py
import os
import sys

# Thêm thư mục gốc vào Python path để có thể import từ 'src'
# Điều này rất quan trọng để có thể tìm thấy module src.chatbot
# __file__ là đường dẫn tới chính file main.py này.
# os.path.dirname() lấy ra thư mục chứa nó (thư mục gốc của project).
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Chúng ta sẽ import Chatbot sau khi đã thêm path
from src.chat_bot import Chatbot

def run_chat_session():
    """
    Khởi tạo và chạy một phiên hội thoại với chatbot trên dòng lệnh.
    Hữu ích cho việc kiểm tra nhanh và gỡ rối.
    """
    config_path = 'config/config.yaml'
    model_config_path = 'config/model_config.json'

    # --- Kiểm tra các điều kiện tiên quyết ---
    print("Kiểm tra các file cần thiết...")
    # Kiểm tra file cấu hình
    if not os.path.exists(config_path):
        print(f"LỖI: Không tìm thấy file cấu hình tại '{config_path}'.")
        return

    # Kiểm tra FAISS index đã được tạo chưa
    if not os.path.exists('data/processed/anime_embeddings.faiss'):
        print("\nCẢNH BÁO: Không tìm thấy FAISS index ('data/processed/anime_embeddings.faiss').")
        print("Có thể bạn chưa chạy script chuẩn bị. Vui lòng chạy:")
        # Sửa lại đường dẫn script cho đúng với cấu trúc của bạn
        print(">>> python -m src.scripts.build_index")
        return

    try:
        # Khởi tạo chatbot
        # Tất cả logic phức tạp về tải model, dữ liệu đều nằm trong class Chatbot
        bot = Chatbot(config_path=config_path, model_config_path=model_config_path)

        # Bắt đầu vòng lặp chat
        print("\n" + "="*50)
        print("    Chào mừng đến với AniBot (chế độ dòng lệnh)")
        print("    Gõ 'exit' để thoát.")
        print("="*50 + "\n")

        while True:
            user_query = input("You: ")
            if user_query.lower() in ['exit', 'quit', 'bye']:
                print("Bot: Tạm biệt! Hẹn gặp lại bạn sau.")
                break
            
            # Lấy câu trả lời từ chatbot
            response = bot.answer(user_query)
            print(f"Bot: {response}")

    except FileNotFoundError as e:
        print(f"\nLỖI KHỞI TẠO: {e}")
        print("Vui lòng đảm bảo bạn đã chạy các script chuẩn bị:")
        # Sửa lại đường dẫn script cho đúng
        print("1. python -m src.scripts.download_models")
        print("2. python -m src.scripts.build_index")
    except Exception as e:
        print(f"\nĐã xảy ra một lỗi không mong muốn: {e}")
        # In ra traceback để gỡ rối dễ hơn
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_chat_session()