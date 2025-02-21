import sqlite3

from playground.core.models.product import Product


class ProductSqlLiteRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.__create_table()

    def __create_table(self) -> None:
        self.conn.execute("""
                    create table if not exists products (
                        id Text,
                        product_name Text,
                        barcode Text,
                        price Integer
                    )
                """)
        self.conn.commit()

    def __get_product(self, key: str, value: str) -> list[Product]:
        raw = self.conn.execute(f"""
                    select * from products where {key} = '{value}'
                """).fetchall()
        return list(Product(x[0], x[1], x[2], x[3]) for x in raw)

    def get_product_with_id(self, p_id: str) -> Product | None:
        p_list = self.__get_product("id", p_id)
        return p_list[0] if len(p_list) > 0 else None

    def get_all_products(self) -> list[Product]:
        return self.__get_product('"1"', "1")

    def update_price(self, p_id: str, price: int) -> bool:
        updated_rows = self.conn.execute(f"""
                    update products
                    set price={price}
                    where id = {p_id}
                """).rowcount
        return updated_rows == 1

    def store_product(self, product: Product) -> None:
        self.conn.execute(
            """
        insert into products (id, product_name, barcode, price)
        values (?,?,?,?)
         """,
            (product.id, product.name, product.barcode, product.price),
        )
        self.conn.commit()

    def contains_product_with_barcode(self, barcode: str) -> bool:
        return len(self.__get_product("barcode", barcode)) != 0
