from sqlite3 import Connection

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.models.product import Product
from playground.core.models.receipt import Receipt, ReceiptItem


class ReceiptSqlLiteRepository:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.__create_tables()

    def store_receipt(self, receipt: Receipt) -> None:
        # Insert the receipt record.
        self.connection.execute(
            "INSERT INTO receipts (id, shift_id, status, total, discounted_total) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                receipt.id,
                receipt.shift_id,
                receipt.status.name,
                receipt.total,
                receipt.discounted_total,
            ),
        )
        # Insert each receipt item.
        for item in receipt.products:
            self.add_product_to_receipt(item)
        self.connection.commit()

    def __get_receipt_key_val(self, key: str, value: str) -> list[Receipt]:
        rows = self.connection.execute(f"""
            select * from receipts where {key}='{value}';
        """).fetchall()

        return list(Receipt(x[0], x[1], x[2], [], x[3], x[4]) for x in rows)

    def __get_item_key_value(self, key: str, value: str) -> list[ReceiptItem]:
        rows = self.connection.execute(f"""
            select * from receipt_items where {key}='{value}';
        """).fetchall()

        return list(ReceiptItem(x[0], x[1], x[2], x[3], x[4]) for x in rows)

    def contains_receipt(self, receipt_id: str) -> bool:
        res = self.__get_receipt_key_val("id", receipt_id)
        return len(res) > 0

    # Returns True if receipt is successfully deleted
    def delete_receipt(self, receipt_id: str) -> bool:
        self.connection.execute("DELETE FROM receipt_items WHERE receipt_id = ?", (receipt_id,))
        cursor = self.connection.execute("DELETE FROM receipts WHERE id = ?", (receipt_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        res = self.__get_receipt_key_val("id", receipt_id)
        if len(res) != 1:
            return None
        receipt = res[0]
        items = self.__get_item_key_value("receipt_id", receipt_id)
        receipt.products.extend(items)
        return receipt

    def add_product_to_receipt(self, item: ReceiptItem) -> Receipt | None:
        self.connection.execute(
            """
            insert into receipt_items (receipt_id, product_id, quantity, price, total)
            values (?,?,?,?,?)
        """,
            (item.receipt_id, item.product_id, item.quantity, item.price, item.total),
        )
        self.connection.commit()
        return self.get_receipt(item.receipt_id)

    def update_shift_id(self, shift_id: str, receipt_id: str) -> bool:
        rowcount = self.connection.execute(
            "UPDATE receipts SET shift_id = ? WHERE id = ?", (shift_id, receipt_id)
        ).rowcount
        self.connection.commit()
        return rowcount > 0

    def get_all_receipts(self, shift_id: str) -> list[Receipt]:
        receipts = self.__get_receipt_key_val("shift_id", shift_id)

        for receipt in receipts:
            receipt.products.extend(self.__get_item_key_value("receipt_id", receipt.id))

        return receipts

    def get_item(self, product_id: str, receipt_id: str) -> ReceiptItem | None:
        p_id = set(self.__get_item_key_value("product_id", product_id))
        r_id = set(self.__get_item_key_value("receipt_id", receipt_id))
        intersection = list(p_id.intersection(r_id))
        return None if len(intersection) == 0 else intersection[0]

    def remove_item(self, item: ReceiptItem) -> None:
        self.connection.execute(
            """DELETE FROM receipt_items WHERE receipt_id = ? and product_id=?""",
            (item.receipt_id, item.product_id),
        )

    def update_receipt_price(self, receipt_id: str, price: int) -> None:
        self.connection.execute(
            """
            update receipts
            set total = ?
            where id = ?;
        """,
            (price, receipt_id),
        )
        self.connection.commit()

    def __create_tables(self) -> None:
        # Create receipts table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id TEXT PRIMARY KEY,
                shift_id TEXT,
                status TEXT,
                total INTEGER,
                discounted_total INTEGER
            )
        """)
        # Create table for receipt items.
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS receipt_items (
                receipt_id TEXT,
                product_id TEXT,
                quantity INTEGER,
                price INTEGER,
                total INTEGER,
                FOREIGN KEY(receipt_id) REFERENCES receipts(id)
            )
        """)
        self.connection.commit()
