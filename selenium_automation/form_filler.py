from selenium.webdriver.common.by import By
from .web_client import WebClient
import logging

class FormFiller:
    def __init__(self, web_client: WebClient):
        self.web_client = web_client

    def fill_form_and_submit(self, url: str, form_data: dict):
        """
        Mở trang, điền form theo dict form_data (key là tên trường, value là dữ liệu),
        rồi submit form.

        form_data ví dụ: {
            "fullname": "Nguyễn Văn A",
            "email": "nguyenvana@example.com",
            "phone": "0901234567"
        }
        """
        self.web_client.open_url(url)

        # Ví dụ trường input có id hoặc name giống key trong form_data
        for field_name, value in form_data.items():
            try:
                # Tìm input bằng id hoặc name
                try:
                    self.web_client.send_keys(By.ID, field_name, value)
                except:
                    self.web_client.send_keys(By.NAME, field_name, value)
                logging.info(f"Filled field {field_name} with value '{value}'")
            except Exception as e:
                logging.error(f"Không tìm thấy trường '{field_name}': {e}")

        # Giả sử nút submit có id 'submit-btn'
        try:
            self.web_client.click(By.ID, "submit-btn")
            logging.info("Form submitted.")
        except Exception as e:
            logging.error(f"Không tìm thấy hoặc không thể click nút submit: {e}")
