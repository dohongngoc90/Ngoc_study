---
fullstack_framework: true
fullstack_framework_init: "2026-06-19 09:40:06+07:00"
fullstack_framework_init_version: "5.0.0"
active_kits: [ba, qc]
paths:
  docs_base: "/Users/dohongngoc/DemoHRM_AT/docs"
  tasks_base: "/Users/dohongngoc/DemoHRM_AT/docs"
  qc_base: "/Users/dohongngoc/DemoHRM_AT/docs"
project: "DemoHRM / HRM Test Automation"
ba_owner: "Đỗ Hồng Ngọc <dohongngoc90@gmail.com>"
---

@~/.claude/fullstack-agent-kit/CLAUDE.md

# Project: DemoHRM / HRM Test Automation

> Framework rules:
> - **Cross-kit principles** loaded from `~/.claude/CLAUDE.md` (auto-loaded globally)
> - **Role dispatcher + workflow routing** loaded from `~/.claude/fullstack-agent-kit/CLAUDE.md` (via `@import` above)
> - **Kit-specific rules** lazy-loaded by skills via `~/.claude/{ba,qc}-agent-kit/CLAUDE.md`
>
> This file contains ONLY project-specific config and overrides.
> **Frontmatter `fullstack_framework: true` is the framework detection signal** (v5.0.0+).
> **Frontmatter `active_kits: [ba, qc]`** — chỉ BA + QC kit được bật. Dev kit disabled.

---

## Project Config

**Domain:** HRM (Human Resource Management)
**Feature slugs:** login · employee · department · dashboard

**Test stack:** Playwright (Python) + pytest, POM pattern.

| Layer | Location |
|---|---|
| Page Objects (POM) | `pages/` (`base_page.py`, `login_page.py`, `employee_page.py`, `department_page.py`, `dashboard_page.py`) |
| Test specs | `tests/` (`test_login.py`, `test_employee.py`, `test_department.py`) |
| Test data | `data/` (JSON fixtures) |
| Config | `config/config.py`, `pytest.ini`, `conftest.py` |
| Reports | `reports/` (junit.xml, report.html, screenshots) |
| Utils | `utils/data_reader.py` |

---

## Promoted Bases (resolved from frontmatter `paths`)

Single-repo project — cả 3 base đều resolve về `DemoHRM_AT/docs/`.

| Base | Path | Used by role |
|---|---|---|
| `{DOCS_BASE}` | `/Users/dohongngoc/DemoHRM_AT/docs` | BA (FRS, US, TECH, UI Spec) |
| `{TASKS_BASE}` | `/Users/dohongngoc/DemoHRM_AT/docs` | (Dev disabled — reserved) |
| `{QC_BASE}` | `/Users/dohongngoc/DemoHRM_AT/docs` | QC (test cases, RTM, defects) |

> Drafts sống ở `ai-outputs/{ba,qc}/[feature]/`; chỉ promote sang `docs/` khi approver duyệt (hook H2 gác cổng).

---

## Source Repos

| Repo | Path |
|------|------|
| App under test (HRM) | `[điền URL/đường dẫn app HRM đang test]` |
| Test automation (this) | `/Users/dohongngoc/DemoHRM_AT` |

> App HRM là hệ thống được test (BA reverse-engineer spec từ UI nếu cần — xem skill `qc:req-from-ui`). Điền base URL vào `config/config.py`.

---

## Project-specific overrides

> Chỉ thêm rule KHÁC với shared framework. Không duplicate rule chung.

## Disabled Kits
- `active_kits: [ba, qc]` → Dev kit KHÔNG được bật. Skill/agent Dev disabled cho dự án này.
