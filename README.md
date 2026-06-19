# HRM ERP — Test Automation Suite (POM + DDT)

Bộ kiểm thử tự động cho **HRM ERP (Anh Tester Demo)** — https://hrm.anhtester.com/erp
Stack: **Python + Playwright (sync) + pytest**, kiến trúc **Page Object Model (POM)** + **Data-Driven Testing (DDT)**.

> ✅ Trạng thái: **32/32 test PASS** (lần chạy gần nhất ~87s, headless Chromium; chạy lặp 2 lần ổn định).
> Xem `docs/test-summary-report.md` và `reports/report.html`.

---

## 1. Cấu trúc thư mục (POM + DDT)

```
DemoHRM_AT/
├── config/
│   └── config.py              # URL, credentials, timeouts — override bằng ENV
├── pages/                     # === POM: 1 màn hình = 1 class ===
│   ├── base_page.py           # hành vi chung (goto, fill, click, toast, submit_edit…)
│   ├── login_page.py          # /erp/login
│   ├── dashboard_page.py      # /erp/desk + logout
│   ├── department_page.py     # /erp/departments-list (CRUD đầy đủ)
│   ├── designation_page.py    # /erp/designation-list (CRUD đầy đủ)
│   ├── holiday_page.py        # /erp/holidays-list (CRUD đầy đủ)
│   └── employee_page.py       # /erp/staff-list (search)
├── data/                      # === DDT: dữ liệu tách khỏi code ===
│   ├── login_data.json
│   ├── department_data.json
│   ├── designation_data.json
│   ├── holiday_data.json
│   └── employee_search_data.json
├── tests/                     # === Test scripts (1 module = 1 file) ===
│   ├── test_login.py
│   ├── test_department.py
│   ├── test_designation.py
│   ├── test_holiday.py
│   └── test_employee.py
├── .gitlab-ci.yml             # CI: GitLab
├── .github/workflows/tests.yml # CI: GitHub Actions
├── utils/
│   └── data_reader.py         # đọc JSON → cấp cho pytest.parametrize
├── reports/                   # junit.xml, report.html, screenshots/, demo/
├── conftest.py                # fixtures: browser, đăng nhập 1 lần, chụp ảnh khi fail
├── pytest.ini                 # markers, pythonpath, addopts
├── requirements.txt
└── docs/
    ├── manual-test-cases.md       # bộ test manual (map 1-1 với automation)
    └── test-summary-report.md     # báo cáo kết quả (IEEE 829 rút gọn)
```

**Nguyên tắc:**
- **POM** — locator & thao tác của mỗi màn nằm trong `pages/`; test chỉ gọi method nghiệp vụ (`login`, `add_department`, `search`…). Khi UI đổi → sửa 1 chỗ trong `pages/`.
- **DDT** — thêm 1 dòng vào `data/*.json` là có thêm 1 test case, **không phải sửa code**.

---

## 2. Cài đặt (1 lần)

```bash
cd DemoHRM_AT
pip install -r requirements.txt
python -m playwright install chromium      # tải browser cho Playwright
```

## 3. Chạy test

```bash
# Chạy toàn bộ
pytest

# Chạy theo nhóm (marker)
pytest -m smoke            # nhóm critical-path, nhanh
pytest -m regression
pytest -m login            # chỉ module đăng nhập
pytest -m department
pytest -m designation
pytest -m holiday
pytest -m employee

# Chạy 1 file / 1 case
pytest tests/test_login.py
pytest "tests/test_department.py::test_create_then_delete_department[TC_DEPT_01_basic_ascii]"

# XEM trình duyệt chạy (demo trực quan)
pytest -m smoke --headed --slowmo=500

# Báo cáo HTML
pytest --html=reports/report.html --self-contained-html
```

Khi 1 test fail, ảnh chụp màn hình tự lưu vào `reports/screenshots/`.

---

## 4. Cấu hình qua biến môi trường (không cần sửa code)

| ENV | Mặc định | Ý nghĩa |
|---|---|---|
| `HRM_BASE_URL` | `https://hrm.anhtester.com/erp` | URL gốc của AUT |
| `HRM_USERNAME` / `HRM_PASSWORD` | `admin_example` / `123456` | Tài khoản đăng nhập |
| `BROWSER` | `chromium` | `chromium` \| `firefox` \| `webkit` |
| `HEADLESS` | `true` | `false` để hiện trình duyệt |
| `SLOW_MO` | `0` | Làm chậm thao tác (ms) để quan sát |
| `DEFAULT_TIMEOUT` | `30000` | Timeout mặc định (ms) |

Ví dụ chạy trên Firefox, có giao diện:
```bash
BROWSER=firefox HEADLESS=false pytest -m smoke
```

---

## 5. Phạm vi kiểm thử (lần này)

| Module | Màn hình | Loại | Số case |
|---|---|---|---|
| Authentication | `/login`, logout | valid/invalid/empty/whitespace/SQLi/XSS + logout | 10 |
| Core HR — Department | `/departments-list` | CRUD đầy đủ (create→search→**edit**→delete) + validation | 6 |
| Core HR — Designation | `/designation-list` | CRUD đầy đủ (có dropdown department) + validation | 5 |
| Core HR — Holidays | `/holidays-list` | CRUD đầy đủ (datepicker) + validation | 5 |
| Employees | `/staff-list` | search (read-only) + headers | 6 |
| **Tổng** | | | **32** |

Tất cả test **idempotent** và **tự dọn dẹp** (bản ghi tạo ra dùng tên có hậu tố timestamp + xóa ngay) nên chạy lại bao nhiêu lần cũng an toàn trên môi trường demo dùng chung.

---

## 6. Mở rộng thêm test (công thức)

1. **Thêm case cho màn đã có** → mở `data/<module>_data.json`, thêm 1 object. Xong.
2. **Thêm màn hình mới** →
   - Tạo `pages/<ten>_page.py` kế thừa `BasePage`, khai báo locator + method.
   - Tạo `data/<ten>_data.json`.
   - Tạo `tests/test_<ten>.py` dùng `load_cases(...)` + `@pytest.mark.parametrize`.

---

## 7. CI (Continuous Integration)

Có sẵn config cho **cả 2 nền tảng**, tự chạy trên mỗi **push** và **MR/PR**:

| Nền tảng | File | Hiển thị kết quả |
|---|---|---|
| GitLab CI | `.gitlab-ci.yml` | Kết quả test ngay trong MR (`artifacts:reports:junit`) + tải `report.html` |
| GitHub Actions | `.github/workflows/tests.yml` | Artifact `test-reports` (junit + html + screenshots) |

Cả hai dùng `python:3.12` + `playwright install --with-deps chromium` (version browser luôn khớp Playwright trong `requirements.txt`). Vì test chạy trên **demo công khai**, CI **không cần deploy app**.

**Kích hoạt** (project chưa phải git repo):
```bash
git init && git add . && git commit -m "init HRM automation + CI"
# GitLab (theo setup global gitlab.metub.dev):
git remote add origin git@gitlab.metub.dev:<group>/<repo>.git && git push -u origin main
# hoặc GitHub:
git remote add origin git@github.com:<user>/<repo>.git && git push -u origin main
```
CI chạy ngay sau push. Nếu chỉ dùng 1 nền tảng → xóa file config của nền tảng còn lại.

---

## 8. Tài liệu liên quan
- `docs/manual-test-cases.md` — bộ test manual chi tiết, ánh xạ 1-1 sang automation.
- `docs/test-summary-report.md` — báo cáo kết quả lần chạy.

---
*README v2.0 | Author: Automation Engineer (QC Agent) | Owner: Đỗ Hồng Ngọc | AI-Augmented*
