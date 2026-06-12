import functools
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def log(filename: str = "") -> Callable[[F], F]:
    """Декоратор для логирования вызова функции и ее результата."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
            except Exception as error:
                message = (
                    f"{func.__name__} error: {error}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(message, filename)
                raise

            _write_log(message, filename)
            return result

        return wrapper  # type: ignore[return-value]

    return decorator


def _write_log(message: str, filename: str) -> None:
    """Записывает сообщение в файл или выводит в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as log_file:
            log_file.write(f"{message}\n")
    else:
        print(message)
