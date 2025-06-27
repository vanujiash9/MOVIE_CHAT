# download_direct.py - Tải model trực tiếp vào D:
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set cache vào D:
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache'

def download_small_model():
    """Tải model nhỏ trực tiếp vào D:"""
    
    model_id = "microsoft/DialoGPT-medium"  # Chỉ 1.4GB
    save_path = "models/small_model_dialogpt"
    
    try:
        print("🔄 Đang tải DialoGPT Medium (1.4GB)...")
        print("📁 Cache sẽ lưu vào D: drive")
        
        # Tạo thư mục
        os.makedirs(save_path, exist_ok=True)
        
        # Tải tokenizer
        print("  - Đang tải tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        tokenizer.save_pretrained(save_path)
        
        # Tải model
        print("  - Đang tải model...")
        model = AutoModelForCausalLM.from_pretrained(model_id)
        model.save_pretrained(save_path)
        
        print(f"  ✅ Đã tải DialoGPT thành công!")
        print(f"  📁 Lưu tại: {save_path}")
        
        # Tạo file hướng dẫn
        with open(f"{save_path}/README.txt", "w", encoding="utf-8") as f:
            f.write("Model: DialoGPT Medium\n")
            f.write("Size: ~1.4GB\n")
            f.write("Description: Model 355M params, chuyên chat, rất nhẹ\n")
            f.write(f"Original ID: {model_id}\n\n")
            f.write("Để sử dụng model này, sửa đường dẫn trong config.yml:\n")
            f.write(f"models:\n")
            f.write(f"  llm_local_path: '{save_path}'\n")
        
        print(f"\n🎉 Hoàn thành! Để sử dụng:")
        print("1. Sửa config/config.yml:")
        print(f"   llm_local_path: '{save_path}'")
        print("2. Chạy: python app.py")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    download_small_model()