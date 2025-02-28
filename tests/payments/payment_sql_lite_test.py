import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.models.payments import Payment
from playground.infra.memory.sql_lite.payment_sql_lite_repository import PaymentSqlLiteRepository


def insert_payment(conn: Connection) -> None:
    conn.execute(
        """
        insert into payments (receipt_id, currency_id, amount)
        values ("my_receipt","GEL",10)
     """
    )
    conn.commit()


def get_payment(conn: Connection) -> Payment | None:
    raw = conn.execute(
        """
        select * from payments where receipt_id = "my_receipt"
    """
    ).fetchone()

    return Payment(raw[0], raw[1], raw[2]) if raw is not None else None


@pytest.fixture
def conn() -> Connection:
    file_path = "shop_test.db"
    if os.path.exists(file_path):
        os.remove(file_path)
    return sqlite3.connect(file_path, check_same_thread=False)


def test_env_works(conn: Connection) -> None:
    assert True
    conn.close()


def test_should_store_new_payment(conn: Connection) -> None:
    payment = Payment("my_receipt", "GEL", 10)
    PaymentSqlLiteRepository(conn).register_payment(payment)
    assert get_payment(conn) is not None
    assert get_payment(conn) == payment
    conn.close()


def test_should_not_return_non_existing_payments(conn: Connection) -> None:
    assert PaymentSqlLiteRepository(conn).get_payment("my_receipt") is None
    conn.close()


def test_should_return_existing_payments(conn: Connection) -> None:
    repo = PaymentSqlLiteRepository(conn)
    insert_payment(conn)
    assert repo.get_payment("my_receipt") == Payment("my_receipt", "GEL", 10)
    conn.close()


def test_should_return_payments_list(conn: Connection) -> None:
    repo = PaymentSqlLiteRepository(conn)
    insert_payment(conn)
    payment_list = repo.get_all_payments()
    assert len(payment_list) == 1
    assert payment_list[0] == Payment("my_receipt", "GEL", 10)
