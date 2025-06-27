# download_small_model.py - Tải model nhỏ phù hợp với 7.5GB RAM
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

def download_small_models():
    """Tải các model nhỏ phù hợp với RAM thấp"""
    
    models_to_try = [
        {
            "name": "TinyLlama 1.1B", 
            "model_id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "size_gb": 2.2,
            "description": "Model 1.1B params, rất nhỏ, phù hợp cho chat"
        },
        {
            "name": "Phi-2 2.7B",
            "model_id": "microsoft/phi-2", 
            "size_gb": 5.4,
            "description": "Model 2.7B params từ Microsoft, chất lượng tốt"
        },
        {
            "name": "DialoGPT Medium",
            "model_id": "microsoft/DialoGPT-medium",
            "size_gb": 1.4,
            "description": "Model 355M params, chuyên chat, rất nhẹ"
        }
    ]
    
    print("=== TẢI MODEL NHỎ CHO MÁY 7.5GB RAM ===\n")
    
    for i, model_info in enumerate(models_to_try, 1):
        print(f"{i}. {model_info['name']}")
        print(f"   Size: ~{model_info['size_gb']}GB")
        print(f"   Mô tả: {model_info['description']}")
        print()
    
    choice = input("Chọn model để tải (1-3) hoặc 'all' để tải tất cả: ").strip()
    
    if choice.lower() == 'all':
        selected_models = models_to_try
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(models_to_try):
                selected_models = [models_to_try[idx]]
            else:
                print("Lựa chọn không hợp lệ!")
                return
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")
            return
    
    for model_info in selected_models:
        print(f"\n🔄 Đang tải {model_info['name']}...")
        
        try:
            model_id = model_info['model_id']
            save_path = f"models/small_model_{model_info['name'].lower().replace(' ', '_').replace('-', '_')}"
            
            # Tạo thư mục
            os.makedirs(save_path, exist_ok=True)
            
            # Tải tokenizer
            print("  - Đang tải tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
            tokenizer.save_pretrained(save_path)
            
            # Tải model
            print("  - Đang tải model...")
            model = AutoModelForCausalLM.from_pretrained(
                model_id, 
                trust_remote_code=True,
                torch_dtype="auto"
            )
            model.save_pretrained(save_path)
            
            print(f"  ✅ Đã tải {model_info['name']} thành công!")
            print(f"  📁 Lưu tại: {save_path}")
            
            # Tạo file hướng dẫn
            with open(f"{save_path}/README.txt", "w", encoding="utf-8") as f:
                f.write(f"Model: {model_info['name']}\n")
                f.write(f"Size: ~{model_info['size_gb']}GB\n")
                f.write(f"Description: {model_info['description']}\n")
                f.write(f"Original ID: {model_id}\n\n")
                f.write("Để sử dụng model này, sửa đường dẫn trong config.yml:\n")
                f.write(f"models:\n")
                f.write(f"  llm_local_path: '{save_path}'\n")
            
        except Exception as e:
            print(f"  ❌ Lỗi khi tải {model_info['name']}: {e}")
    
    print(f"\n🎉 Hoàn thành! Để sử dụng model mới:")
    print("1. Mở file 'config/config.yml'")
    print("2. Sửa dòng 'llm_local_path' thành đường dẫn model mới")
    print("3. Chạy lại 'python app.py'")

if __name__ == "__main__":
    download_small_models()