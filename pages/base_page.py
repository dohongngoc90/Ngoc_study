"""BasePage - thành phần dùng chung cho mọi Page Object (gốc của POM).

Giữ handle `Page` của Playwright và bọc lại các thao tác phổ biến nhất, nhờ đó
các page object cụ thể gọn nhẹ và đọc gần như một test script.
"""
from __future__ import annotations

from playwright.sync_api import Page

from config.config import Config


class BasePage:
    # Container thông báo toastr dùng chung cho toàn bộ app HRM
    TOAST_CONTAINER = "#toast-container"
    # Nút edit (bút chì) trên mỗi dòng DataTable - chung cho mọi màn list/CRUD
    EDIT_BTN_IN_ROW = "button.btn-light-primary"

    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(Config.DEFAULT_TIMEOUT)
        self.page.set_default_navigation_timeout(Config.NAV_TIMEOUT)

    # --- điều hướng -------------------------------------------------------
    def goto(self, path: str = ""):
        """Điều hướng tới một path tương đối của app (hoặc một URL tuyệt đối)."""
        url = path if path.startswith("http") else f"{Config.BASE_URL}/{path.lstrip('/')}"
        self.page.goto(url, wait_until="domcontentloaded")
        return self

    @property
    def url(self) -> str:
        return self.page.url

    # --- thao tác cơ bản --------------------------------------------------
    def fill(self, selector: str, value: str):
        loc = self.page.locator(selector)
        loc.wait_for(state="visible")
        loc.fill(value)

    def click(self, selector: str):
        self.page.locator(selector).click()

    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).inner_text().strip()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    # --- helper cho luồng edit (modal) ------------------------------------
    def submit_edit(self, edit_form: str, field_selector: str, new_value: str):
        """Trong modal edit (đã mở sẵn): xóa field rồi điền giá trị mới, bấm Update.

        Class modal khác nhau giữa các màn (.view-modal-data ở Department/Designation,
        .edit-modal-data ở Holiday) nên định vị modal qua ancestor của form edit để
        dùng chung được. Nội dung modal nạp qua AJAX -> chờ field visible trước khi điền.
        """
        modal = self.page.locator(edit_form).locator(
            "xpath=ancestor::div[contains(@class,'modal')][1]")
        field = modal.locator(field_selector)
        field.wait_for(state="visible")
        field.fill("")
        field.fill(new_value)
        # App để class .show trên NHIỀU modal cùng lúc -> nút Update hay bị modal
        # khác che pointer-event, click thường bị chặn/trượt. dispatch_event gửi
        # click thẳng tới đúng phần tử, bỏ qua overlay (giống DOM .click()).
        modal.get_by_role("button", name="Update").dispatch_event("click")
        # Chờ toast xác nhận (vd 'Department updated.') trước khi reload: nó báo AJAX
        # update đã xong. Nếu reload ngay (như trước) khi request còn đang bay, trên CI
        # chậm request bị hủy -> update mất -> flaky. Chờ toast loại bỏ race này.
        self.page.locator(self.TOAST_CONTAINER).wait_for(state="visible", timeout=10000)
        self.page.wait_for_load_state("networkidle")
        return self

    # --- helper cho toastr ------------------------------------------------
    def toast_text(self, timeout: int = 4000) -> str:
        """Trả về nội dung thông báo toastr, hoặc '' nếu không kịp xuất hiện.

        Toastr tự ẩn nhanh nên ta chỉ đọc khi có cơ hội, không bao giờ fail cứng
        khi nó vắng mặt - trạng thái bảng/URL mới là assertion chính thống.
        """
        try:
            toast = self.page.locator(self.TOAST_CONTAINER)
            toast.wait_for(state="visible", timeout=timeout)
            return toast.inner_text().strip()
        except Exception:
            return ""
