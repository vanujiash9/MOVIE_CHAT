import pandas as pd

def create_knowledge_documents(anime_info_df: pd.DataFrame) -> pd.DataFrame:
    """Tạo cột 'knowledge' để làm cơ sở cho việc tìm kiếm ngữ nghĩa."""
    if anime_info_df is None or anime_info_df.empty:
        raise ValueError("DataFrame ANIME_INFO không được rỗng.")

    df = anime_info_df.copy()
    
    # Xử lý các giá trị NaN để tránh lỗi khi ghép chuỗi
    str_cols = ['Title', 'Other Names', 'Genres', 'Short Description', 'Similar Anime']
    for col in str_cols:
        df[col] = df[col].fillna('').astype(str)

    # Tạo văn bản tổng hợp cho mỗi anime
    df['knowledge'] = (
        "Tên anime: " + df['Title'] + ". " +
        "Tên gọi khác: " + df['Other Names'] + ". " +
        "Thể loại: " + df['Genres'] + ". " +
        "Tóm tắt: " + df['Short Description']
    )
    
    print("Đã tạo cột 'knowledge' cho RAG.")
    return df[['ID', 'Title', 'knowledge']].copy()