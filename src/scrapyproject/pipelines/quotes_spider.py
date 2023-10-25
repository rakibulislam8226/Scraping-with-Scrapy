import sqlite3


class QuotesPipelineWithSqlite(object):
    def __init__(self) -> None:
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("db.sqlite3")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes_db""")
        self.curr.execute(
            """create table quotes_db (
                    text text,
                    author text,
                    tag text
        )"""
        )

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
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
