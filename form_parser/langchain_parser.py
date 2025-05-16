from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import re

# Khai báo đường dẫn model LLaMA (thay path cho đúng)
LLAMA_MODEL_PATH = "./models/llama-7b.ggmlv3.q4_0.bin"

# Khởi tạo LLM LlamaCpp với model đã tải
llm = LlamaCpp(model_path=LLAMA_MODEL_PATH)

# Tạo prompt template để extract thông tin
prompt_template = """
Extract the following information from the text below in JSON format:
- Full Name
- Birth Date
- Email
- Phone Number

Text:
{text}

Information (JSON):
"""

PROMPT = PromptTemplate(
    input_variables=["text"],
    template=prompt_template
)

# Tạo chain để dễ gọi
chain = LLMChain(llm=llm, prompt=PROMPT)

def extract_form_info(text: str) -> dict:
    """
    Dùng Llama + prompt engineering để extract thông tin từ text dạng form.
    Trả về dict chứa các field: full_name, birth_date, email, phone_number

    Nếu output không phải JSON chuẩn, sẽ cố parse bằng regex fallback.
    """
    response = chain.run(text=text)
    
    # Cố gắng parse JSON từ response
    import json
    try:
        # Một số LLM trả JSON kèm chú thích hoặc text khác, nên tìm đoạn JSON
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        json_str = response[json_start:json_end]
        info = json.loads(json_str)
    except Exception:
        # fallback: dùng regex đơn giản extract từng trường
        info = {}
        # tìm tên
        match = re.search(r"(?:Họ tên|Full Name|Name):\s*([^\n]+)", text, re.IGNORECASE)
        info["full_name"] = match.group(1).strip() if match else None
        # ngày sinh
        match = re.search(r"(?:Ngày sinh|Birth Date|DOB):\s*([^\n]+)", text, re.IGNORECASE)
        info["birth_date"] = match.group(1).strip() if match else None
        # email
        match = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
        info["email"] = match.group(1) if match else None
        # phone
        match = re.search(r"(?:Số điện thoại|Phone Number|Phone):\s*([\d\s\-\+\(\)]+)", text, re.IGNORECASE)
        info["phone_number"] = match.group(1).strip() if match else None

    return info


if __name__ == "__main__":
    sample_text = """
    Họ tên: Nguyễn Văn A
    Ngày sinh: 01/01/2000
    Email: nguyenvana@example.com
    Số điện thoại: 0901234567
    """
    
    info = extract_form_info(sample_text)
    print(info)