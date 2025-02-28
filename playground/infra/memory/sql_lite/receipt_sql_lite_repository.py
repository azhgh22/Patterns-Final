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
            self.connection.execute(
                "INSERT INTO receipt_items (receipt_id, product_id, quantity, price, total) "
                "VALUES (?, ?, ?, ?, ?)",
                (receipt.id, item.product_id, item.quantity, item.price, item.total),
            )
        self.connection.commit()

    def contains_receipt(self, receipt_id: str) -> bool:
        cursor = self.connection.execute(
            "SELECT 1 FROM receipts WHERE id = ? LIMIT 1", (receipt_id,)
        )
        return cursor.fetchone() is not None

    # Returns True if receipt is successfully deleted
    def delete_receipt(self, receipt_id: str) -> bool:
        self.connection.execute("DELETE FROM receipt_items WHERE receipt_id = ?", (receipt_id,))
        cursor = self.connection.execute("DELETE FROM receipts WHERE id = ?", (receipt_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        cursor = self.connection.execute(
            "SELECT id, shift_id, status, total, discounted_total FROM receipts WHERE id = ?",
            (receipt_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        status = ReceiptStatus[row[2]]
        receipt = Receipt(
            id=row[0],
            shift_id=row[1],
            status=status,
            products=[],
            total=row[3],
            discounted_total=row[4],
        )
        items_cursor = self.connection.execute(
            "SELECT product_id, quantity, price, total FROM receipt_items WHERE receipt_id = ?",
            (receipt_id,),
        )
        for item_row in items_cursor.fetchall():
            receipt.products.append(
                ReceiptItem(
                    product_id=item_row[0],
                    quantity=item_row[1],
                    price=item_row[2],
                    total=item_row[3],
                )
            )
        return receipt

    def add_product_to_receipt(
        self, receipt: Receipt, product: Product, quantity: int
    ) -> Receipt:
        # Check if the product already exists in the receipt.
        cursor = self.connection.execute(
            "SELECT id, quantity, price, total FROM receipt_items "
            "WHERE receipt_id = ? AND product_id = ?",
            (receipt.id, product.id),
        )
        row = cursor.fetchone()
        if row is None:
            # Insert a new receipt item.
            item_total = product.price * quantity
            self.connection.execute(
                "INSERT INTO receipt_items (receipt_id, product_id, quantity, price, total)"
                " VALUES (?, ?, ?, ?, ?)",
                (receipt.id, product.id, quantity, product.price, item_total),
            )
            new_item = ReceiptItem(
                product_id=product.id, quantity=quantity, price=product.price, total=item_total
            )
            receipt.products.append(new_item)
        else:
            # Update the existing receipt item.
            item_id = row[0]
            new_quantity = row[1] + quantity
            new_total = product.price * new_quantity
            self.connection.execute(
                "UPDATE receipt_items SET quantity = ?, total = ? WHERE id = ?",
                (new_quantity, new_total, item_id),
            )
            receipt_item = receipt.get_receipt_item(product)
            if receipt_item is not None:
                receipt_item.add_item(quantity)

        receipt.total += product.price * quantity
        self.connection.execute(
            "UPDATE receipts SET total = ? WHERE id = ?", (receipt.total, receipt.id)
        )
        self.connection.commit()
        return receipt

    def update_shift_id(self, shift_id: str, receipt_id: str) -> None:
        self.connection.execute(
            "UPDATE receipts SET shift_id = ? WHERE id = ?", (shift_id, receipt_id)
        )
        self.connection.commit()

    def get_all_receipts(self, shift_id: str) -> list[Receipt]:
        cursor = self.connection.execute(
            "SELECT id, shift_id, status, total, discounted_total FROM receipts "
            "WHERE shift_id = ?",
            (shift_id,),
        )
        receipts = []
        for row in cursor.fetchall():
            try:
                status = ReceiptStatus[row[2]]
            except KeyError:
                status = row[2]
            receipt = Receipt(
                id=row[0],
                shift_id=row[1],
                status=status,
                products=[],
                total=row[3],
                discounted_total=row[4],
            )
            items_cursor = self.connection.execute(
                "SELECT product_id, quantity, price, total FROM receipt_items "
                "WHERE receipt_id = ?",
                (row[0],),
            )
            for item in items_cursor.fetchall():
                receipt.products.append(ReceiptItem(item[0], item[1], item[2], item[3]))
            receipts.append(receipt)
        return receipts

    def clear_receipt_shift_id(self, receipt_id: str) -> bool:
        cursor = self.connection.execute(
            "UPDATE receipts SET shift_id = '' WHERE id = ?", (receipt_id,)
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def close_receipt(self, updated_receipt: Receipt) -> None:
        self.connection.execute(
            "UPDATE receipts SET total = ?, discounted_total = ?, status = ? WHERE id = ?",
            (
                updated_receipt.total,
                updated_receipt.discounted_total,
                updated_receipt.status.name,
                updated_receipt.id,
            ),
        )

        for item in updated_receipt.products:
            self.connection.execute(
                """UPDATE receipt_items SET quantity = ?, total = ? 
                        WHERE product_id = ? and receipt_id = ?""",
                (item.quantity, item.total, item.product_id, updated_receipt.id),
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id TEXT,
                product_id TEXT,
                quantity INTEGER,
                price INTEGER,
                total INTEGER,
                FOREIGN KEY(receipt_id) REFERENCES receipts(id)
            )
        """)
        self.connection.commit()
