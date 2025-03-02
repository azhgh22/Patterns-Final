import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.enums.shift_state import ShiftState
from playground.core.models.receipt import Receipt
from playground.core.models.shift import Shift
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository
from playground.infra.memory.sql_lite.receipt_sql_lite_repository import ReceiptSqlLiteRepository
from playground.infra.memory.sql_lite.shift_sql_lite_repository import ShiftSqlLiteRepository


@pytest.fixture
def conn() -> Connection:
    file_path = "shop_test.db"
    if os.path.exists(file_path):
        os.remove(file_path)
    return sqlite3.connect(file_path, check_same_thread=False)


class ReceiptRepoMock(ReceiptSqlLiteRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self.conn = conn
        self.__create_test_receipts()

    def __create_test_receipts(self) -> None:
        self.conn.execute("""
            create table if not exists shift_receipt_linker(
                shift_id Text,
                receipt_id Text       
            )
            """)

        self.conn.commit()

    def insert_receipt(self, receipt_id: str, shift_id: str) -> ReceiptRepository:
        self.conn.execute(
            """
            insert into shift_receipt_linker (shift_id,receipt_id)
            values(?,?)
        """,
            (shift_id, receipt_id),
        )
        self.conn.commit()
        return self

    def update_shift_id(self, shift_id: str, receipt_id: str) -> bool:
        self.conn.execute(f"""
            update shift_receipt_linker
            set shift_id = '{shift_id}'
            where receipt_id = '{receipt_id}'
        """)
        self.conn.commit()
        return True

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        return Receipt("1", "1", ReceiptStatus.OPEN, [], 3, 3)


def insert_shift(conn: Connection, shift: Shift) -> None:
    print(shift.state)
    conn.execute(
        """
        insert into shifts (id,status)
        values(?,?)
    """,
        (shift.id, shift.state),
    )
    conn.commit()


def get_shift_status(conn: Connection, shift_id: str) -> str | None:
    res = conn.execute(f"""
                select status from shifts 
                where id='{shift_id}';
            """).fetchone()

    if res is None:
        return None
    return str(res[0])


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
    assert get_shift_status(conn, "1") == ShiftState.CLOSED
    conn.close()


def test_should_add_new_shift(conn: Connection) -> None:
    repo = ShiftSqlLiteRepository(conn, ReceiptRepoMock(conn))
    repo.store(Shift("1", ShiftState.OPEN, []))
    assert get_shift_status(conn, "1") == ShiftState.OPEN
    assert get_shift_receipts(conn, "1") == []
    conn.close()


def test_should_return_true_if_shift_exists(conn: Connection) -> None:
    repo = ShiftSqlLiteRepository(conn, ReceiptRepoMock(conn))
    insert_shift(conn, Shift("1", ShiftState.OPEN, []))
    assert repo.shift_exists("1")
    conn.close()


def test_should_return_false_if_shift_does_not_exist(conn: Connection) -> None:
    repo = ShiftSqlLiteRepository(conn, ReceiptRepoMock(conn))
    assert not repo.shift_exists("1")
    conn.close()


def test_should_add_receipt_to_shift(conn: Connection) -> None:
    repo = ShiftSqlLiteRepository(conn, ReceiptRepoMock(conn).insert_receipt("1", "10"))
    repo.add_receipt("1", Receipt("1", "", ReceiptStatus.OPEN, [], 3, 3))
    res = conn.execute(f"""
        select shift_id from shift_receipt_linker
        where receipt_id = '{1}'
    """).fetchone()
    assert res is not None
    assert str(res[0]) == "1"
    conn.close()
