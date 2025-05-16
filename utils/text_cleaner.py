import re
import unicodedata

def normalize_unicode(text: str) -> str:
    """Chuẩn hóa Unicode, chuyển về NFC form."""
    return unicodedata.normalize('NFC', text)

def clean_text(text: str) -> str:
    """
    Làm sạch text:
    - Chuẩn hóa unicode
    - Loại bỏ khoảng trắng thừa
    - Loại bỏ ký tự đặc biệt (ngoại trừ dấu câu cơ bản)
    - Chuyển về chữ thường
    """
    text = normalize_unicode(text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,?!:;\'\"()\-\s]', '', text)
    text = text.lower().strip()
    return text

def remove_non_printable(text: str) -> str:
    """Loại bỏ ký tự không in được."""
    return ''.join(c for c in text if c.isprintable())
