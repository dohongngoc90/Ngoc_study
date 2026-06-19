"""Bộ test CRUD chức danh - hướng dữ liệu từ data/designation_data.json.

Mỗi case tạo một chức danh tên duy nhất (gắn phòng ban), assert nó xuất hiện
trong DataTable, rồi xóa (tự dọn dẹp). Case âm kiểm tra validation phía server
khi thiếu phòng ban bắt buộc.

POM sử dụng: DesignationPage.
"""
import time

import pytest

from pages.designation_page import DesignationPage
from utils.data_reader import ids_for, load_cases

CREATE_CASES = load_cases("designation_data.json", "create")
NEG_CASES = load_cases("designation_data.json", "negative")


def _unique(base: str) -> str:
    return f"{base}_{int(time.time() * 1000)}"


@pytest.mark.designation
@pytest.mark.regression
@pytest.mark.parametrize("data", CREATE_CASES, ids=ids_for(CREATE_CASES))
def test_create_then_delete_designation(auth_page, data):
    desig = DesignationPage(auth_page).open()
    name = _unique(data["base_name"])

    # --- TẠO --------------------------------------------------------------
    desig.add_designation(name, department=data["department"],
                          description=data.get("description", ""))
    assert desig.has_designation(name), \
        f"[{data['case_id']}] '{name}' không thấy trong danh sách sau khi tạo"

    # --- XÓA (dọn dẹp) ----------------------------------------------------
    desig.delete_designation(name)
    assert not desig.has_designation(name), \
        f"[{data['case_id']}] '{name}' vẫn còn sau khi xóa"


@pytest.mark.designation
@pytest.mark.regression
def test_edit_designation(auth_page):
    """Edit: tạo chức danh -> đổi tên -> tên mới xuất hiện, tên cũ biến mất -> xóa."""
    desig = DesignationPage(auth_page).open()
    old = _unique("QA_EditOrig_Desig")
    new = _unique("QA_EditNew_Desig")

    desig.add_designation(old, department="2")
    assert desig.has_designation(old), f"tạo '{old}' thất bại"

    desig.edit_designation(old, new)
    assert desig.has_designation(new), f"tên mới '{new}' không thấy sau khi edit"
    assert not desig.has_designation(old), f"tên cũ '{old}' vẫn còn sau khi edit"

    desig.delete_designation(new)
    assert not desig.has_designation(new), f"'{new}' vẫn còn sau khi xóa"


@pytest.mark.designation
@pytest.mark.regression
@pytest.mark.parametrize("data", NEG_CASES, ids=ids_for(NEG_CASES))
def test_designation_validation(auth_page, data):
    """Case âm: thiếu phòng ban bắt buộc -> app từ chối qua toast lỗi."""
    desig = DesignationPage(auth_page).open()
    name = _unique(data["base_name"])

    toast = desig.save_expecting_toast(name=name, department=data["department"])
    assert data["expect_toast_contains"].lower() in toast.lower(), \
        f"[{data['case_id']}] toast '{toast}' không chứa '{data['expect_toast_contains']}'"
    # Đảm bảo không có bản ghi rác nào được tạo
    assert not desig.has_designation(name), \
        f"[{data['case_id']}] '{name}' bị tạo dù lẽ ra phải bị từ chối"


@pytest.mark.designation
@pytest.mark.smoke
def test_designation_list_loads(auth_page):
    """Smoke: màn Designation và DataTable của nó render được."""
    desig = DesignationPage(auth_page).open()
    assert desig.is_visible(desig.TABLE)
    assert "records" in desig.info_text().lower()
