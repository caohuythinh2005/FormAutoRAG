from form_reader.pdf_reader import extract_text_from_pdf
from form_reader.docx_reader import extract_text_from_docx
from form_reader.html_reader import extract_text_from_html
from form_reader.image_reader import extract_text_from_image

print("=== PDF Reader ===")
print(extract_text_from_pdf("./test_data/form_sample.pdf"))

# print("\n=== DOCX Reader ===")
# print(extract_text_from_docx("./test_data/form_sample.docx"))

# print("\n=== HTML Reader ===")
# print(extract_text_from_html("./test_data/form_sample.html"))

# print("\n=== Image Reader ===")
# print(extract_text_from_image("./test_data/form_sample.png"))
