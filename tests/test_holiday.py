"""Bộ test CRUD ngày lễ - hướng dữ liệu từ data/holiday_data.json.

Mỗi case tạo một ngày lễ tên duy nhất (1 ngày hoặc theo khoảng ngày), assert nó
xuất hiện trong DataTable, rồi xóa (tự dọn dẹp). Case âm kiểm tra validation phía
server khi thiếu mô tả bắt buộc.

POM sử dụng: HolidayPage.
"""
import time

import pytest

from pages.holiday_page import HolidayPage
from utils.data_reader import ids_for, load_cases

CREATE_CASES = load_cases("holiday_data.json", "create")
NEG_CASES = load_cases("holiday_data.json", "negative")


def _unique(base: str) -> str:
    return f"{base}_{int(time.time() * 1000)}"


@pytest.mark.holiday
@pytest.mark.regression
@pytest.mark.parametrize("data", CREATE_CASES, ids=ids_for(CREATE_CASES))
def test_create_then_delete_holiday(auth_page, data):
    holiday = HolidayPage(auth_page).open()
    name = _unique(data["base_name"])

    # --- TẠO --------------------------------------------------------------
    holiday.add_holiday(name, data["start_date"], data["end_date"], data["description"])
    assert holiday.has_holiday(name), \
        f"[{data['case_id']}] '{name}' không thấy trong danh sách sau khi tạo"

    # --- XÓA (dọn dẹp) ----------------------------------------------------
    holiday.delete_holiday(name)
    assert not holiday.has_holiday(name), \
        f"[{data['case_id']}] '{name}' vẫn còn sau khi xóa"


@pytest.mark.holiday
@pytest.mark.regression
def test_edit_holiday(auth_page):
    """Edit: tạo ngày lễ -> đổi tiêu đề -> tiêu đề mới xuất hiện, cũ biến mất -> xóa."""
    holiday = HolidayPage(auth_page).open()
    old = _unique("QA_EditOrig_Holiday")
    new = _unique("QA_EditNew_Holiday")

    holiday.add_holiday(old, "20-06-2026", "20-06-2026", "Ngày lễ probe edit")
    assert holiday.has_holiday(old), f"tạo '{old}' thất bại"

    holiday.edit_holiday(old, new)
    assert holiday.has_holiday(new), f"tiêu đề mới '{new}' không thấy sau khi edit"
    assert not holiday.has_holiday(old), f"tiêu đề cũ '{old}' vẫn còn sau khi edit"

    holiday.delete_holiday(new)
    assert not holiday.has_holiday(new), f"'{new}' vẫn còn sau khi xóa"


@pytest.mark.holiday
@pytest.mark.regression
@pytest.mark.parametrize("data", NEG_CASES, ids=ids_for(NEG_CASES))
def test_holiday_validation(auth_page, data):
    """Case âm: thiếu mô tả bắt buộc -> app từ chối qua toast lỗi."""
    holiday = HolidayPage(auth_page).open()
    name = _unique(data["base_name"])

    toast = holiday.save_expecting_toast(
        event=name, start=data["start_date"], end=data["end_date"],
        description=data["description"])
    assert data["expect_toast_contains"].lower() in toast.lower(), \
        f"[{data['case_id']}] toast '{toast}' không chứa '{data['expect_toast_contains']}'"
    assert not holiday.has_holiday(name), \
        f"[{data['case_id']}] '{name}' bị tạo dù lẽ ra phải bị từ chối"


@pytest.mark.holiday
@pytest.mark.smoke
def test_holiday_list_loads(auth_page):
    """Smoke: màn Holidays và DataTable của nó render được."""
    holiday = HolidayPage(auth_page).open()
    assert holiday.is_visible(holiday.TABLE)
    info = holiday.info_text().lower()
    assert "records" in info or "no records" in info
