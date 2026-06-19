"""Fixture của Pytest: vòng đời browser, cache phiên xác thực, chụp ảnh khi fail.

Bản đồ fixture
--------------
browser        (session) một tiến trình browser cho cả lần chạy
storage_state  (session) đăng nhập MỘT lần, cache cookie/state đã xác thực
page           (function) page mới, CHƯA xác thực  -> dành cho test login
auth_page      (function) page đã xác thực sẵn qua storage_state -> test trong app

Tùy chọn khi chạy
-----------------
--headed            xem browser chạy (hoặc env HEADLESS=false)
--slowmo=<ms>       làm chậm thao tác (hoặc env SLOW_MO=<ms>)
"""
import os

import pytest
from playwright.sync_api import sync_playwright

from config.config import Config
from pages.login_page import LoginPage

VIEWPORT = {"width": 1440, "height": 900}


# ----------------------------------------------------------------------------
# Tùy chọn CLI
# ----------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", default=False,
                     help="Chạy với cửa sổ browser hiển thị")
    parser.addoption("--slowmo", action="store", default=None,
                     help="Làm chậm thao tác đi N mili-giây")


# ----------------------------------------------------------------------------
# Browser
# ----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def _playwright():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(_playwright, pytestconfig):
    headed = pytestconfig.getoption("--headed") or not Config.HEADLESS
    slowmo = pytestconfig.getoption("--slowmo")
    slow_mo = int(slowmo) if slowmo is not None else Config.SLOW_MO
    engine = getattr(_playwright, Config.BROWSER)
    browser = engine.launch(headless=not headed, slow_mo=slow_mo)
    yield browser
    browser.close()


# ----------------------------------------------------------------------------
# Xác thực - đăng nhập một lần, tái sử dụng storage state ở mọi nơi
# ----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def storage_state(browser):
    context = browser.new_context(viewport=VIEWPORT)
    page = context.new_page()
    LoginPage(page).login_as(Config.USERNAME, Config.PASSWORD)
    state = context.storage_state()
    context.close()
    return state


# ----------------------------------------------------------------------------
# Page chưa xác thực (bộ test login)
# ----------------------------------------------------------------------------
@pytest.fixture
def page(browser, request):
    context = browser.new_context(viewport=VIEWPORT)
    pg = context.new_page()
    yield pg
    _screenshot_on_failure(pg, request)
    context.close()


# ----------------------------------------------------------------------------
# Page đã xác thực (các bộ test trong app)
# ----------------------------------------------------------------------------
@pytest.fixture
def auth_page(browser, storage_state, request):
    context = browser.new_context(viewport=VIEWPORT, storage_state=storage_state)
    pg = context.new_page()
    yield pg
    _screenshot_on_failure(pg, request)
    context.close()


# ----------------------------------------------------------------------------
# Chụp ảnh màn hình khi test thất bại
# ----------------------------------------------------------------------------
def _screenshot_on_failure(pg, request):
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
        safe = request.node.name.replace("/", "_").replace("[", "_").replace("]", "")
        path = os.path.join(Config.SCREENSHOT_DIR, f"{safe}.png")
        try:
            pg.screenshot(path=path, full_page=True)
            print(f"\n[screenshot] {path}")
        except Exception as exc:  # pragma: no cover
            print(f"\n[screenshot failed] {exc}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Đưa kết quả mỗi phase ra cho fixture dưới dạng item.rep_<when>."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
