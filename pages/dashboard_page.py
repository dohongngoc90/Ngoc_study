"""DashboardPage - màn chính /erp/desk (trang home sau khi đăng nhập)."""
from __future__ import annotations

from pages.base_page import BasePage


class DashboardPage(BasePage):
    PATH = "desk"

    USER_MENU = "a.pc-head-link.dropdown-toggle"
    # App hiển thị nút Logout luôn-hiện ở header (và một nút ẩn bên trong
    # dropdown user). Nhắm vào nút đang hiện để click ổn định.
    LOGOUT_LINK = "a.btn[href*='system-logout']"

    def wait_loaded(self):
        self.page.wait_for_url("**/desk", timeout=20000)
        return self

    def is_loaded(self) -> bool:
        return "/desk" in self.page.url

    def logout(self):
        link = self.page.locator(self.LOGOUT_LINK).first
        link.wait_for(state="visible", timeout=10000)
        link.click()
        self.page.wait_for_url("**/login", timeout=20000)
        return self
