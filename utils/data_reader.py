"""Helper cho Data-Driven Testing (DDT).

Đọc dữ liệu test tách rời từ `data/*.json` để logic test tách biệt khỏi dữ liệu
test. Thêm một dòng vào file JSON -> xuất hiện một case parametrize mới, không cần
sửa code.
"""
import json
import os

from config.config import Config


def load_json(filename: str):
    """Đọc và parse một file JSON từ thư mục data."""
    path = os.path.join(Config.DATA_DIR, filename)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_cases(filename: str, key: str | None = None) -> list:
    """Trả về danh sách các dict case.

    `key` chọn một mảng con khi gốc JSON là một object, ví dụ
    load_cases("department_data.json", "create").
    """
    data = load_json(filename)
    if key is not None:
        data = data[key]
    if not isinstance(data, list):
        raise ValueError(f"{filename} (key={key}) did not resolve to a list")
    return data


def ids_for(cases: list, id_field: str = "case_id") -> list:
    """Tạo id parametrize cho pytest từ danh sách case."""
    return [str(c.get(id_field, i)) for i, c in enumerate(cases)]
