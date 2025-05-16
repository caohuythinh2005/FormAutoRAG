from transformers import AutoTokenizer

# Load pretrained tokenizer, ví dụ dùng bert-base-uncased
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def transformers_tokenize(text: str) -> list[str]:
    """
    Tokenize text using transformers tokenizer,
    trả về list các token dạng string.
    """
    tokens = tokenizer.tokenize(text)
    return tokens

def transformers_encode(text: str) -> list[int]:
    """
    Encode text thành input_ids (dạng số) cho model.
    """
    encoded = tokenizer.encode(text, add_special_tokens=True)
    return encoded

def detokenize(tokens: list[str]) -> str:
    """
    Ghép list tokens thành câu string.
    Xử lý đặc biệt cho tokenizer kiểu BERT có token bắt đầu bằng '##' để nối lại.
    """
    text = ""
    for token in tokens:
        if token.startswith("##"):
            text += token[2:]
        else:
            if len(text) > 0:
                text += " "
            text += token
    return text
