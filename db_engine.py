import sqlite3
from Utils.logging import get_logger as log


class DBHelper:
    def __init__(self, dbname="kubera.sqlite"):
        self.dbname = dbname
        try:
            log().info('connecting to local database')
            self.conn = sqlite3.connect(dbname)
            log().info(sqlite3.version)
        except sqlite3.Error as e:
            log().critical('local database initialisation error: "%s"', e)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item):
        stmt = "INSERT INTO users (id) VALUES (?)"
        args = (item,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item):
        stmt = "DELETE FROM users WHERE id = (?)"
        args = (item,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT id FROM users"
        return [x[0] for x in self.conn.execute(stmt)]