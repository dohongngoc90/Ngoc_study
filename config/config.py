"""Cấu hình tập trung cho bộ automation HRM.

Mọi giá trị đều có thể override qua biến môi trường để cùng một bộ test chạy được
ở local (headed, chậm) hoặc trên CI (headless, nhanh) mà không cần sửa code.
"""
import os


def _bool(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


class Config:
    # --- Ứng dụng được test (AUT) -----------------------------------------
    BASE_URL = os.getenv("HRM_BASE_URL", "https://hrm.anhtester.com/erp").rstrip("/")
    LOGIN_URL = f"{BASE_URL}/login"

    # --- Thông tin đăng nhập (tài khoản demo công khai của Anh Tester) ----
    USERNAME = os.getenv("HRM_USERNAME", "admin_example")
    PASSWORD = os.getenv("HRM_PASSWORD", "123456")

    # --- Browser / chế độ chạy --------------------------------------------
    BROWSER = os.getenv("BROWSER", "chromium")          # chromium | firefox | webkit
    HEADLESS = _bool("HEADLESS", "true")                # HEADLESS=false để xem chạy
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))            # độ trễ (ms) giữa các thao tác

    # --- Timeout (ms) -----------------------------------------------------
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    NAV_TIMEOUT = int(os.getenv("NAV_TIMEOUT", "45000"))

    # --- Đường dẫn --------------------------------------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    SCREENSHOT_DIR = os.path.join(REPORT_DIR, "screenshots")
