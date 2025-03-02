import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.models.product import Product
from playground.core.models.receipt import Receipt, ReceiptItem
from playground.infra.memory.sql_lite.receipt_sql_lite_repository import ReceiptSqlLiteRepository


def insert_receipt(
    conn: Connection,
    receipt: Receipt = Receipt("1", "1", ReceiptStatus.OPEN, [], 100, None),
    items: list[ReceiptItem] | None = None,
) -> None:
    if items is None:
        items = []

    conn.execute(
        """
        INSERT INTO receipts (id, shift_id, status, total, discounted_total)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            receipt.id,
            receipt.shift_id,
            receipt.status.name,
            receipt.total,
            receipt.discounted_total,
        ),
    )
    for item in items:
        conn.execute(
            """
            INSERT INTO receipt_items (receipt_id, product_id, quantity, price, total)
            VALUES (?, ?, ?, ?, ?)
            """,
            (receipt.id, item.product_id, item.quantity, item.price, item.total),
        )
    conn.commit()


def get_receipt_direct(conn: Connection, receipt_id: str) -> Receipt | None:
    raw = conn.execute(
        """
        SELECT id, shift_id, status, total, discounted_total
        FROM receipts
        WHERE id = ?
        """,
        (receipt_id,),
    ).fetchone()

    if raw is None:
        return None

    receipt = Receipt(
        id=raw[0],
        shift_id=raw[1],
        status=ReceiptStatus[raw[2]],
        products=[],
        total=raw[3],
        discounted_total=raw[4],
    )
    items = conn.execute(
        """
        SELECT receipt_id ,product_id, quantity, price, total
        FROM receipt_items
        WHERE receipt_id = ?
        """,
        (receipt_id,),
    ).fetchall()

    for item in items:
        receipt.products.append(ReceiptItem(item[0], item[1], item[2], item[3], item[4]))
    return receipt


@pytest.fixture
def conn() -> Connection:
    file_path = "shop_test.db"
    if os.path.exists(file_path):
        os.remove(file_path)
    connection = sqlite3.connect(file_path, check_same_thread=False)
    ReceiptSqlLiteRepository(connection)
    return connection


def test_env_works(conn: Connection) -> None:
    assert True
    conn.close()


def test_should_store_new_receipt(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    receipt = Receipt(
        id="r1",
        shift_id="s1",
        status=ReceiptStatus.OPEN,
        products=[],
        total=100,
        discounted_total=None,
    )
    repo.store_receipt(receipt)
    stored = get_receipt_direct(conn, "r1")
    assert stored is not None
    assert stored.id == receipt.id
    assert stored.shift_id == receipt.shift_id
    assert stored.status == receipt.status
    assert stored.total == receipt.total
    assert stored.discounted_total == receipt.discounted_total
    conn.close()


def test_should_check_contains_receipt(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    assert not repo.contains_receipt("1")
    insert_receipt(conn)
    assert repo.contains_receipt("1")
    conn.close()


def test_should_delete_receipt(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    insert_receipt(conn)
    assert get_receipt_direct(conn, "1") is not None
    assert repo.delete_receipt("1")
    assert get_receipt_direct(conn, "1") is None
    conn.close()


def test_should_return_none_for_non_existing_receipt(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    assert repo.get_receipt("non-existing") is None
    conn.close()


def test_should_add_product_to_receipt(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    insert_receipt(conn)
    product = Product("p1", "Test Product", "barcode1", 100)
    updated = repo.add_product_to_receipt(
        ReceiptItem("1", product.id, 2, product.price, 2 * product.price)
    )
    assert updated is not None
    assert len(updated.products) == 1
    item = updated.products[0]
    assert item.product_id == "p1"
    assert item.quantity == 2
    assert item.price == 100
    assert item.total == 200
    assert updated.total == 100
    conn.close()


def test_should_return_receipt_item(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    # Create a receipt with no products.
    insert_receipt(conn, items=[ReceiptItem("1", "1", 1, 1, 1)])
    item = repo.get_item("1", "1")
    assert item is not None
    assert item == ReceiptItem("1", "1", 1, 1, 1)
    conn.close()


def test_should_remove_item(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    insert_receipt(conn, items=[ReceiptItem("1", "1", 1, 1, 1)])
    receipt = get_receipt_direct(conn, "1")
    assert receipt is not None
    assert len(receipt.products) == 1
    repo.remove_item(ReceiptItem("1", "1", 1, 1, 1))
    receipt = get_receipt_direct(conn, "1")
    assert receipt is not None
    assert len(receipt.products) == 0
    conn.close()


def test_should_update_receipt_total(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    insert_receipt(conn)
    repo.update_receipt_price("1", 10)
    receipt = get_receipt_direct(conn, "1")
    assert receipt is not None
    assert 10 == receipt.total
    conn.close()


def test_should_update_shift_id(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    insert_receipt(conn)
    assert repo.update_shift_id("33", "1")
    receipt = get_receipt_direct(conn, "1")
    assert receipt is not None
    assert receipt.shift_id == "33"
    conn.close()


def test_should_return_all_receipts(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    insert_receipt(conn)
    receipts = repo.get_all_receipts("1")
    assert len(receipts) == 1
    assert receipts[0].id == "1"
    conn.close()
