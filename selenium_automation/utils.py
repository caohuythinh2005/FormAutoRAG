import time
import logging

def wait(seconds: float):
    """Hàm delay đơn giản"""
    logging.info(f"Waiting for {seconds} seconds")
    time.sleep(seconds)


def safe_click(element):
    """Click với xử lý ngoại lệ"""
    try:
        element.click()
    except Exception as e:
        logging.error(f"Click failed: {e}")