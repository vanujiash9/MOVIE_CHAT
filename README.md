
```markdown
# 🎌 AniBot V2 — Trợ Lý AI cho Anime & Manga

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Gradio](https://img.shields.io/badge/Gradio-4.10-00C853?style=for-the-badge&logo=gradio&logoColor=white)](https://www.gradio.app/)
[![Hugging Face](https://img.shields.io/badge/🤗%20HuggingFace-Spaces-FFD21E?style=for-the-badge)](https://huggingface.co/spaces)

> 🤖 Chatbot AI chuyên sâu về **Anime & Manga**  
> 🧠 Kiến trúc **RAG** + LLM (Gemma 2 9B)  
> 🎯 Ứng dụng: tra cứu, gợi ý, tóm tắt, thảo luận anime/manga

---

## ✨ Tính năng chính

### 🔹 Khả năng cốt lõi

- 📚 **RAG-based retrieval** với FAISS (truy xuất ngữ nghĩa từ tri thức anime/manga)  
- 🧠 Sinh câu trả lời với **Gemma 2 – 9B (instruction-tuned)**  
- 📊 Cơ sở tri thức tùy chỉnh từ file **Excel/CSV**  
- 💾 **4-bit quantization** (bitsandbytes) – tối ưu VRAM, chạy được trên GPU 16GB  
- 🌐 Giao diện **Gradio UI** hiện đại, dễ dùng, dễ deploy lên Hugging Face Spaces

### 🎮 Use case tiêu biểu

- 🔍 Tra cứu thông tin anime/manga (studio, năm, thể loại, nhân vật…)  
- 🎯 Gợi ý anime theo sở thích (thể loại, mood, độ dài, artstyle)  
- 📖 Tóm tắt nội dung, giới thiệu nhân vật, giải thích lore/thế giới  
- 💬 Hỏi đáp, “tám” về anime/manga dựa trên tri thức đã được index

---

## 🖼️ Demo giao diện

| 🏠 Trang chính | 💬 Ví dụ hội thoại |
| :---: | :---: |
| ![Main UI](https://github.com/user-attachments/assets/5189f7f4-d50c-4389-9e8c-57c9dfd39a3f) | ![Chat Example](https://github.com/user-attachments/assets/b343c5b5-7836-4148-be28-a83d3408f9ac) |

---

## ⚙️ Yêu cầu hệ thống

- 🧮 GPU: NVIDIA ≥ **16GB VRAM** (đã dùng 4-bit quantization)  
- 💽 Ổ đĩa trống: ≥ **25GB** (model + index + dữ liệu)  
- 🧪 Khuyến nghị:
  - Chuẩn bị dữ liệu: **Google Colab**
  - Triển khai lâu dài: **GPU server (RTX 3090/4090)** hoặc **Hugging Face Spaces**

---

## ⚡ Khởi động nhanh (dùng bộ model tải sẵn)

### 1️⃣ Tải models

🔗 Link tải:  
https://drive.google.com/drive/folders/1L5tVq8qTbOgABFLb4pfX1nJFJ9myRXv8?usp=sharing

### 2️⃣ Giải nén

Đặt thư mục `models/` vào thư mục gốc dự án:

```bash
AniBot/
├── gradio_app.py
├── models/        # <– đặt thư mục này ở đây
└── ...
```

### 3️⃣ Bỏ qua bước download tự động

Khi đã có `models/`, **không cần** chạy:

```bash
python3 src/scripts/download_models.py
```

---

## 🏗️ Kiến trúc hệ thống

```text
📁 Data Layer (src/data_utils)
        ↓
🔎 Retriever (FAISS + Sentence Transformers)
        ↓
🧠 LLM Handler (Gemma-2-9B)
        ↓
📝 Prompt Manager
        ↓
🎛️ Chatbot Orchestrator
        ↓
🌐 Gradio UI
```

---

## 🚀 Cài đặt & chạy

### 1️⃣ Cài đặt phụ thuộc

```bash
sudo apt-get update && sudo apt-get install -y build-essential
pip install -r requirements.txt
```

### 2️⃣ Đăng nhập Hugging Face (nếu dùng model trên HF)

```bash
python3 login_helper.py
```

Chỉnh `config/config.yaml` cho đúng (tên model, token, đường dẫn, v.v.).

### 3️⃣ Chuẩn bị dữ liệu & models (nếu không dùng gói tải sẵn)

```bash
# Tải models (LLM + embedding)
python3 src/scripts/download_models.py

# Xây dựng index FAISS từ dữ liệu anime/manga
python3 src/scripts/build_index.py
```

### 4️⃣ Chạy ứng dụng

```bash
python3 gradio_app.py
```

- Gradio sẽ hiển thị link local (vd: http://127.0.0.1:7860)  
- Nếu bật share, sẽ có link `.gradio.live`

Chạy 24/7 trên server Linux:

```bash
# Cách 1: screen
screen -S anibot
python3 gradio_app.py

# Cách 2: nohup
nohup python3 gradio_app.py > anibot.log 2>&1 &
```

---

## 📂 Cấu trúc dự án (tóm tắt)

```text
AniBot/
├── gradio_app.py          # Giao diện Gradio
├── src/
│   ├── core/              # Logic chatbot, orchestration
│   ├── data_utils/        # Xử lý dữ liệu, xây index FAISS
│   ├── scripts/           # Script tiện ích (tải model, build index, ...)
│   └── chat_bot.py        # Định nghĩa luồng hội thoại
├── config/                # File cấu hình (.yaml)
├── models/                # Models (LLM, embedding, tokenizer, ...)
└── data/                  # Dữ liệu anime/manga, index FAISS, ...
```

---

## 🔮 Hướng phát triển

- 🧠 Bộ nhớ hội thoại dài (temporal memory, session-based)  
- 🌍 Hỗ trợ đa ngôn ngữ (Anh – Việt – Nhật)  
- 🎯 Fine-tuning / LoRA LLM cho domain anime/manga  
- 🧩 Tách backend thành **API (FastAPI)** để tích hợp vào web/app/Discord bot

---

## 📬 Liên hệ & đóng góp

**Tác giả**

- 👤 Tên: **Thanh Vân**  
- 💻 GitHub: https://github.com/vanujiash9  
- 📧 Email: thanh.van19062004@gmail.com  
- 📘 Facebook: https://www.facebook.com/gmail.com.vancutenemoinguoi196  

**Đóng góp**

- Fork repository  
- Tạo branch mới cho tính năng/bugfix  
- Gửi Pull Request kèm mô tả rõ ràng (mục tiêu, thay đổi, cách test)

⭐ Nếu thấy dự án hữu ích, bạn có thể để lại một **Star** để ủng hộ.
```
