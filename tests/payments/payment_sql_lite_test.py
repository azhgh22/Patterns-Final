import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.models.payments import Payment
from playground.core.models.product import Product
from playground.infra.memory.sql_lite.payment_sql_lite_repository import PaymentSqlLiteRepository


def insert_payment(conn: Connection) -> None:
    conn.execute(
        """
        insert into payments (receipt_id, currency_id, amount)
        values ("my_receipt","GEL",10)
     """
    )
    conn.commit()


def get_payment(conn: Connection) -> Product | None:
    raw = conn.execute(
        """
        select * from payments where id = "my_receipt"
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
    assert PaymentSqlLiteRepository(conn).get_payment("1") is None
    conn.close()
