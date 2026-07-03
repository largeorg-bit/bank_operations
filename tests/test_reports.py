from pathlib import Path

import pytest

from src.reports import (spending_by_category, spending_by_weekday,
                         spending_by_workday)
from src.utils import load_transactions_dataframe


@pytest.fixture
def транзакции_df():
    return load_transactions_dataframe("data/operations.xlsx")


def test_spending_by_category(транзакции_df, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("reports").mkdir()

    result = spending_by_category(транзакции_df, "Супермаркеты", "2021-12-20")

    assert not result.empty
    assert Path("reports/spending_by_category.json").exists()


def test_spending_by_weekday(транзакции_df, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("reports").mkdir()

    result = spending_by_weekday(транзакции_df, "2021-12-20")

    assert not result.empty
    assert Path("reports/spending_by_weekday.json").exists()


def test_spending_by_workday(транзакции_df, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("reports").mkdir()

    result = spending_by_workday(транзакции_df, "2021-12-20")

    assert len(result) == 2
    assert Path("reports/spending_by_workday.json").exists()
