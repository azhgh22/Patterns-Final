import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.enums.shift_state import ShiftState
from playground.core.models.shift import Shift
from playground.infra.memory.sql_lite.receipt_sql_lite_repository import ReceiptSqlLiteRepository
from playground.infra.memory.sql_lite.shift_sql_lite_repository import ShiftSqlLiteRepository


@pytest.fixture
def conn() -> Connection:
    file_path = "shop_test.db"
    if os.path.exists(file_path):
        os.remove(file_path)
    return sqlite3.connect(file_path, check_same_thread=False)


def insert_shift(conn: Connection, shift: Shift) -> None:
    conn.execute(
        """
        insert into shifts (id,status)
        values(?,?)
    """,
        (shift.id, str(shift.state)),
    )
    conn.commit()


def get_shift_status(conn: Connection, shift_id: str) -> str:
    return conn.execute(f"""
                select status from shifts 
                where id='{shift_id}';
            """).fetchone()[0]


def get_shift_receipts(conn: Connection, shift_id: str) -> list[str]:
    return conn.execute(f"""
                    select receipt_id from shift_receipt_linker 
                    where shift_id='{shift_id}';
                """).fetchall()


def test_env_works(conn: Connection) -> None:
    ShiftSqlLiteRepository(conn, ReceiptSqlLiteRepository(conn))
    insert_shift(conn, Shift("1", ShiftState.OPEN, []))
    assert True
    conn.close()


def test_should_return_none_open_shift_id(conn: Connection) -> None:
    repo = ShiftSqlLiteRepository(conn, ReceiptSqlLiteRepository(conn))
    assert repo.get_open_shift_id() is None
    conn.close()


def test_should_return_open_shift_id(conn: Connection) -> None:
    repo = ShiftSqlLiteRepository(conn, ReceiptSqlLiteRepository(conn))
    insert_shift(conn, Shift("1", ShiftState.OPEN, []))
    assert repo.get_open_shift_id() == "1"
    conn.close()


def test_should_change_shift_status(conn: Connection) -> None:
    repo = ShiftSqlLiteRepository(conn, ReceiptSqlLiteRepository(conn))
    insert_shift(conn, Shift("1", ShiftState.OPEN, []))
    repo.close("1")
    assert get_shift_status(conn, "1") == str(ShiftState.CLOSED)
    conn.close()


def test_should_add_new_shift(conn: Connection) -> None:
    repo = ShiftSqlLiteRepository(conn, ReceiptSqlLiteRepository(conn))
    repo.store(Shift("1", ShiftState.OPEN, []))
    assert get_shift_status(conn, "1") == str(ShiftState.OPEN)
    assert get_shift_receipts(conn, "1") == []
    conn.close()
