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

    def __get_payment_with_key(self, key: str, value: str) -> list[Payment]:
        rows = self.conn.execute(
            f"""SELECT receipt_id, currency_id, amount FROM payments
               where {key}="{value}";
            """,
        ).fetchall()
        return list(Payment(x[0], x[1], x[2]) for x in rows)

    def get_payment(self, receipt_id: str) -> Payment | None:
        payment = self.__get_payment_with_key("receipt_id", receipt_id)
        return payment[0] if len(payment) > 0 else None

    def get_all_payments(self) -> list[Payment]:
        return self.__get_payment_with_key('"1"', "1")
