# 🎌 AniBot - Trợ Lý AI Chuyên Sâu Về Anime & Manga

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-orange?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/Transformers-4.37-yellow?style=for-the-badge&logo=huggingface)](https://huggingface.co/docs/transformers/index)
[![Gradio](https://img.shields.io/badge/Gradio-4.10-green?style=for-the-badge&logo=gradio)](https://www.gradio.app/)

**AniBot** là một dự án chatbot thông minh, được xây dựng để trở thành một chuyên gia về thế giới anime và manga. Sử dụng kiến trúc **RAG (Retrieval-Augmented Generation)**, AniBot có khả năng kết hợp một cơ sở kiến thức tùy chỉnh (từ file Excel) với sức mạnh của các Mô hình Ngôn ngữ Lớn (LLM) hiện đại để đưa ra những câu trả lời chính xác, chi tiết và tự nhiên.

---

## ⚠️ Lưu Ý Quan Trọng Về Yêu Cầu Hệ Thống

Dự án này sử dụng các Mô hình Ngôn ngữ Lớn (LLM) có dung lượng rất lớn.

*   **Dung lượng Model:** Model được đề xuất (`google/gemma-2-9b-it`) có dung lượng tải về khoảng **18 GB**.
*   **Yêu cầu VRAM:** Để chạy model này, bạn cần một GPU NVIDIA với ít nhất **16 GB VRAM**.
*   **Khuyến nghị:**
    *   **Để thử nghiệm và chuẩn bị dữ liệu:** Khuyến khích sử dụng **Google Colab** để tận dụng tốc độ mạng cao khi tải model.
    *   **Để triển khai và sử dụng lâu dài:** Khuyến khích **thuê một GPU Server** (ví dụ: RTX 3090/4090, A4000, A6000...) để đảm bảo hiệu suất và sự ổn định.

---

## ✨ Tính Năng Nổi Bật

- **Hệ Thống Trả Lời Đa Tầng:** Xử lý câu hỏi qua nhiều lớp logic, từ các quy tắc cứng (FAQ, chào hỏi) đến RAG và fallback, đảm bảo câu trả lời phù hợp nhất cho từng tình huống.
- **Truy Xuất Thông Tin Thông Minh (RAG):** Sử dụng `sentence-transformers` và `FAISS` để tìm kiếm các thông tin anime liên quan nhất trong cơ sở dữ liệu dựa trên ngữ nghĩa của câu hỏi.
- **Sinh Văn Bản Nâng Cao:** Tận dụng sức mạnh của các LLM lớn như `google/gemma-2-9b-it` để diễn giải thông tin và tạo ra các câu trả lời mạch lạc, tự nhiên.
- **Cơ Sở Kiến Thức Tùy Chỉnh:** Dễ dàng mở rộng kiến thức cho bot bằng cách cập nhật file `Movie_Web_Chatbot_AI.xlsx`.
- **Giao Diện Trực Quan:** Cung cấp giao diện web thân thiện, đẹp mắt được xây dựng bằng **Gradio**.
- **Tối Ưu Hóa Hiệu Năng:** Hỗ trợ kỹ thuật lượng tử hóa 4-bit (`bitsandbytes`) để chạy các model lớn trên các GPU có VRAM giới hạn.

## 🛠️ Kiến Trúc Hệ Thống

Dự án được xây dựng theo kiến trúc module hóa, bao gồm các thành phần chính:
1.  **Data Layer (`src/data_utils`):** Tải và xử lý dữ liệu từ file Excel.
2.  **Core Logic (`src/core`):**
    -   **`Retriever`:** Tìm kiếm ngữ nghĩa bằng `FAISS`.
    -   **`LLMHandler`:** Tương tác với LLM.
    -   **`PromptManager`:** Tạo các prompt động.
3.  **Chatbot Orchestrator (`src/chat_bot.py`):** Lớp chính, điều phối luồng xử lý.
4.  **Presentation Layer (`gradio_app.py`):** Cung cấp giao diện người dùng.

## 🚀 Hướng Dẫn Cài Đặt và Sử Dụng

Làm theo các bước sau để triển khai AniBot trên một server Linux có GPU.

### 1. Chuẩn Bị
- Một server Linux (khuyến nghị Ubuntu 22.04) với GPU NVIDIA (>= 16GB VRAM).
- Đã cài đặt Python 3.10+.
- Đã tải mã nguồn dự án lên server.

### 2. Cài Đặt Môi Trường
Mở Terminal và di chuyển vào thư mục gốc của dự án.

```bash
# (Tùy chọn) Cài đặt các công cụ build cần thiết
sudo apt-get update && sudo apt-get install -y build-essential

# Cài đặt tất cả các thư viện Python
pip install -r requirements.txt
```

### 3. Cấu Hình
Mở file `login_helper.py` và dán token Hugging Face của bạn vào. Sau đó chạy:
```bash
python3 login_helper.py
```
Hãy chắc chắn file `config/config.yaml` trỏ đến đúng model bạn muốn dùng.

### 4. Chạy Các Bước Chuẩn Bị
```bash
# Tải models (bước này rất lâu)
python3 src/scripts/download_models.py

# Xây dựng index
python3 src/scripts/build_index.py
```

### 5. Khởi Chạy Ứng Dụng
```bash
# Chạy ứng dụng Gradio
python3 gradio_app.py
```
Gradio sẽ cung cấp một link công khai (`.gradio.live`) để bạn truy cập. Để ứng dụng chạy 24/7, hãy sử dụng `screen` hoặc `nohup`.

## 📬 Liên Hệ

- **Tác giả:** vanujiash9
- **Email:** `thanh.van19062004@gmail.com`
- **Facebook:** [https://www.facebook.com/gmail.com.vancutenemoinguoi196](https://www.facebook.com/gmail.com.vancutenemoinguoi196)

## 🤝 Đóng Góp
Mọi ý kiến đóng góp, báo lỗi, hoặc yêu cầu tính năng đều được chào đón. Vui lòng tạo một "Issue" hoặc "Pull Request" trên kho chứa GitHub này.

---
*Dự án được tạo bởi vanujiash9 - 2025*
