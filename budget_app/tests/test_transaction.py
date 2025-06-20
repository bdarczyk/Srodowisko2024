import pytest
from models.transaction import Transaction
from models.transaction_manager import TransactionManager
from storage.file_storage import FileStorage
from unittest.mock import MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def dummy_storage(tmp_path):
    # Zwraca tymczasowy FileStorage z pustym plikiem
    path = tmp_path / "test_data.json"
    return FileStorage(str(path))

def test_add_and_list_transactions(dummy_storage):
    manager = TransactionManager(dummy_storage)
    t = Transaction(100, "Jedzenie", "Test", "2025-06-19", "expense")
    manager.add_transaction(t)

    result = manager.list_transactions()
    assert len(result) == 1
    assert result[0].amount == 100
    assert result[0].category == "Jedzenie"

def test_get_balance(dummy_storage):
    manager = TransactionManager(dummy_storage)
    manager.add_transaction(Transaction(200, "Wypłata", "Test income", "2025-06-01", "income"))
    manager.add_transaction(Transaction(50, "Zakupy", "Test expense", "2025-06-02", "expense"))

    assert manager.get_balance() == 150

def test_save_called_on_add(monkeypatch):
    mock_storage = MagicMock()
    manager = TransactionManager(mock_storage)

    t = Transaction(75, "Transport", "Test", "2025-06-05", "expense")
    manager.add_transaction(t)

    mock_storage.save.assert_called_once()

def test_edit_transaction(tmp_path):
    path = tmp_path / "test_data.json"
    storage = FileStorage(str(path))
    manager = TransactionManager(storage)

    t = Transaction(50, "Rachunki", "Do edycji", "2025-06-03", "expense")
    manager.add_transaction(t)

    manager.transactions[0].amount = 99.99
    manager.save()

    new_manager = TransactionManager(FileStorage(str(path)))
    assert new_manager.transactions[0].amount == 99.99