# 🎌 AniBot V2 - Trợ Lý AI Chuyên Sâu Về Anime & Manga

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-orange?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![Gradio](https://img.shields.io/badge/Gradio-4.10-green?style=for-the-badge&logo=gradio)](https://www.gradio.app/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow)](https://huggingface.co/spaces)

**AniBot** là một dự án chatbot thông minh, được xây dựng để trở thành một chuyên gia về thế giới anime và manga. Sử dụng kiến trúc **RAG (Retrieval-Augmented Generation)**, AniBot có khả năng kết hợp một cơ sở kiến thức tùy chỉnh (từ file Excel) với sức mạnh của các Mô hình Ngôn ngữ Lớn (LLM) hiện đại như `google/gemma-2-9b-it` để đưa ra những câu trả lời chính xác, chi tiết và tự nhiên.

---

## 🖼️ Giao Diện Demo

Giao diện được xây dựng bằng Gradio với CSS tùy chỉnh, mang lại trải nghiệm tương tác thân thiện, hiện đại và responsive trên mọi thiết bị.

| Giao diện chính | Cuộc hội thoại ví dụ |
| :---: | :---: |
| ![Giao diện chính của AniBot](https://github.com/user-attachments/assets/5189f7f4-d50c-4389-9e8c-57c9dfd39a3f) | ![Ví dụ hội thoại với AniBot](https://github.com/user-attachments/assets/b343c5b5-7836-4148-be28-a83d3408f9ac) |

---

## ⚡ Bắt Đầu Nhanh (Sử Dụng Model Đã Tải Sẵn)

Để tiết kiệm thời gian và băng thông, bạn có thể tải về bộ model đã được chuẩn bị sẵn, bao gồm `google/gemma-2-9b-it` và model embedding (tổng dung lượng ~18GB).

1.  **Tải Model:** Tải file `models.zip` từ link Google Drive sau:
    > **[🔗 Tải Bộ Models (18GB+) Tại Đây]**
    > (https://drive.google.com/drive/folders/1L5tVq8qTbOgABFLb4pfX1nJFJ9myRXv8?usp=sharing)

2.  **Giải Nén:** Giải nén file `models.zip` và đặt thư mục `models` vào thư mục gốc của dự án.
3.  **Bỏ Qua Bước Tải:** Khi thực hiện theo hướng dẫn cài đặt bên dưới, bạn có thể **bỏ qua bước `python3 src/scripts/download_models.py`**.

---

## ⚠️ Yêu Cầu Hệ Thống

Dự án này sử dụng các LLM có dung lượng rất lớn.
- **VRAM:** Yêu cầu GPU NVIDIA với ít nhất **16 GB VRAM** để chạy ở chế độ lượng tử hóa 4-bit.
- **Dung lượng ổ đĩa:** Cần ít nhất 25 GB dung lượng trống.
- **Khuyến nghị:**
    - **Để chuẩn bị dữ liệu:** Sử dụng **Google Colab** để tận dụng tốc độ mạng cao.
    - **Để triển khai:** **Thuê một GPU Server** (ví dụ: RTX 3090/4090, RTX A4000...) hoặc triển khai trên **Hugging Face Spaces**.

---

## ✨ Tính Năng & Kiến Trúc

### Tính Năng Nổi Bật
- **Hệ Thống Trả Lời Đa Tầng:** Xử lý câu hỏi qua nhiều lớp logic để đưa ra câu trả lời phù hợp nhất.
- **Truy Xuất Thông Tin Thông Minh (RAG):** Sử dụng `sentence-transformers` và `FAISS` để tìm kiếm thông tin dựa trên ngữ nghĩa.
- **Sinh Văn Bản Nâng Cao:** Tận dụng sức mạnh của `google/gemma-2-9b-it` để diễn giải thông tin và tạo ra các câu trả lời tự nhiên.
- **Cơ Sở Kiến Thức Tùy Chỉnh:** Dễ dàng mở rộng kiến thức cho bot bằng cách cập nhật file `data/Movie_Web_Chatbot_AI.xlsx`.
- **Tối Ưu Hóa Hiệu Năng:** Sử dụng kỹ thuật lượng tử hóa 4-bit (`bitsandbytes`) để chạy model lớn trên các GPU có VRAM hạn chế.

### Kiến Trúc Hệ Thống
1.  **Data Layer (`src/data_utils`):** Tải và xử lý dữ liệu từ Excel.
2.  **Core Logic (`src/core`):**
    -   **`Retriever`:** Tìm kiếm ngữ nghĩa.
    -   **`LLMHandler`:** Tương tác với LLM.
    -   **`PromptManager`:** Quản lý và tạo prompt động.
3.  **Chatbot Orchestrator (`src/chat_bot.py`):** Lớp chính, điều phối luồng xử lý.
4.  **Presentation Layer (`gradio_app.py`):** Cung cấp giao diện người dùng.

---

## 🚀 Hướng Dẫn Cài Đặt và Triển Khai

Làm theo các bước sau để triển khai AniBot trên một server Linux (khuyến nghị Ubuntu 22.04) có GPU.

### 1. Cài Đặt Môi Trường
Mở Terminal và di chuyển vào thư mục gốc của dự án.
```bash
# Cài đặt các công cụ build cần thiết (chỉ làm một lần)
sudo apt-get update && sudo apt-get install -y build-essential

# Cài đặt tất cả các thư viện Python từ file requirements
pip install -r requirements.txt
```

### 2. Cấu Hình
Mở file `login_helper.py`, dán token Hugging Face của bạn vào và chạy:
```bash
python3 login_helper.py
```
Hãy chắc chắn file `config/config.yaml` đã được cấu hình đúng.

### 3. Chuẩn Bị Dữ Liệu & Models
*(Bạn có thể bỏ qua `download_models` nếu đã tải từ link Google Drive ở trên)*
```bash
# Tải models (bước này rất lâu)
python3 src/scripts/download_models.py

# Xây dựng index từ file Excel
python3 src/scripts/build_index.py
```

### 4. Khởi Chạy Ứng Dụng
```bash
# Chạy ứng dụng Gradio
python3 gradio_app.py
```
Gradio sẽ cung cấp một link công khai (`.gradio.live`) để bạn truy cập. Để ứng dụng chạy 24/7, hãy sử dụng `screen` hoặc `nohup`.

---

## 📬 Liên Hệ

- **Tác giả:** vanujiash9
- **Email:** `thanh.van19062004@gmail.com`
- **Facebook:** [https://www.facebook.com/gmail.com.vancutenemoinguoi196](https://www.facebook.com/gmail.com.vancutenemoinguoi196)

## 🤝 Đóng Góp
Mọi ý kiến đóng góp, báo lỗi, hoặc yêu cầu tính năng đều được chào đón. Vui lòng tạo một "Issue" hoặc "Pull Request" trên kho chứa GitHub này.

---
*Dự án được tạo bởi vanujiash9 - 2025*
