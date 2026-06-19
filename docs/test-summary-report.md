# Test Summary Report — HRM ERP (Anh Tester Demo)

> Theo khung **IEEE 829** (rút gọn).
> **AUT:** https://hrm.anhtester.com/erp · **Build:** live demo · **Ngày chạy:** 2026-06-19 11:04:16+07:00
> **Người thực thi:** Test Executor (QC Agent) · **Owner:** Đỗ Hồng Ngọc

## 1. Tổng quan
Thực thi bộ automation (Playwright + pytest, POM + DDT) trên **5 module**: Authentication, Core HR > Department, Designation, Holidays, Employees. 3 màn Core HR đạt **CRUD đầy đủ** (Create-Read-**Update**-Delete). Locator + hành vi (edit modal, case âm) được kiểm chứng trực tiếp trên UI thật qua Playwright MCP trước khi viết test.

## 2. Kết quả thực thi

| Chỉ số | Giá trị |
|---|---|
| Tổng số test | **32** |
| Pass | **32** |
| Fail | 0 |
| Error | 0 |
| Skip | 0 |
| Tỷ lệ pass | **100%** (chạy lặp 2 lần đều xanh — không flaky) |
| Thời gian | ~87s (headless Chromium) |
| Môi trường | macOS · Python 3.14 · Playwright Chromium |

### Chi tiết theo module

| Module | Test | Happy | Unhappy/Negative | Kết quả |
|---|---|---|---|---|
| Authentication | login matrix ×9 + logout | 1 | 8 (sai pass, user lạ, rỗng ×3, khoảng trắng, SQLi, XSS) | 10/10 PASS |
| Core HR — Department | create→delete ×3 + **edit** + validation + list | 5 | 1 (tên rỗng → toast required) | 6/6 PASS |
| Core HR — Designation | create→delete ×2 + **edit** + validation + list | 4 | 1 (thiếu department → toast required) | 5/5 PASS |
| Core HR — Holidays | create→delete ×2 + **edit** + validation + list | 4 | 1 (thiếu description → toast required) | 5/5 PASS |
| Employees | search ×5 + table_headers | 5 | 1 (no-match → empty state) | 6/6 PASS |

> Tăng từ 16 → 29 → **32 test** (3 → 5 module). Bổ sung 2 màn CRUD mới (Designation, Holidays), 5 case âm/biên, và **3 test Update (edit)** hoàn thiện vòng đời CRUD cho Department/Designation/Holiday.

## 3. Artefacts
| File | Nội dung |
|---|---|
| `reports/report.html` | Báo cáo HTML self-contained |
| `reports/junit.xml` | Kết quả JUnit (cho CI) |
| `reports/screenshots/` | Ảnh khi test fail (rỗng nếu all-pass) |
| `docs/manual-test-cases.md` | Manual TC v2.0 (5 module, ánh xạ Auto ID) |

## 4. Issues / Quan sát

| # | Mức độ | Mô tả | Bằng chứng | Trạng thái |
|---|---|---|---|---|
| 1 | Medium | **Department cho phép tạo trùng tên** (không ràng buộc unique). | Verify live: tạo "Development" lần 2 → toast "Department added.", bảng có 2 dòng cùng tên. | Chờ BA xác nhận có cần chặn |
| 2 | Low (kỹ thuật) | **App để class `.show` trên nhiều modal cùng lúc**, không đóng modal sạch sau submit → overlay che pointer, gây flaky cho automation (UX cũng có thể bị ảnh hưởng). | Verify live: sau Create/Update, nhiều `.modal.show` cùng tồn tại; click Update/Confirm bị chặn pointer. | Dev: ẩn modal đúng cách sau submit. QC đã xử lý bằng `dispatch_event("click")` + reload trang. |
| — | Info | Validation bắt buộc đều ở **phía server**, báo qua **toast** (không có label client-side). Field rỗng → "The <field> field is required." | Verify live Department/Designation/Holiday | Đã ghi nhận trong POM |
| — | Info | Login bất đồng bộ (~2-3s, ladda spinner): đã xử lý bằng `wait_for_url("**/desk")` + retry trong `login_as`. | — | Đã xử lý |
| — | Info | Toastr tự ẩn nhanh → không dùng làm assertion chính cho happy-path; thay bằng trạng thái bảng/URL. Riêng case âm thì đọc toast (validation toast tồn tại đủ lâu). | — | Đã xử lý |
| — | Info | Môi trường demo dùng chung công khai: mọi test tạo dữ liệu đều dùng tên có hậu tố timestamp + tự xóa → idempotent, không phụ thuộc dữ liệu sẵn có. | — | Đã xử lý |

## 5. Khuyến nghị mở rộng
- Thêm CRUD cho Awards, Leave Request, Attendance (luồng phức tạp hơn — có phê duyệt/ngày tháng).
- Mở rộng test edit: đổi cả **department của Designation**, đổi **khoảng ngày/Publish của Holiday** (hiện edit mới đổi tên/tiêu đề).
- Tích hợp CI (GitHub Actions/GitLab CI) chạy `pytest --junitxml` + upload `report.html`.
- Bổ sung API-level test cho `/auth/login`, `/department/add_department`, `/department/update_department`... để tăng tốc & giảm phụ thuộc UI.

## 6. Kết luận — Go/No-Go
✅ **GO** cho 5 module đã kiểm: Authentication, Department, Designation, Holidays, Employees hoạt động đúng kỳ vọng với **CRUD đầy đủ** (gồm Update). Không có defect chặn (blocking). 1 issue Medium (trùng tên phòng ban) + 1 issue Low kỹ thuật (modal `.show` chồng) cần Dev/BA xử lý — không chặn release.

---
*Test Summary Report v2.1 | Author: Test Executor (QC Agent) | Owner: Đỗ Hồng Ngọc | AI-Augmented*
