"""Bộ test CRUD phòng ban - hướng dữ liệu từ data/department_data.json.

Mỗi case tạo một phòng ban có tên duy nhất, assert nó xuất hiện trong
DataTable, rồi xóa đi (tự dọn dẹp) và assert nó đã biến mất. Cách này giữ cho
môi trường demo công khai dùng chung luôn gọn gàng và cho phép chạy lại bộ test
mà không bị trùng dữ liệu.

POM sử dụng: DepartmentPage.
"""
import time

import pytest

from pages.department_page import DepartmentPage
from utils.data_reader import ids_for, load_cases

CASES = load_cases("department_data.json", "create")
NEG_CASES = load_cases("department_data.json", "negative")


def _unique(base: str) -> str:
    return f"{base}_{int(time.time() * 1000)}"


@pytest.mark.department
@pytest.mark.regression
@pytest.mark.parametrize("data", CASES, ids=ids_for(CASES))
def test_create_then_delete_department(auth_page, data):
    dept = DepartmentPage(auth_page).open()
    name = _unique(data["base_name"])

    # --- TẠO --------------------------------------------------------------
    dept.add_department(name)
    assert dept.has_department(name), \
        f"[{data['case_id']}] '{name}' not found in list after create"

    # --- XÓA (dọn dẹp) ----------------------------------------------------
    dept.delete_department(name)
    assert not dept.has_department(name), \
        f"[{data['case_id']}] '{name}' still present after delete"


@pytest.mark.department
@pytest.mark.regression
def test_edit_department(auth_page):
    """Edit: tạo phòng ban -> đổi tên -> tên mới xuất hiện, tên cũ biến mất -> xóa.

    Dùng 2 tên khác hẳn (không phải substring của nhau) để assert chính xác.
    """
    dept = DepartmentPage(auth_page).open()
    old = _unique("QA_EditOrig_Dept")
    new = _unique("QA_EditNew_Dept")

    dept.add_department(old)
    assert dept.has_department(old), f"tạo '{old}' thất bại"

    dept.edit_department(old, new)
    assert dept.has_department(new), f"tên mới '{new}' không thấy sau khi edit"
    assert not dept.has_department(old), f"tên cũ '{old}' vẫn còn sau khi edit"

    dept.delete_department(new)
    assert not dept.has_department(new), f"'{new}' vẫn còn sau khi xóa"


@pytest.mark.department
@pytest.mark.regression
@pytest.mark.parametrize("data", NEG_CASES, ids=ids_for(NEG_CASES))
def test_department_validation(auth_page, data):
    """Case âm: tên rỗng -> app từ chối qua toast 'department_name ... required'."""
    dept = DepartmentPage(auth_page).open()
    toast = dept.save_expecting_toast(name=data["name"])
    assert data["expect_toast_contains"].lower() in toast.lower(), \
        f"[{data['case_id']}] toast '{toast}' không chứa '{data['expect_toast_contains']}'"


@pytest.mark.department
@pytest.mark.smoke
def test_department_list_loads(auth_page):
    """Smoke: màn Department và DataTable của nó render được."""
    dept = DepartmentPage(auth_page).open()
    assert dept.is_visible(dept.TABLE)
    assert "records" in dept.info_text().lower()
