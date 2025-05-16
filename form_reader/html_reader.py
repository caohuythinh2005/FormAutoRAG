from bs4 import BeautifulSoup

def extract_text_from_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # Lọc bỏ các tag script/style
    for tag in soup(['script', 'style']):
        tag.extract()
    return soup.get_text(separator='\n', strip=True)
