import mysql.connector


class BooksPipelineWithMySQL(object):
    def __init__(self) -> None:
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            database="scrapy_books",
            user="root",
            password="Password123#@!",
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS books""")
        self.curr.execute(
            """create table books (
                    image text,
                    image_alt text,
                    title text,
                    price text,
                    stock text
        )"""
        )

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        stock = "".join(item["stock"])
        self.curr.execute(
            """insert into books values (%s,%s,%s,%s,%s)""",
            (
                item["image"],
                item["image_alt"],
                item["title"],
                item["price"],
                stock,
            ),
        )
        self.conn.commit()
