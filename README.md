<div align="center">

# AniBot

### Trợ lý AI tiếng Việt dành cho Anime và Manga

AniBot kết hợp **RAG, FAISS và Gemma 2** để tra cứu thông tin, gợi ý Anime và hỗ trợ thứ tự xem bằng hội thoại tự nhiên.

[Demo](#demo) · [Tính năng](#tính-năng) · [Kiến trúc](#kiến-trúc) · [Cài đặt](#cài-đặt) · [Hướng phát triển](#hướng-phát-triển)

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch&logoColor=white)
![Transformers](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E?logo=huggingface&logoColor=black)
![Gemma](https://img.shields.io/badge/LLM-Gemma%202%209B-4285F4)
![FAISS](https://img.shields.io/badge/Vector%20Search-FAISS-0467DF)
![Gradio](https://img.shields.io/badge/UI-Gradio-F97316)
![RAG](https://img.shields.io/badge/Architecture-RAG-7B61FF)
![License](https://img.shields.io/badge/License-MIT-2EA44F)

</div>

---

## Giới thiệu

**AniBot** là chatbot chuyên biệt về Anime và Manga, hỗ trợ người dùng tra cứu thông tin, tìm nội dung tương tự, xem thứ tự phát hành và nhận gợi ý bằng tiếng Việt.

Thay vì gửi mọi câu hỏi trực tiếp đến mô hình ngôn ngữ, hệ thống sử dụng **query routing** để lựa chọn cách xử lý phù hợp:

- Trả lời trực tiếp bằng rule cho câu hỏi đơn giản
- Truy xuất dữ liệu có cấu trúc cho recommendation và watch order
- Tìm kiếm ngữ nghĩa bằng FAISS cho câu hỏi kiến thức
- Sử dụng Gemma 2 để tạo câu trả lời tự nhiên từ context đã truy xuất

---

## Demo

<div align="center">

![AniBot Demo]([assets/anibot-demo.gif](https://drive.google.com/drive/folders/1L5tVq8qTbOgABFLb4pfX1nJFJ9myRXv8))

</div>

---

## Tính năng

- Hỏi đáp về Anime và Manga bằng tiếng Việt
- Semantic search với sentence embeddings
- Vector retrieval bằng FAISS
- Retrieval-Augmented Generation với Gemma 2 9B Instruct
- Gợi ý Anime có nội dung tương tự
- Tra cứu thứ tự xem của các series
- Xử lý nhanh FAQ và câu hỏi đơn giản bằng rules
- Quản lý context hội thoại
- Lưu lịch sử và phương thức tạo câu trả lời
- Giao diện web bằng Gradio

---

## Kiến trúc

```text
Người dùng
   ↓
Giao diện Gradio
   ↓
Query Router
   ├── Greeting / FAQ ───────→ Rule-based Response
   ├── Recommendation ───────→ Structured Data
   ├── Watch Order ──────────→ Structured Data
   └── Knowledge Query
          ↓
     Embedding Model
          ↓
     FAISS Vector Search
          ↓
     Relevant Context
          ↓
       RAG Prompt
          ↓
     Gemma 2 9B Instruct
          ↓
      Câu trả lời
```

---

## Công nghệ sử dụng

### Ngôn ngữ và định dạng

| Công nghệ | Vai trò |
|---|---|
| Python | Xây dựng pipeline chatbot, xử lý dữ liệu, retrieval và inference |
| YAML | Quản lý cấu hình model và đường dẫn |
| JSON | Lưu tham số model và mapping dữ liệu |
| Markdown | Viết tài liệu dự án |

### AI và xử lý dữ liệu

| Thành phần | Công nghệ |
|---|---|
| Large Language Model | Google Gemma 2 9B Instruct |
| Embedding model | sentence-transformers/all-MiniLM-L6-v2 |
| Vector search | FAISS |
| Deep Learning | PyTorch |
| LLM framework | Hugging Face Transformers |
| Data processing | Pandas, OpenPyXL, NumPy |
| Giao diện | Gradio |
| Knowledge base | Microsoft Excel |
| Kiến trúc | Retrieval-Augmented Generation |

---

## Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/vanujiash9/MOVIE_CHAT.git
cd MOVIE_CHAT
```

### 2. Tạo môi trường ảo

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux hoặc macOS:

```bash
source .venv/bin/activate
```

### 3. Cài đặt thư viện

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Chuẩn bị mô hình

Chạy script tải model:

```bash
python src/scripts/download_models.py
```

Các model mặc định:

```text
Embedding: sentence-transformers/all-MiniLM-L6-v2
LLM: google/gemma-2-9b-it
```

> Gemma có thể yêu cầu đăng nhập Hugging Face và chấp nhận điều khoản sử dụng trước khi tải.

---

## Xây dựng FAISS index

Đặt file dữ liệu tại:

```text
data/Movie_Web_Chatbot_AI.xlsx
```

Sau đó chạy:

```bash
python src/scripts/build_index.py
```

Các file index được tạo:

```text
data/processed/
├── anime_embeddings.faiss
└── index_to_id.json
```

---

## Chạy ứng dụng

```bash
python gradio_app.py
```

Truy cập ứng dụng tại:

```text
http://localhost:7861
```

---

## Ví dụ câu hỏi

```text
Jujutsu Kaisen nói về điều gì?
```

```text
Gợi ý Anime giống Attack on Titan.
```

```text
Thứ tự xem Fate như thế nào?
```

```text
Tôi thích Anime tâm lý, bí ẩn và có nhiều plot twist. Nên xem gì?
```

---

## Cấu trúc dự án

```text
MOVIE_CHAT/
├── config/
│   ├── config.yaml
│   └── model_config.json
├── data/
│   ├── Movie_Web_Chatbot_AI.xlsx
│   └── processed/
├── models/
├── src/
│   ├── core/
│   ├── data_utils/
│   └── scripts/
├── assets/
├── logs/
├── gradio_app.py
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

## Hướng phát triển

- [ ] Thêm similarity threshold cho retrieval
- [ ] Hiển thị nguồn dữ liệu trong câu trả lời
- [ ] Hỗ trợ quantization 4-bit hoặc 8-bit
- [ ] Xây dựng REST API bằng FastAPI
- [ ] Lưu hội thoại bằng SQLite hoặc PostgreSQL
- [ ] Bổ sung bộ đánh giá retrieval và hallucination
- [ ] Docker hóa ứng dụng
- [ ] Triển khai lên cloud
- [ ] Tích hợp Telegram hoặc Discord

---

## Tác giả

GitHub: [@vanujiash9](https://github.com/vanujiash9)

---

## Giấy phép

Dự án được phát hành theo giấy phép [MIT](LICENSE).

<div align="center">

Được xây dựng bằng **Python, PyTorch, Gemma 2, FAISS và Gradio**.

Nếu dự án hữu ích, hãy để lại một ⭐ để ủng hộ.

</div>

- 📧 Email: [thanh.van19062004@gmail.com](mailto:thanh.van19062004@gmail.com)  
- 💻 GitHub: [@vanujiash9](https://github.com/vanujiash9)

Nếu bạn thấy dự án hữu ích, hãy để lại một ⭐ **Star** trên GitHub để ủng hộ.
