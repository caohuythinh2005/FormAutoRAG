import os
import platform
import subprocess
import stat
import zipfile
import requests
from pathlib import Path

# Helper lấy version Chrome cài trên máy
def get_chrome_version():
    system = platform.system().lower()

    def _try_run_command(cmd):
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
            return output
        except Exception:
            return None

    version = None
    if system == "windows":
        paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ]
        for path in paths:
            if os.path.exists(path):
                version_output = _try_run_command([path, "--version"])
                if version_output:
                    version = version_output
                    break
        if not version:
            try:
                reg_output = subprocess.check_output(
                    r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                    shell=True, stderr=subprocess.DEVNULL).decode()
                for line in reg_output.splitlines():
                    if "version" in line.lower():
                        version = line.split()[-1]
                        break
            except Exception:
                pass

    elif system == "darwin":
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            version_output = _try_run_command([chrome_path, "--version"])
            version = version_output

    elif system == "linux":
        for cmd in [["google-chrome", "--version"], ["chromium-browser", "--version"], ["chromium", "--version"]]:
            version_output = _try_run_command(cmd)
            if version_output:
                version = version_output
                break

    if not version:
        raise RuntimeError("Không tìm thấy phiên bản Chrome trên hệ thống.")

    import re
    m = re.search(r"\d+\.\d+\.\d+\.\d+", version)
    if m:
        return m.group(0)
    else:
        raise RuntimeError(f"Không thể phân tích version Chrome: {version}")

def get_platform_arch():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if machine in ["amd64", "x86_64"]:
        arch = "x86_64"
    elif machine in ["arm64", "aarch64"]:
        arch = "arm64"
    elif machine in ["x86", "i386", "i686"]:
        arch = "x86"
    else:
        arch = machine

    if system == "darwin":
        system = "mac-x64" if arch == "x86_64" else "mac-arm64"
    elif system == "linux":
        system = "linux64"
    elif system.startswith("win"):
        system = "win64" if arch in ["x86_64", "amd64"] else "win32"
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    return system

def download_chromedriver(dest_folder: str = "./selenium_automation/drivers") -> str:
    chrome_version = get_chrome_version()
    print(f"Detected Chrome version: {chrome_version}")

    platform_name = get_platform_arch()
    print(f"Detected platform: {platform_name}")

    base_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/{platform_name}"
    chromedriver_zip_name = f"chromedriver-{platform_name}.zip"
    url = f"{base_url}/{chromedriver_zip_name}"
    print(f"Download URL: {url}")

    dest_folder = Path(dest_folder)
    dest_folder.mkdir(parents=True, exist_ok=True)

    zip_path = dest_folder / chromedriver_zip_name

    # Nếu driver đã có sẵn, trả về luôn
    chromedriver_path = dest_folder / "chromedriver"
    if platform.system().lower() == "windows":
        chromedriver_path = dest_folder / "chromedriver.exe"

    if chromedriver_path.exists():
        print(f"ChromeDriver already downloaded at {chromedriver_path}")
        return str(chromedriver_path)

    print(f"Downloading ChromeDriver ...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Extracting {zip_path} ...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        print("Files in zip:")
        for member in zip_ref.namelist():
            print(" -", member)
        zip_ref.extractall(dest_folder)

    zip_path.unlink()  # xóa file zip

    # Di chuyển chromedriver ra ngoài cùng nếu nằm trong thư mục con
    extracted_driver = None
    for path in dest_folder.glob("**/chromedriver*"):
        if path.is_file():
            extracted_driver = path
            break

    if not extracted_driver:
        raise FileNotFoundError("Chromedriver executable not found after extraction!")

    # Nếu file chromedriver không nằm ở dest_folder trực tiếp thì di chuyển nó
    if extracted_driver.parent != dest_folder:
        target_path = dest_folder / extracted_driver.name
        extracted_driver.rename(target_path)
        extracted_driver = target_path

    # Set quyền chạy cho Linux/mac
    if platform.system().lower() != "windows":
        st = os.stat(extracted_driver)
        os.chmod(extracted_driver, st.st_mode | stat.S_IEXEC)

    print(f"ChromeDriver ready at {extracted_driver}")
    return str(extracted_driver)


if __name__ == "__main__":
    path = download_chromedriver()
    print("Driver path:", path)
