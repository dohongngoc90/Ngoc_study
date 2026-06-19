"""Bộ test tìm kiếm nhân viên - hướng dữ liệu từ data/employee_search_data.json.

Luồng chỉ-đọc trên DataTable của màn Employees.

POM sử dụng: EmployeePage.
"""
import pytest

from pages.employee_page import EmployeePage
from utils.data_reader import ids_for, load_cases

CASES = load_cases("employee_search_data.json", "search")

EXPECTED_HEADERS = ["NAME", "DESIGNATION", "CONTACT NUMBER", "GENDER",
                    "COUNTRY", "ROLE", "STATUS"]


@pytest.mark.employee
@pytest.mark.regression
@pytest.mark.parametrize("data", CASES, ids=ids_for(CASES))
def test_employee_search(auth_page, data):
    emp = EmployeePage(auth_page).open()
    emp.search(data["term"])

    if data["expect_results"]:
        assert not emp.is_empty_state(), \
            f"[{data['case_id']}] expected results for '{data['term']}' but got empty state"
        assert emp.total_filtered() > 0
    else:
        assert emp.is_empty_state(), \
            f"[{data['case_id']}] expected empty state for '{data['term']}'"


@pytest.mark.employee
@pytest.mark.smoke
def test_employee_table_headers(auth_page):
    """Smoke: bảng Employees có đủ các cột như kỳ vọng."""
    emp = EmployeePage(auth_page).open()
    headers = [h.upper() for h in emp.column_headers()]
    for expected in EXPECTED_HEADERS:
        assert expected in headers, f"Missing column: {expected} (got {headers})"
