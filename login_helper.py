# login_helper.py (Phiên bản an toàn, đọc từ .env)
import os
from huggingface_hub import login
from dotenv import load_dotenv

def huggingface_login():
    load_dotenv()
    token = os.getenv("HUGGINGFACE_TOKEN")
    
    if not token:
        print("❌ LỖI: Không tìm thấy HUGGINGFACE_TOKEN trong file .env.")
        return

    print("🔑 Đang đăng nhập bằng token từ file .env...")
    try:
        login(token=token, add_to_git_credential=False)
        print("\n✅ Đăng nhập thành công!")
    except Exception as e:
        print(f"\n❌ Đăng nhập thất bại: {e}")

if __name__ == "__main__":
    huggingface_login()