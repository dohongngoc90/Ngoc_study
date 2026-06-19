"""DepartmentPage - màn phòng ban /erp/departments-list (Core HR > Department).

Minh họa luồng CRUD đầy đủ trên màn hình Bootstrap + DataTables + toastr -
mẫu (pattern) lặp lại ở hầu hết các trang dạng danh sách của HRM.
"""
from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class DepartmentPage(BasePage):
    PATH = "departments-list"

    # Form thêm mới
    NAME_INPUT = "#xin-form input[name='department_name']"
    # Nút Save nằm trong card-footer (ngoài <form>), submit bằng JS
    SAVE_BTN_NAME = "Save"

    # Form edit (trong modal .view-modal-data, mở khi bấm bút chì trên dòng)
    EDIT_FORM = "#edit_department"
    EDIT_NAME_FIELD = "input[name='department_name']"

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
    def add_department(self, name: str):
        self.fill(self.NAME_INPUT, name)
        self.page.get_by_role("button", name=self.SAVE_BTN_NAME).click()
        # DataTable tải lại qua AJAX sau khi lưu thành công
        self.page.wait_for_load_state("networkidle")
        return self

    def save_expecting_toast(self, name: str = "") -> str:
        """Điền tên (có thể rỗng) và bấm Save, trả về toast - dùng cho case âm.

        App validate phía server: tên rỗng -> toast 'The department_name field
        is required.' và KHÔNG thêm dòng nào vào bảng.
        """
        self.fill(self.NAME_INPUT, name)
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
    def edit_department(self, old_name: str, new_name: str):
        """Sửa tên phòng ban: mở modal edit của dòng `old_name`, đổi sang `new_name`.

        Verify live: toast 'Department updated.' và tên mới xuất hiện trong bảng.
        """
        self.search(old_name)
        self.row(old_name).first.locator(self.EDIT_BTN_IN_ROW).click()
        self.submit_edit(self.EDIT_FORM, self.EDIT_NAME_FIELD, new_name)
        self.open()  # reload để reset modal còn sót (app không tự đóng) trước bước sau
        return self

    def has_department(self, name: str) -> bool:
        self.search(name)
        return self.row(name).count() > 0

    def info_text(self) -> str:
        return self.text_of(self.INFO)

    # --- xóa (dọn dẹp) ----------------------------------------------------
    def delete_department(self, name: str):
        self.search(name)
        self.row(name).first.locator(self.DELETE_BTN_IN_ROW).click()
        modal = self.page.locator(self.DELETE_MODAL)
        modal.wait_for(state="visible")
        # dispatch_event: gửi click thẳng tới nút Confirm, tránh bị modal .show
        # còn sót che pointer (app không đóng modal sạch -> click thường hay trượt).
        modal.get_by_role("button", name=self.CONFIRM_BTN_NAME).dispatch_event("click")
        self.page.wait_for_load_state("networkidle")
        return self
