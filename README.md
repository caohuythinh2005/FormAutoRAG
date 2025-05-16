## Project Structure

```
form_auto_rag/
├── main.py
├── form_reader/
│   ├── __init__.py
│   ├── pdf_reader.py
│   ├── html_reader.py
│   └── docx_reader.py
├── form_parser/
│   ├── __init__.py
│   └── layout_parser.py
├── rag/
│   ├── __init__.py
│   ├── embedder.py
│   ├── retriever.py
│   └── generator.py
├── vector_store/
│   ├── __init__.py
│   └── faiss_store.py
├── selenium_automation/         # Thư mục dành riêng cho code Selenium
│   ├── __init__.py
│   ├── web_client.py            # Wrapper hoặc helper để tương tác Selenium
│   ├── form_filler.py           # Script tự động điền form hoặc gửi prompt lên web
│   └── utils.py                 # Hàm tiện ích riêng cho Selenium nếu cần
├── utils/
│   ├── __init__.py
│   ├── text_cleaner.py
│   ├── tokenizer.py
│   ├── stopwords.py
│   └── text_utils.py
├── tests/
│   ├── __init__.py
│   ├── test_text_cleaner.ipynb
│   ├── test_tokenizer.ipynb
│   ├── test_stopwords.ipynb
│   ├── test_pdf_reader.py
│   ├── test_layout_parser.py
│   ├── test_faiss_store.py
│   └── test_selenium_automation.py   # Test cho selenium_automation
├── requirements.txt
└── README.md
```


