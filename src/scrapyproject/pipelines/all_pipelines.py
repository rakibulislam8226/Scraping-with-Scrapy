import sqlite3

from ..items.quotes_spider import QuotesSpiderItem
from ..items.books import BooksSpiderItem


class ScrapyprojectPipelineWithSqlite(object):
    def __init__(self) -> None:
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("db.sqlite3")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS books_db (
                    image text,
                    image_alt text,
                    title text,
                    price text,
                    stock text
        )"""
        )
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS quotes_db (
                    text text,
                    author text,
                    tag text
        )"""
        )

    def process_item(self, item, spider):
        if isinstance(item, QuotesSpiderItem):
            self.store_quotes(item)
        elif isinstance(item, BooksSpiderItem):
            self.store_books(item)
        return item

    def store_quotes(self, item):
        print("------- quotes executing")
        tags = ",".join(item.get("tags")[0]) if item.get("tags") else ""
        self.curr.execute(
            """insert into quotes_db values (?,?,?)""",
            (
                item["text"][0],
                item["author"][0],
                tags,
            ),
        )
        self.conn.commit()

    def store_books(self, item):
        print("===== books executing")
        stock = (
            " ".join([x.strip() for x in item["stock"] if isinstance(x, str)])
            if item["stock"]
            else ""
        )
        self.curr.execute(
            """insert into books_db values (?,?,?,?,?)""",
            (
                item["image"][0],
                item["image_alt"][0],
                item["title"][0],
                item["price"][0],
                stock,
            ),
        )
        self.conn.commit()
