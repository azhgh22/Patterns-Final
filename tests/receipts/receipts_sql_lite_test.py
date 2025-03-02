import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.models.product import Product
from playground.core.models.receipt import Receipt, ReceiptItem
from playground.infra.memory.sql_lite.receipt_sql_lite_repository import ReceiptSqlLiteRepository


def insert_receipt(conn: Connection, receipt: Receipt) -> None:
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
    for item in receipt.products:
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
    assert not repo.contains_receipt("r1")
    receipt = Receipt(
        id="r1",
        shift_id="s1",
        status=ReceiptStatus.OPEN,
        products=[],
        total=0,
        discounted_total=None,
    )
    insert_receipt(conn, receipt)
    assert repo.contains_receipt("r1")
    conn.close()


def test_should_delete_receipt(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    receipt = Receipt(
        id="r1",
        shift_id="s1",
        status=ReceiptStatus.OPEN,
        products=[],
        total=0,
        discounted_total=None,
    )
    insert_receipt(conn, receipt)
    # Ensure it exists.
    assert get_receipt_direct(conn, "r1") is not None
    # Delete it and verify.
    assert repo.delete_receipt("r1")
    assert get_receipt_direct(conn, "r1") is None
    conn.close()


def test_should_return_none_for_non_existing_receipt(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    assert repo.get_receipt("non-existing") is None
    conn.close()


def test_should_add_product_to_receipt(conn: Connection) -> None:
    repo = ReceiptSqlLiteRepository(conn)
    # Create a receipt with no products.
    receipt = Receipt(
        id="r1",
        shift_id="s1",
        status=ReceiptStatus.OPEN,
        products=[],
        total=0,
        discounted_total=None,
    )
    repo.store_receipt(receipt)

    # Create a product to add.
    product = Product("p1", "Test Product", "barcode1", 100)

    # Add product with quantity 2.
    updated = repo.add_product_to_receipt(
        ReceiptItem(receipt.id, product.id, 2, product.price, 2 * product.price)
    )
    assert updated is not None
    assert len(updated.products) == 1
    item = updated.products[0]
    assert item.product_id == "p1"
    assert item.quantity == 2
    assert item.price == 100
    assert item.total == 200
    assert updated.total == 0
    conn.close()
