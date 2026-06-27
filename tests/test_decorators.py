import pytest

from src.decorators import log


def test_log_успех_в_консоль(capsys):
    @log()
    def my_function(x, y):
        return x + y

    assert my_function(1, 2) == 3
    captured = capsys.readouterr()
    assert captured.out.strip() == "my_function ok"


def test_log_ошибка_в_консоль(capsys):
    @log()
    def my_function(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        my_function(1, 0)

    captured = capsys.readouterr()
    assert "my_function error: division by zero" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


def test_log_успех_в_файл(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def my_function(x, y):
        return x + y

    my_function(1, 2)
    assert log_file.read_text(encoding="utf-8").strip() == "my_function ok"


def test_log_ошибка_в_файл(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def my_function(x, y):
        raise ValueError("тип ошибки")

    with pytest.raises(ValueError):
        my_function(1, 2)

    content = log_file.read_text(encoding="utf-8").strip()
    assert "my_function error: тип ошибки" in content
    assert "Inputs: (1, 2), {}" in content


@pytest.mark.parametrize(
    "args, kwargs",
    [
        ((1, 2), {}),
        ((), {"x": 1}),
    ],
)
def test_log_с_разными_аргументами(capsys, args, kwargs):
    @log()
    def sample(*func_args, **func_kwargs):
        return func_args, func_kwargs

    sample(*args, **kwargs)
    captured = capsys.readouterr()
    assert "sample ok" in captured.out


def test_log_несколько_вызовов_в_файл(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def my_function():
        return 1

    my_function()
    my_function()
    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert lines == ["my_function ok", "my_function ok"]
