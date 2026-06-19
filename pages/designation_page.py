"""DesignationPage - màn chức danh /erp/designation-list (Core HR > Designation).

Cùng pattern #xin-form + #xin_table như Department, nhưng form có thêm dropdown
`department` (select2, BẮT BUỘC chọn) và textarea `description` (tùy chọn).
Locator + hành vi đã kiểm chứng trực tiếp trên app Anh Tester HRM.
"""
from __future__ import annotations

from pages.base_page import BasePage


class DesignationPage(BasePage):
    PATH = "designation-list"

    # Form thêm mới
    DEPT_SELECT = "#xin-form select[name='department']"   # select2-hidden-accessible
    NAME_INPUT = "#xin-form input[name='designation_name']"
    DESC_INPUT = "#xin-form textarea[name='description']"
    SAVE_BTN_NAME = "Save"

    # Form edit (trong modal .view-modal-data, mở khi bấm bút chì trên dòng)
    EDIT_FORM = "#edit_designation"
    EDIT_NAME_FIELD = "input[name='designation_name']"

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
    def _fill_form(self, name: str, department: str = "", description: str = ""):
        """Điền form. `department` là VALUE của option (vd '2' = Development).

        Select bị select2 che nên dùng force=True để bỏ qua check hiển thị -
        khi submit, server đọc thẳng value của <select> nên vẫn đúng.
        """
        if department:
            self.page.select_option(self.DEPT_SELECT, value=department, force=True)
        self.fill(self.NAME_INPUT, name)
        if description:
            self.fill(self.DESC_INPUT, description)
        return self

    def add_designation(self, name: str, department: str = "2", description: str = ""):
        """Tạo chức danh (happy path). department mặc định '2' (Development)."""
        self._fill_form(name, department, description)
        self.page.get_by_role("button", name=self.SAVE_BTN_NAME).click()
        # DataTable tải lại qua AJAX sau khi lưu thành công
        self.page.wait_for_load_state("networkidle")
        return self

    def save_expecting_toast(self, name: str = "", department: str = "",
                             description: str = "") -> str:
        """Điền form (có thể thiếu field), bấm Save, trả về toast - dùng cho case âm."""
        self._fill_form(name, department, description)
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
    def edit_designation(self, old_name: str, new_name: str):
        """Sửa tên chức danh: mở modal edit của dòng `old_name`, đổi sang `new_name`.

        Verify live: toast 'Designation updated.' và tên mới xuất hiện trong bảng.
        """
        self.search(old_name)
        self.row(old_name).first.locator(self.EDIT_BTN_IN_ROW).click()
        self.submit_edit(self.EDIT_FORM, self.EDIT_NAME_FIELD, new_name)
        self.open()  # reload để reset modal còn sót (app không tự đóng) trước bước sau
        return self

    def has_designation(self, name: str) -> bool:
        self.search(name)
        return self.row(name).count() > 0

    def info_text(self) -> str:
        return self.text_of(self.INFO)

    # --- xóa (dọn dẹp) ----------------------------------------------------
    def delete_designation(self, name: str):
        self.search(name)
        self.row(name).first.locator(self.DELETE_BTN_IN_ROW).click()
        modal = self.page.locator(self.DELETE_MODAL)
        modal.wait_for(state="visible")
        # dispatch_event: gửi click thẳng tới nút Confirm, tránh bị modal .show
        # còn sót che pointer (app không đóng modal sạch -> click thường hay trượt).
        modal.get_by_role("button", name=self.CONFIRM_BTN_NAME).dispatch_event("click")
        self.page.wait_for_load_state("networkidle")
        return self
