# src/core/model_handler.py - GPU Server Version
import torch, os
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, Any

class LLMHandler:
    def __init__(self, model_path: str, model_config: Dict[str, Any]):
        print("[*] Đang khởi tạo LLM Handler (chế độ FP16 - GPU Server)...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if self.device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"    - GPU được phát hiện: {gpu_name}")
            print(f"    - VRAM: {gpu_memory:.1f}GB")
        else:
            print("    - Sử dụng CPU")

        print(f"    - Đang tải Tokenizer từ: '{model_path}'")
        print(f"    - Đang tải Model với FP16 từ: '{model_path}'...")
        
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # Load model với FP16 thay vì quantization
            if self.device == "cuda":
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    torch_dtype=torch.float16,  # FP16 thay vì quantization
                    device_map="auto",
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    torch_dtype=torch.float32,
                    device_map="cpu",
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
                
            print("✅ LLM Handler đã sẵn sàng!")
            
        except Exception as e:
            print(f"❌ Lỗi nghiêm trọng khi tải model: {e}")
            raise

    def generate(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        try:
            chat_template = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            inputs = self.tokenizer(chat_template, return_tensors="pt").to(self.model.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs, 
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
            response_text = self.tokenizer.decode(
                outputs[0][inputs.input_ids.shape[-1]:], 
                skip_special_tokens=True
            )
            return response_text.strip()
            
        except Exception as e:
            print(f"Lỗi khi generate: {e}")
            return "Xin lỗi, đã có sự cố khi tạo câu trả lời."