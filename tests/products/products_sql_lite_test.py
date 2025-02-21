import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.models.product import Product
from playground.infra.memory.sql_lite.product_sql_lite_repository import (
    ProductSqlLiteRepository,
)


def insert_product(conn: Connection) -> None:
    conn.execute(
        """
    insert into products (id, product_name, barcode, price)
    values ("1","1","1",1)
     """
    )
    conn.commit()


def get_product(conn: Connection) -> Product | None:
    raw = conn.execute(
        """
        select * from products where id = "1"
    """
    ).fetchone()

    return Product(raw[0], raw[1], raw[2], raw[3]) if raw is not None else None


@pytest.fixture
def conn() -> Connection:
    file_path = "shop_test.db"
    if os.path.exists(file_path):
        os.remove(file_path)
    return sqlite3.connect(file_path, check_same_thread=False)


def test_env_works(conn: Connection) -> None:
    assert True
    conn.close()


def test_should_store_new_product(conn: Connection) -> None:
    prod = Product("1", "1", "1", 1)
    ProductSqlLiteRepository(conn).store_product(prod)
    assert get_product(conn) is not None
    assert get_product(conn) == prod
    conn.close()


def test_should_not_return_non_existing_products(conn: Connection) -> None:
    assert ProductSqlLiteRepository(conn).get_product_with_id("1") is None
    conn.close()


def test_should_return_existing_products(conn: Connection) -> None:
    repo = ProductSqlLiteRepository(conn)
    insert_product(conn)
    assert repo.get_product_with_id("1") == Product("1", "1", "1", 1)
    conn.close()


def test_should_return_false_as_it_does_not_contains_product_with_barcode(
    conn: Connection,
) -> None:
    assert not ProductSqlLiteRepository(conn).contains_product_with_barcode("1")
    conn.close()


def test_should_return_true_as_it_contains_product_with_barcode(
    conn: Connection,
) -> None:
    repo = ProductSqlLiteRepository(conn)
    insert_product(conn)
    assert repo.contains_product_with_barcode("1")
    conn.close()


def test_should_return_empty_list(conn: Connection) -> None:
    assert ProductSqlLiteRepository(conn).get_all_products() == []
    conn.close()


def test_should_return_list_of_all_products(conn: Connection) -> None:
    repo = ProductSqlLiteRepository(conn)
    insert_product(conn)
    assert repo.get_all_products() == [Product("1", "1", "1", 1)]
    conn.close()


def test_should_not_update_price_of_non_existing_product(conn: Connection) -> None:
    assert not ProductSqlLiteRepository(conn).update_price("1", 10)
    conn.close()


def test_should_update_price_of_existing_product(conn: Connection) -> None:
    repo = ProductSqlLiteRepository(conn)
    insert_product(conn)
    assert repo.update_price("1", 10)
    assert get_product(conn) == Product("1", "1", "1", 10)
    conn.close()
