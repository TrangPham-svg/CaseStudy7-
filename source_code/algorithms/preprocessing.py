import re
from typing import List

def preprocess_text(text: str) -> List[str]:
    """
    Chuẩn hóa văn bản: chuyển chữ thường, loại bỏ dấu câu/ký tự đặc biệt, tách thành tokens (từ).
    Hỗ trợ đầy đủ tiếng Việt (giữ nguyên dấu).
    Trả về danh sách các từ đã chuẩn hóa.
    """
    if not text:
        return []

    # Chuyển về chữ thường (hỗ trợ unicode)
    text = text.lower()

    # Loại bỏ dấu câu/ký tự đặc biệt, thay bằng space (giữ \w bao gồm chữ cái có dấu)
    text = re.sub(r'[^\w\s]', ' ', text)

    # Loại bỏ khoảng trắng thừa và tách thành tokens
    tokens = re.split(r'\s+', text.strip())

    return tokens
