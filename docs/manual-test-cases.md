# Manual Test Cases — HRM ERP (Anh Tester Demo)

> **AUT (Application Under Test):** https://hrm.anhtester.com/erp
> **Tài khoản test:** `admin_example` / `123456`
> **Phạm vi:** Authentication, Core HR > Department / Designation / Holidays (CRUD đầy đủ: Create-Read-**Update**-Delete), Employees (Search)
> **Người tạo:** Test Designer (QC Agent) · **Owner:** Đỗ Hồng Ngọc
> **Created:** 2026-06-19 09:42:00+07:00 · **Last updated:** 2026-06-19 11:04:16+07:00

Mỗi manual TC dưới đây có 1 automation script tương ứng (cột *Auto ID*) trong thư mục `tests/`.
Kỹ thuật áp dụng: **EP** (Equivalence Partitioning), **BVA** (Boundary), **Negative testing**, **State transition**, **CRUD lifecycle**.
Locator + hành vi (đặc biệt các case âm) đã **kiểm chứng trực tiếp trên app thật** qua Playwright MCP.

---

## 1. Module: Authentication (Login / Logout)

| TC ID | Tiêu đề | Tiền điều kiện | Các bước | Dữ liệu | Kết quả mong đợi | Priority | Auto ID |
|---|---|---|---|---|---|---|---|
| TC_LOGIN_01 | Đăng nhập hợp lệ | Đã ở trang `/login` | 1. Nhập username<br>2. Nhập password<br>3. Bấm **Login** | `admin_example` / `123456` | Chuyển sang `/erp/desk` (Dashboard) | High | `test_login[TC_LOGIN_01_valid_admin]` |
| TC_LOGIN_02 | Sai mật khẩu | Ở `/login` | Nhập đúng user, sai pass → Login | `admin_example` / `wrong_pass_999` | Ở lại `/login`, KHÔNG vào `/desk` | High | `test_login[TC_LOGIN_02_wrong_password]` |
| TC_LOGIN_03 | Username không tồn tại | Ở `/login` | Nhập user lạ → Login | `no_such_user_zz` / `123456` | Ở lại `/login`, bị từ chối | Medium | `test_login[TC_LOGIN_03_unknown_user]` |
| TC_LOGIN_04 | Bỏ trống username | Ở `/login` | Để trống user → Login | `` / `123456` | Không đăng nhập, ở lại `/login` | Medium | `test_login[TC_LOGIN_04_empty_username]` |
| TC_LOGIN_05 | Bỏ trống password | Ở `/login` | Để trống pass → Login | `admin_example` / `` | Không đăng nhập, ở lại `/login` | Medium | `test_login[TC_LOGIN_05_empty_password]` |
| TC_LOGIN_06 | Bỏ trống cả hai | Ở `/login` | Bấm Login khi 2 ô trống | `` / `` | Không đăng nhập, ở lại `/login` | Low | `test_login[TC_LOGIN_06_empty_both]` |
| TC_LOGIN_07 | Chống SQL Injection | Ở `/login` | Nhập payload SQLi vào username | `admin_example' OR '1'='1` / `anything` | Bị từ chối, không bypass | High | `test_login[TC_LOGIN_07_sql_injection]` |
| TC_LOGIN_08 | Username toàn khoảng trắng | Ở `/login` | Nhập 3 dấu cách → Login | `"   "` / `123456` | Không đăng nhập, ở lại `/login` | Low | `test_login[TC_LOGIN_08_whitespace_username]` |
| TC_LOGIN_09 | Chống XSS ở username | Ở `/login` | Nhập payload `<script>` → Login | `<script>alert(1)</script>` / `123456` | Bị từ chối, không thực thi script | High | `test_login[TC_LOGIN_09_xss_payload]` |
| TC_LOGOUT_01 | Đăng xuất | Đã đăng nhập | Bấm **Logout** ở header | — | Quay về `/login`, phiên kết thúc | High | `test_logout` |

> **EP/BVA:** TC_01 (happy) vs TC_02–09 (các phân vùng lỗi: sai pass, user lạ, rỗng, khoảng trắng, SQLi, XSS).

---

## 2. Module: Core HR > Department (CRUD + validation)

| TC ID | Tiêu đề | Tiền điều kiện | Các bước | Dữ liệu | Kết quả mong đợi | Priority | Auto ID |
|---|---|---|---|---|---|---|---|
| TC_DEPT_00 | Tải danh sách phòng ban | Đã đăng nhập | Mở `/departments-list` | — | DataTable hiển thị, có "Showing ... records" | High | `test_department_list_loads` |
| TC_DEPT_01 | Tạo phòng ban (ASCII) | Ở màn Department | 1. Nhập tên<br>2. **Save**<br>3. Tìm lại tên | `QA_Auto_Dept_<ts>` | Phòng ban mới xuất hiện (toast "Department added.") | High | `test_create_then_delete_department[TC_DEPT_01_basic_ascii]` |
| TC_DEPT_02 | Tạo phòng ban (tên VN) | Ở màn Department | Như trên | `Phong_Ky_Thuat_<ts>` | Tạo thành công | Medium | `...[TC_DEPT_02_unicode_vietnamese]` |
| TC_DEPT_03 | Tạo phòng ban có số | Ở màn Department | Như trên | `Dept_2026_R1_<ts>` | Tạo thành công | Low | `...[TC_DEPT_03_with_numbers]` |
| TC_DEPT_04 | Xóa phòng ban | Tồn tại phòng ban vừa tạo | 1. Icon **Delete**<br>2. **Confirm** | — | Dòng biến mất (toast "Department deleted.") | High | (bước cleanup trong test create_then_delete) |
| TC_DEPT_05 | **Sửa tên phòng ban (Update)** | Tồn tại phòng ban | 1. Icon **Edit** (bút chì)<br>2. Đổi tên trong modal<br>3. **Update** | tên cũ → tên mới | Toast "Department updated.", tên mới có trong bảng, tên cũ biến mất | High | `test_edit_department` |
| TC_DEPT_NEG_01 | **Tên rỗng bị từ chối** | Ở màn Department | Để trống tên → **Save** | `name = ""` | Toast **"The department_name field is required."**, không thêm dòng | High | `test_department_validation[TC_DEPT_NEG_01_empty_name]` |

> ⚠️ **Phát hiện (xem Issue #1):** app **CHO PHÉP tạo phòng ban trùng tên** (đã verify: tạo "Development" thứ 2 → "Department added."). Không ràng buộc unique → không viết test assert-reject (sẽ sai). Ghi nhận làm issue.

---

## 3. Module: Core HR > Designation (CRUD + validation)

> Form có dropdown **Department** (select2, bắt buộc) + **Designation Name** + Description (tùy chọn).

| TC ID | Tiêu đề | Tiền điều kiện | Các bước | Dữ liệu | Kết quả mong đợi | Priority | Auto ID |
|---|---|---|---|---|---|---|---|
| TC_DESIG_00 | Tải danh sách chức danh | Đã đăng nhập | Mở `/designation-list` | — | DataTable hiển thị | Medium | `test_designation_list_loads` |
| TC_DESIG_01 | Tạo chức danh (ASCII) | Ở màn Designation | 1. Chọn Department<br>2. Nhập tên<br>3. **Save**<br>4. Tìm lại | tên `QA_Auto_Desig_<ts>`, dept Development | Chức danh mới xuất hiện (toast "Designation added.") | High | `test_create_then_delete_designation[TC_DESIG_01_basic_ascii]` |
| TC_DESIG_02 | Tạo chức danh có mô tả | Ở màn Designation | Như trên + nhập mô tả | tên `QA_Lead_<ts>`, dept QA | Tạo thành công | Medium | `...[TC_DESIG_02_with_description]` |
| TC_DESIG_03 | Xóa chức danh | Tồn tại chức danh vừa tạo | Delete → Confirm | — | Dòng biến mất (toast "Designation deleted.") | High | (cleanup trong test create_then_delete) |
| TC_DESIG_04 | **Sửa tên chức danh (Update)** | Tồn tại chức danh | Edit → đổi tên trong modal → **Update** | tên cũ → tên mới | Toast "Designation updated.", tên mới có, tên cũ biến mất | High | `test_edit_designation` |
| TC_DESIG_NEG_01 | **Thiếu phòng ban bị từ chối** | Ở màn Designation | Nhập tên, KHÔNG chọn Department → Save | dept `""` | Toast **"The department field is required."**, không tạo | High | `test_designation_validation[TC_DESIG_NEG_01_missing_department]` |

---

## 4. Module: Core HR > Holidays (CRUD + validation)

> Form: **Event Title** + **Start Date** + **End Date** (datepicker DD-MM-YYYY) + **Description** (bắt buộc) + Publish (mặc định "Published").

| TC ID | Tiêu đề | Tiền điều kiện | Các bước | Dữ liệu | Kết quả mong đợi | Priority | Auto ID |
|---|---|---|---|---|---|---|---|
| TC_HOLIDAY_00 | Tải danh sách ngày lễ | Đã đăng nhập | Mở `/holidays-list` | — | DataTable render (có thể rỗng) | Medium | `test_holiday_list_loads` |
| TC_HOLIDAY_01 | Tạo ngày lễ (1 ngày) | Ở màn Holidays | Nhập title + ngày + mô tả → Save → tìm lại | `QA_Auto_Holiday_<ts>`, 20-06-2026 | Ngày lễ mới xuất hiện, status "Published" (toast "Holiday added.") | High | `test_create_then_delete_holiday[TC_HOLIDAY_01_single_day]` |
| TC_HOLIDAY_02 | Tạo ngày lễ (khoảng ngày) | Ở màn Holidays | Như trên, start < end | 20→25-06-2026 | Tạo thành công | Medium | `...[TC_HOLIDAY_02_date_range]` |
| TC_HOLIDAY_03 | Xóa ngày lễ | Tồn tại ngày lễ vừa tạo | Delete → Confirm | — | Dòng biến mất (toast "Holiday deleted.") | High | (cleanup trong test create_then_delete) |
| TC_HOLIDAY_04 | **Sửa tiêu đề ngày lễ (Update)** | Tồn tại ngày lễ | Edit → đổi Event Title trong modal → **Update** | tiêu đề cũ → mới | Toast "Holiday updated.", tiêu đề mới có, cũ biến mất | High | `test_edit_holiday` |
| TC_HOLIDAY_NEG_01 | **Thiếu mô tả bị từ chối** | Ở màn Holidays | Nhập title + ngày, để trống mô tả → Save | description `""` | Toast **"The description field is required."**, không tạo | High | `test_holiday_validation[TC_HOLIDAY_NEG_01_missing_description]` |

---

## 5. Module: Employees (Search — read-only)

| TC ID | Tiêu đề | Tiền điều kiện | Các bước | Dữ liệu | Kết quả mong đợi | Priority | Auto ID |
|---|---|---|---|---|---|---|---|
| TC_EMP_00 | Kiểm tra cột bảng nhân viên | Đã đăng nhập | Mở `/staff-list` | — | Đủ cột: NAME, DESIGNATION, CONTACT NUMBER, GENDER, COUNTRY, ROLE, STATUS | Medium | `test_employee_table_headers` |
| TC_EMP_01 | Tìm theo ký tự phổ biến | Ở màn Employees | Gõ `a` vào Search | `a` | Có ≥ 1 kết quả | Medium | `test_employee_search[TC_EMP_01_common_letter]` |
| TC_EMP_02 | Tìm theo tên | Ở màn Employees | Gõ `Admin` | `Admin` | Có kết quả khớp | Medium | `...[TC_EMP_02_admin]` |
| TC_EMP_03 | Tìm không có kết quả | Ở màn Employees | Gõ từ khóa vô nghĩa | `zzzz_no_match_9981` | Trạng thái rỗng (no records) | Low | `...[TC_EMP_03_no_match]` |
| TC_EMP_04 | Ô tìm kiếm rỗng | Ở màn Employees | Xóa hết Search | `` | Hiển thị toàn bộ bản ghi (verify: 12 records) | Low | `...[TC_EMP_04_empty_shows_all]` |
| TC_EMP_05 | Không phân biệt hoa/thường | Ở màn Employees | Gõ `ADMIN` (HOA) | `ADMIN` | Vẫn có kết quả (case-insensitive) | Medium | `...[TC_EMP_05_uppercase_insensitive]` |

---

## Issues phát hiện (cho BA/Dev xác nhận)

| # | Mức độ | Mô tả | Bằng chứng | Đề xuất |
|---|---|---|---|---|
| 1 | Medium | **Department cho phép trùng tên** — không ràng buộc unique. Tạo "Development" lần 2 vẫn thành công. | Verify live 2026-06-19: toast "Department added." khi tạo tên đã tồn tại; bảng có 2 dòng "Development". | BA quyết định: có nên chặn trùng tên? Nếu có → Dev thêm unique constraint; QC thêm test assert-reject. |
| 2 | Low (kỹ thuật) | **App để class `.show` trên nhiều modal cùng lúc**, không đóng modal sạch sau thao tác → overlay che pointer, gây flaky cho automation. | Verify live: sau Create/Update, nhiều `.modal.show` (edit-modal-data, view-modal-data, payroll-modal-data) cùng tồn tại. | Dev: đóng/ẩn modal đúng cách sau submit. QC đã xử lý bằng `dispatch_event("click")` + reload trang (xem `base_page.submit_edit`). |

---

## Ma trận kỹ thuật thiết kế (Technique coverage)

| Kỹ thuật | Áp dụng tại |
|---|---|
| Equivalence Partitioning | Login (valid vs invalid), Employee search (match / no-match / empty / uppercase) |
| Boundary / Negative | Login (rỗng, khoảng trắng, SQLi, XSS); validation rỗng của Department/Designation/Holiday |
| State Transition | Login → Dashboard → Logout → Login |
| CRUD lifecycle | Department, Designation, Holiday: Create → Read(search) → **Update(edit)** → Delete |
| Data-Driven (DDT) | Toàn bộ TC tham số hóa từ `data/*.json` |

---

*Manual Test Cases v2.1 | Author: Test Designer (QC Agent) | Owner: Đỗ Hồng Ngọc | AI-Augmented*
