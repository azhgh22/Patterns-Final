import sqlite3

from playground.core.enums.shift_state import ShiftState
from playground.core.models.receipt import Receipt
from playground.core.models.shift import Shift
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository


class ShiftSqlLiteRepository:
    def __init__(self, connection: sqlite3.Connection, receipt_repo: ReceiptRepository):
        self.conn = connection
        self.receipt_repo = receipt_repo
        self.__create_shift_table()
        self.__create_shift_receipt_linker()

    def get_open_shift_id(self) -> str | None:
        res = self.conn.execute(f"""
            select id from shifts 
            where status = '{str(ShiftState.OPEN)}';
        """).fetchone()

        if res is not None:
            return res[0]
        return None

    def close(self, shift_id: str) -> bool:
        updated_rows = self.conn.execute(f"""
                            update shifts
                            set status = '{str(ShiftState.CLOSED)}'
                            where id = '{shift_id}'
                        """).rowcount
        self.conn.commit()
        return updated_rows == 1

    def store(self, shift: Shift) -> None:
        self.conn.execute(
            """
            insert into shifts (id,status)
            values(?,?)
        """,
            (shift.id, str(shift.state)),
        )
        self.conn.commit()

    def add_receipt(self, shift_id: str, receipt: Receipt) -> Receipt | None:
        pass

    def get_shift_receipts(self, shift_id: str) -> list[Receipt]:
        pass

    def remove_receipt(self, shift_id: str, receipt_id: str) -> bool:
        pass

    def __create_shift_table(self) -> None:
        self.conn.execute("""
                                    create table if not exists shifts (
                                        id Text,
                                        status Text
                                    )
                                """)

        self.conn.commit()

    def __create_shift_receipt_linker(self) -> None:
        self.conn.execute("""
                    create table if not exists shift_receipt_linker(
                            shift_id Text,
                            receipt_id Text       
                        )
                """)

        self.conn.commit()
