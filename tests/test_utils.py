from src.utils import load_operations


def test_load_operations_из_файла():
    операции = load_operations("data/operations.json")
    assert len(операции) == 6
    assert операции[0]["id"] == 939719570


def test_load_operations_файл_не_найден(tmp_path):
    assert load_operations(str(tmp_path / "нет_такого.json")) == []


def test_load_operations_пустой_файл(tmp_path):
    путь = tmp_path / "пустой.json"
    путь.write_text("", encoding="utf-8")
    assert load_operations(str(путь)) == []


def test_load_operations_не_список(tmp_path):
    путь = tmp_path / "объект.json"
    путь.write_text('{"id": 1}', encoding="utf-8")
    assert load_operations(str(путь)) == []


def test_load_operations_битый_json(tmp_path):
    путь = tmp_path / "битый.json"
    путь.write_text("{]", encoding="utf-8")
    assert load_operations(str(путь)) == []
