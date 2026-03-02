# 🎌 AniBot V2 — The Ultimate Anime & Manga AI Assistant

AniBot V2 là một **Chatbot AI chuyên sâu cho cộng đồng Anime & Manga**.  
Ứng dụng kết hợp sức mạnh của **Gemma 2 9B** và kỹ thuật **RAG (Retrieval‑Augmented Generation)** để:

- Cung cấp thông tin chính xác
- Tóm tắt cốt truyện, nhân vật, lore
- Gợi ý anime/manga theo sở thích người dùng

---

## ✨ Tính năng nổi bật

- 🧠 **Smart Retrieval (RAG)**  
  Sử dụng **FAISS** để truy xuất ngữ nghĩa từ cơ sở dữ liệu Anime/Manga tùy chỉnh (CSV/Excel).

- 🚀 **High Performance**  
  Tối ưu hóa với **4-bit quantization** (bitsandbytes), chạy mượt trên GPU phổ thông (≥ 16GB VRAM).

- 🔍 **Deep Domain Knowledge**  
  Tra cứu chi tiết về **Studio, Nhân vật, Seiyuu, Lore**, v.v. và trả lời logic, có dẫn dắt.

- 🎯 **Personalized Recommendation**  
  Gợi ý anime/manga theo **sở thích, mood, artstyle** mà người dùng yêu cầu.

- 🎨 **Modern UI**  
  Giao diện **Gradio** thân thiện, hỗ trợ share link public nhanh chóng.

---

## 🛠 Kiến trúc hệ thống

Dự án được thiết kế theo mô hình phân lớp, dễ mở rộng và bảo trì:

```mermaid
graph TD
    A[User Input] --> B[Gradio UI]
    B --> C[Orchestrator]
    C --> D[Embedding Model]
    D --> E[FAISS Vector Store]
    E --> F[Context Retrieval]
    F --> G[Gemma 2 9B LLM]
    G --> B

---

## 💻 Yêu cầu hệ thống

| Thành phần | Cấu hình tối thiểu           | Khuyến nghị                 |
|-----------|------------------------------|-----------------------------|
| GPU       | NVIDIA RTX 3060 (12–16GB)    | RTX 3090 / 4090 (24GB)      |
| RAM       | 16 GB                        | 32 GB                       |
| Disk      | 25 GB SSD                    | 50 GB SSD                   |
| OS        | Ubuntu 20.04+ / Windows 11 (WSL2) | Linux (Dockerized)   |

---

## 🚀 Hướng dẫn cài đặt

### 1️⃣ Khởi tạo môi trường

```bash
# Clone project
git clone https://github.com/vanujiash9/AniBot-V2.git
cd AniBot-V2

# Cài đặt phụ thuộc
pip install -r requirements.txt
```

### 2️⃣ Chuẩn bị Models & Data

**Cách 1 – Dùng bộ models đã đóng gói sẵn (khuyến nghị):**

- Tải tại:  
  https://drive.google.com/drive/folders/1L5tVq8qTbOgABFLb4pfX1nJFJ9myRXv8?usp=sharing  

- Giải nén vào thư mục `models/` ngay tại gốc dự án:

```bash
AniBot/
├── gradio_app.py
├── models/       # <— đặt thư mục giải nén ở đây
└── ...
```

**Cách 2 – Tự tải và build thủ công:**

```bash
python3 src/scripts/download_models.py
python3 src/scripts/build_index.py
```

---

### 3️⃣ Khởi chạy ứng dụng

```bash
python3 gradio_app.py
```

- Gradio sẽ hiển thị đường dẫn local (vd: `http://127.0.0.1:7860`)  
- Có thể bật share link public nếu cần demo nhanh

---

## 📂 Cấu trúc dự án

```text
AniBot/
├── config/             # File cấu hình YAML (đường dẫn model, tham số, ...)
├── data/               # Dataset gốc và index FAISS
├── models/             # Lưu trữ LLM & embedding weights
├── src/
│   ├── core/           # Logic xử lý AI & RAG, orchestrator
│   ├── data_utils/     # Pipeline xử lý dữ liệu, build index
│   └── scripts/        # Script tiện ích (download, build_index, ...)
└── gradio_app.py       # Entry point cho giao diện Gradio
```

---

## 🔮 Lộ trình phát triển (Roadmap)

- [ ] 🌍 **Multi-language**: Hỗ trợ song ngữ Anh – Việt hoàn chỉnh  
- [ ] 🧠 **Long-term Memory**: Ghi nhớ ngữ cảnh hội thoại theo từng phiên  
- [ ] 🧩 **Integration**: Xây dựng API (FastAPI) để tích hợp với Discord Bot / Telegram Bot  
- [ ] ⚡ **Optimization**: Fine‑tuning bằng LoRA để cá nhân hóa văn phong “wibu”

---

## 🤝 Liên hệ & đóng góp

Mọi đóng góp cho AniBot đều được hoan nghênh. Nếu bạn gặp lỗi hoặc có ý tưởng mới, hãy mở **Issue** hoặc gửi **Pull Request**.

- 👤 Tác giả: **Thanh Vân**  
- 📧 Email: [thanh.van19062004@gmail.com](mailto:thanh.van19062004@gmail.com)  
- 💻 GitHub: [@vanujiash9](https://github.com/vanujiash9)

Nếu bạn thấy dự án hữu ích, hãy để lại một ⭐ **Star** trên GitHub để ủng hộ.
