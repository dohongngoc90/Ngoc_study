"""LoginPage - màn đăng nhập /erp/login."""
from __future__ import annotations

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "login"

    # Locator (đã kiểm chứng trên DOM thật)
    USERNAME_INPUT = "#iusername"
    PASSWORD_INPUT = "#ipassword"
    SUBMIT_BTN = "#erp-form button[type=submit]"
    FORGOT_LINK = "a[href*='forgot-password']"

    def open(self):
        self.goto(self.PATH)
        self.page.locator(self.USERNAME_INPUT).wait_for(state="visible")
        return self

    def login(self, username: str, password: str):
        """Điền thông tin đăng nhập và submit. KHÔNG chờ kết quả - bên gọi tự
        assert thành công/thất bại nên cùng một method phục vụ cả hai luồng."""
        self.page.fill(self.USERNAME_INPUT, username)   # cho phép giá trị rỗng
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.locator(self.SUBMIT_BTN).click()
        return self

    def login_as(self, username: str, password: str, retries: int = 2):
        """Đăng nhập và chờ vào Dashboard. Dùng bởi fixture xác thực (auth).

        Đăng nhập bất đồng bộ (ladda spinner ~2-3s); ta chờ redirect sang /desk
        và thử lại 1 lần nếu phiên chưa được thiết lập.
        """
        for attempt in range(retries + 1):
            self.open().login(username, password)
            try:
                self.page.wait_for_url("**/desk", timeout=20000)
                return self
            except Exception:
                if attempt == retries:
                    raise
        return self

    def is_on_login(self) -> bool:
        return "/login" in self.page.url
