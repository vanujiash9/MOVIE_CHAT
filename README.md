# 🎌 AniBot - Trợ Lý AI Chuyên Sâu Về Anime & Manga

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-orange?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/Transformers-4.37-yellow?style=for-the-badge&logo=huggingface)](https://huggingface.co/docs/transformers/index)
[![Gradio](https://img.shields.io/badge/Gradio-4.10-green?style=for-the-badge&logo=gradio)](https://www.gradio.app/)

**AniBot** là một dự án chatbot thông minh, được xây dựng để trở thành một chuyên gia về thế giới anime và manga. Sử dụng kiến trúc **RAG (Retrieval-Augmented Generation)**, AniBot có khả năng kết hợp một cơ sở kiến thức tùy chỉnh (từ file Excel) với sức mạnh của các Mô hình Ngôn ngữ Lớn (LLM) hiện đại để đưa ra những câu trả lời chính xác, chi tiết và tự nhiên.

## ✨ Tính Năng Nổi Bật

- **Hệ Thống Trả Lời Đa Tầng:** Xử lý câu hỏi qua nhiều lớp logic, từ các quy tắc cứng (FAQ, chào hỏi) đến RAG và fallback, đảm bảo câu trả lời phù hợp nhất cho từng tình huống.
- **Truy Xuất Thông Tin Thông Minh (RAG):** Sử dụng `sentence-transformers` và `FAISS` để tìm kiếm các thông tin anime liên quan nhất trong cơ sở dữ liệu dựa trên ngữ nghĩa của câu hỏi.
- **Sinh Văn Bản Nâng Cao:** Tận dụng sức mạnh của các LLM lớn như `google/gemma-2-9b-it` hoặc `vinai/PhoGPT-4B-Chat` để diễn giải thông tin và tạo ra các câu trả lời mạch lạc, tự nhiên.
- **Cơ Sở Kiến Thức Tùy Chỉnh:** Dễ dàng mở rộng kiến thức cho bot bằng cách cập nhật file `Movie_Web_Chatbot_AI.xlsx` với các sheet thông tin khác nhau (thông tin anime, gợi ý, thứ tự xem, FAQ...).
- **Giao Diện Trực Quan:** Cung cấp giao diện web thân thiện, đẹp mắt được xây dựng bằng **Gradio**, cho phép tương tác dễ dàng.
- **Tối Ưu Hóa Hiệu Năng:** Hỗ trợ các kỹ thuật như lượng tử hóa 4-bit (`bitsandbytes`) để chạy các model lớn trên các GPU có VRAM hạn chế.

## 🛠️ Kiến Trúc Hệ Thống

Dự án được xây dựng theo kiến trúc module hóa, bao gồm các thành phần chính:

1.  **Data Layer (`src/data_utils`):** Chịu trách nhiệm tải và xử lý dữ liệu từ file Excel.
2.  **Core Logic (`src/core`):**
    -   **`Retriever`:** Sử dụng `FAISS` để tìm kiếm ngữ nghĩa.
    -   **`LLMHandler`:** Đóng gói việc tương tác với LLM (tải model, sinh văn bản).
    -   **`PromptManager`:** Quản lý và tạo các prompt động dựa trên ngữ cảnh.
3.  **Chatbot Orchestrator (`src/chat_bot.py`):** Lớp chính, kết hợp tất cả các thành phần để xử lý luồng câu trả lời.
4.  **Presentation Layer (`gradio_app.py` / `app.py`):** Cung cấp giao diện người dùng cuối.

## 🚀 Hướng Dẫn Cài Đặt và Sử Dụng

Làm theo các bước sau để triển khai AniBot trên server Linux (ví dụ: Ubuntu) có GPU.

### 1. Chuẩn Bị
- Một server Linux có GPU NVIDIA (khuyến nghị VRAM >= 16GB).
- Đã cài đặt Python 3.10+.
- Đã có mã nguồn dự án trên server.

### 2. Cài Đặt Môi Trường

Mở Terminal và di chuyển vào thư mục gốc của dự án (`MOVIE_CHATBOT`).

**a. Cài đặt các công cụ build cần thiết (chỉ làm một lần):**
```bash
sudo apt-get update && sudo apt-get install -y build-essential
```

**b. Tạo môi trường ảo (khuyến khích):**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

**c. Cài đặt các thư viện Python:**
Lệnh này sẽ cài đặt tất cả các thư viện cần thiết với phiên bản đã được kiểm tra là tương thích.
```bash
pip install -r requirements.txt
```

### 3. Cấu Hình

**a. Đăng nhập Hugging Face:**
Chạy script helper để xác thực và có quyền tải các model.
```bash
# Mở file login_helper.py và dán token của bạn vào
nano login_helper.py 

# Chạy script
python3 login_helper.py
```

**b. Cấu hình Model:**
Mở file `config/config.yaml` và đảm bảo `llm_repo_id` trỏ đến model bạn muốn sử dụng (ví dụ: `google/gemma-2-9b-it`).

### 4. Chạy Các Bước Chuẩn Bị

**a. Tải Models:**
Lệnh này sẽ xóa thư mục models cũ (nếu có) và tải về các model được định nghĩa trong `config.yaml`.
```bash
rm -rf models
python3 src/scripts/download_models.py
```
*(Lưu ý: Quá trình này sẽ mất nhiều thời gian. Hãy sử dụng `screen` hoặc `tmux` để chạy ngầm nếu kết nối không ổn định.)*

**b. Xây dựng Index:**
Sau khi tải model xong, hãy xây dựng cơ sở dữ liệu vector từ file Excel.
```bash
python3 src/scripts/build_index.py
```

### 5. Khởi Chạy Ứng Dụng

Mọi thứ đã sẵn sàng! Bây giờ hãy khởi động giao diện web.

**a. Chạy để Test:**
```bash
# Chạy trên cổng 7861 để tránh xung đột
python3 gradio_app.py --server_port 7861
```
Gradio sẽ cung cấp một link công khai (`.gradio.live`) để bạn truy cập và thử nghiệm.

**b. Chạy Ngầm 24/7:**
Sau khi đã xác nhận mọi thứ hoạt động, hãy dùng `screen` để ứng dụng chạy liên tục.
```bash
# Bắt đầu một phiên screen tên là "anibot"
screen -S anibot

# Chạy ứng dụng bên trong screen
python3 gradio_app.py --server_port 7861

# Tách ra khỏi screen bằng cách nhấn: Ctrl + A, sau đó nhấn phím D
```
Bây giờ, bạn có thể đóng Terminal và chatbot vẫn sẽ hoạt động qua link Gradio. Để quay lại xem log, dùng lệnh `screen -r anibot`.

## 🤝 Đóng Góp
Mọi ý kiến đóng góp, báo lỗi, hoặc yêu cầu tính năng đều được chào đón. Vui lòng tạo một "Issue" hoặc "Pull Request" trên kho chứa GitHub.

---
*Dự án được tạo bởi [Tên Của Bạn] - [Năm]*
