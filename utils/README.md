## Notes
- text_cleaner.py: làm sạch và chuẩn hóa text → ✔ đã có test
- tokenizer.py: dùng tokenizer của transformers, hỗ trợ tokenize + detokenize → ✔ test ok
- stopwords.py: lọc từ dừng bằng nltk → ✔ test chạy ổn
- text_utils.py: bạn có thể thêm dần, ví dụ:
- đo độ dài trung bình câu
- đếm số từ, số câu
- kiểm tra có chứa số, dấu câu, v.v.
- tests/: dùng .ipynb để test từng file → dễ debug, xem log rõ ràng


## Structure


'''
utils/
├── __init__.py
├── text_cleaner.py      # Xử lý làm sạch, chuẩn hóa văn bản
├── tokenizer.py         # Tách câu thành tokens, detokenize
├── stopwords.py         # Danh sách stopwords và hàm loại bỏ
├── text_utils.py        # Các hàm tiện ích khác (ví dụ: đo độ dài câu, ... )
└── tests/
    ├── __init__.py
    ├── test_text_cleaner.ipynb
    ├── test_tokenizer.ipynb
    └── test_stopwords.ipynb
'''
