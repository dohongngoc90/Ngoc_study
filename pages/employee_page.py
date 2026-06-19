"""EmployeePage - màn nhân viên /erp/staff-list (Employees).

Luồng chỉ-đọc: tìm kiếm + assert trạng thái kết quả trên DataTable.
"""
from __future__ import annotations

import re

from pages.base_page import BasePage


class EmployeePage(BasePage):
    PATH = "staff-list"

    TABLE = "#xin_table"
    TABLE_ROWS = "#xin_table tbody tr"
    SEARCH_INPUT = "#xin_table_filter input"
    INFO = "#xin_table_info"
    HEADERS = "#xin_table thead th"

    def open(self):
        self.goto(self.PATH)
        self.page.locator(self.TABLE).wait_for(state="visible")
        return self

    def search(self, term: str):
        box = self.page.locator(self.SEARCH_INPUT)
        box.fill("")
        box.fill(term)
        self.page.wait_for_timeout(800)  # chờ bộ lọc phía server / client xử lý
        return self

    def info_text(self) -> str:
        return self.text_of(self.INFO)

    def total_filtered(self) -> int:
        """Bóc tách 'Showing 1 to N of M records' -> M (0 khi trạng thái rỗng)."""
        info = self.info_text()
        m = re.search(r"of\s+([\d,]+)\s+", info)
        if m:
            return int(m.group(1).replace(",", ""))
        return 0

    def is_empty_state(self) -> bool:
        info = self.info_text().lower()
        return "no records" in info or self.total_filtered() == 0

    def column_headers(self) -> list[str]:
        return [h.strip() for h in self.page.locator(self.HEADERS).all_inner_texts()]
