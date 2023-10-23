import sqlite3

conn = sqlite3.connect("db.sqlite3")
curr = conn.cursor()

curr.execute(
    """create table quotes_db (
             title text,
             author text,
             tag text
)"""
)
curr.execute("""insert into quotes_db values ('title', 'rakib','abcd')""")

conn.commit()
conn.close()
