import sqlite3

from playground.core.models.payments import Payment


class PaymentSqlLiteRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.__create_table()

    def __create_table(self) -> None:
        self.conn.execute("""
                    create table if not exists payments (
                        receipt_id TEXT PRIMARY KEY,
                        currency_id TEXT NOT NULL,
                        amount INTEGER NOT NULL
                    )
                """)
        self.conn.commit()

    def register_payment(self, payment: Payment) -> None:
        self.conn.execute(
            "INSERT INTO payments (receipt_id, currency_id, amount) VALUES (?, ?, ?)",
            (payment.receipt_id, payment.currency_id, payment.amount),
        )
        self.conn.commit()

    def get_payment(self, receipt_id: str) -> Payment | None:
        row = self.conn.execute(
            "SELECT receipt_id, currency_id, amount FROM payments WHERE receipt_id = ?",
            (receipt_id,),
        ).fetchone()
        if row:
            return Payment(
                receipt_id=row[0],
                currency_id=row[1],
                amount=row[2],
            )
        return None

    def get_all_payments(self) -> list[Payment]:
        row = self.conn.execute(
            "SELECT receipt_id, currency_id, amount FROM payments",
        ).fetchall()
        payment_list: list[Payment] = []
        for r in row:
            payment_list.append(Payment(r[0], r[1], r[2]))
        return payment_list
