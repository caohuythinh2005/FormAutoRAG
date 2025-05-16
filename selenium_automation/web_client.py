import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_automation.driver_downloader import download_chromedriver, get_chrome_version

class WebClient:
    def __init__(self, headless=True, wait_time=1):
        self.wait_time = wait_time

        base_dir = os.path.dirname(os.path.abspath(__file__))
        drivers_dir = os.path.join(base_dir, "drivers")

        chromedriver_path = self._find_existing_driver(drivers_dir)
        if not chromedriver_path or not self._is_valid_driver(chromedriver_path):
            print("[WebClient] Đang tải chromedriver phù hợp...")
            chromedriver_path = download_chromedriver(dest_folder=drivers_dir)

        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => false,
                    });
                    window.chrome = {
                        runtime: {},
                    };
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en'],
                    });
                """
            },
        )

    def _find_existing_driver(self, drivers_dir):
        """Tìm file chromedriver có quyền thực thi trong thư mục con"""
        if not os.path.exists(drivers_dir):
            return None
        for root, dirs, files in os.walk(drivers_dir):
            for file in files:
                if "chromedriver" in file.lower():
                    full_path = os.path.join(root, file)
                    if os.access(full_path, os.X_OK):
                        return full_path
        return None

    def _is_valid_driver(self, driver_path):
        """So sánh major version của Chrome và ChromeDriver"""
        try:
            chrome_version = get_chrome_version()
            major_chrome = chrome_version.split('.')[0]

            output = subprocess.check_output([driver_path, "--version"], stderr=subprocess.STDOUT).decode().strip()
            # output ví dụ: "ChromeDriver 114.0.5735.90 ..."
            major_driver = output.split()[1].split('.')[0]

            is_valid = major_chrome == major_driver
            if not is_valid:
                print(f"[WebClient] Phiên bản Chrome ({major_chrome}) khác ChromeDriver ({major_driver})")
            return is_valid
        except Exception as e:
            print(f"[WebClient] Không kiểm tra được version chromedriver: {e}")
            return False

    def get(self, url):
        self.driver.get(url)
        time.sleep(self.wait_time)

    def find_and_fill(self, by, identifier, value):
        try:
            elem = self.driver.find_element(by, identifier)
            elem.clear()
            elem.send_keys(value)
            time.sleep(self.wait_time)
        except Exception as e:
            print(f"❌ Lỗi fill element {identifier}: {e}")

    def click(self, by, identifier):
        try:
            elem = self.driver.find_element(by, identifier)
            elem.click()
            time.sleep(self.wait_time)
        except Exception as e:
            print(f"❌ Lỗi click element {identifier}: {e}")

    def quit(self):
        self.driver.quit()
