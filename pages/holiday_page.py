"""HolidayPage - màn ngày lễ /erp/holidays-list (Core HR > Holidays).

Cùng pattern #xin-form + #xin_table. Form gồm: event_name, start_date + end_date
(datepicker, định dạng DD-MM-YYYY), description (BẮT BUỘC) và select2 is_publish
(mặc định "Published"). Locator + hành vi đã kiểm chứng trực tiếp trên app.
"""
from __future__ import annotations

from pages.base_page import BasePage


class HolidayPage(BasePage):
    PATH = "holidays-list"

    # Form thêm mới
    EVENT_INPUT = "#xin-form input[name='event_name']"
    START_DATE = "#xin-form input[name='start_date']"
    END_DATE = "#xin-form input[name='end_date']"
    DESC_INPUT = "#xin-form textarea[name='description']"
    SAVE_BTN_NAME = "Save"

    # Form edit (trong modal .edit-modal-data, mở khi bấm bút chì trên dòng)
    EDIT_FORM = "#edit_holiday"
    EDIT_EVENT_FIELD = "input[name='event_name']"

    # DataTable
    TABLE = "#xin_table"
    TABLE_ROWS = "#xin_table tbody tr"
    SEARCH_INPUT = "#xin_table_filter input"
    INFO = "#xin_table_info"

    # Modal xác nhận xóa
    DELETE_MODAL = ".delete-modal"
    DELETE_BTN_IN_ROW = "button.delete"
    CONFIRM_BTN_NAME = "Confirm"

    def open(self):
        self.goto(self.PATH)
        self.page.locator(self.TABLE).wait_for(state="visible")
        return self

    # --- tạo mới ----------------------------------------------------------
    def _fill_form(self, event: str, start: str = "", end: str = "",
                   description: str = ""):
        """Điền form. Ô ngày là datepicker -> fill xong nhấn Escape để đóng
        overlay, tránh lịch che mất nút Save."""
        self.fill(self.EVENT_INPUT, event)
        if start:
            self.page.locator(self.START_DATE).fill(start)
            self.page.keyboard.press("Escape")
        if end:
            self.page.locator(self.END_DATE).fill(end)
            self.page.keyboard.press("Escape")
        if description:
            self.fill(self.DESC_INPUT, description)
        return self

    def add_holiday(self, event: str, start: str, end: str, description: str):
        """Tạo ngày lễ (happy path). is_publish giữ mặc định 'Published'."""
        self._fill_form(event, start, end, description)
        self.page.get_by_role("button", name=self.SAVE_BTN_NAME).click()
        # DataTable tải lại qua AJAX sau khi lưu thành công
        self.page.wait_for_load_state("networkidle")
        return self

    def save_expecting_toast(self, event: str = "", start: str = "", end: str = "",
                             description: str = "") -> str:
        """Điền form (có thể thiếu field), bấm Save, trả về toast - dùng cho case âm."""
        self._fill_form(event, start, end, description)
        self.page.get_by_role("button", name=self.SAVE_BTN_NAME).click()
        return self.toast_text()

    # --- đọc / tìm kiếm ---------------------------------------------------
    def search(self, term: str):
        box = self.page.locator(self.SEARCH_INPUT)
        box.fill("")
        box.fill(term)
        self.page.wait_for_timeout(600)  # debounce của bộ lọc client-side DataTables
        return self

    def row(self, name: str):
        return self.page.locator(self.TABLE_ROWS, has_text=name)

    # --- cập nhật (edit) --------------------------------------------------
    def edit_holiday(self, old_name: str, new_name: str):
        """Sửa tiêu đề ngày lễ: mở modal edit của dòng `old_name`, đổi event_name.

        Verify live: toast 'Holiday updated.' và tiêu đề mới xuất hiện trong bảng.
        """
        self.search(old_name)
        self.row(old_name).first.locator(self.EDIT_BTN_IN_ROW).click()
        self.submit_edit(self.EDIT_FORM, self.EDIT_EVENT_FIELD, new_name)
        self.open()  # reload để reset modal còn sót (app không tự đóng) trước bước sau
        return self

    def has_holiday(self, name: str) -> bool:
        self.search(name)
        return self.row(name).count() > 0

    def info_text(self) -> str:
        return self.text_of(self.INFO)

    # --- xóa (dọn dẹp) ----------------------------------------------------
    def delete_holiday(self, name: str):
        self.search(name)
        self.row(name).first.locator(self.DELETE_BTN_IN_ROW).click()
        modal = self.page.locator(self.DELETE_MODAL)
        modal.wait_for(state="visible")
        # dispatch_event: gửi click thẳng tới nút Confirm, tránh bị modal .show
        # còn sót che pointer (app không đóng modal sạch -> click thường hay trượt).
        modal.get_by_role("button", name=self.CONFIRM_BTN_NAME).dispatch_event("click")
        self.page.wait_for_load_state("networkidle")
        return self
