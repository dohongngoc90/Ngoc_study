"""Bộ test đăng nhập - hướng dữ liệu (data-driven) từ data/login_data.json.

POM sử dụng: LoginPage, DashboardPage.
"""
import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utils.data_reader import ids_for, load_cases

CASES = load_cases("login_data.json")


@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.parametrize("data", CASES, ids=ids_for(CASES))
def test_login(page, data):
    login = LoginPage(page).open()
    login.login(data["username"], data["password"])

    if data["expected"] == "success":
        DashboardPage(page).wait_loaded()
        assert "/desk" in page.url, f"[{data['case_id']}] expected dashboard, got {page.url}"
    else:
        # Đăng nhập bị từ chối phải giữ người dùng ở /login và không bao giờ vào /desk.
        page.wait_for_timeout(2500)
        assert "/desk" not in page.url, f"[{data['case_id']}] login should have failed but reached {page.url}"
        assert "/login" in page.url, f"[{data['case_id']}] expected to remain on login, got {page.url}"


@pytest.mark.login
@pytest.mark.smoke
def test_logout(auth_page):
    """Một phiên đã đăng nhập có thể đăng xuất và được đưa về /login."""
    dash = DashboardPage(auth_page).goto("desk").wait_loaded()
    dash.logout()
    assert "/login" in auth_page.url
