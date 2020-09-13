# singleton pattern

import sqlite3
from Utils.logging import get_logger as log


class DBEngine:
    __instance = None

    class __DBEngine:
        def __init__(self, dbname):
            self.dbname = dbname
            try:
                self.conn = sqlite3.connect(dbname)
            except sqlite3.Error as e:
                log().critical('local database initialisation error: "%s"', e)

        def setup(self):
            stmt = "CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, username text, first text, last text, " \
                   "persona text) "
            self.conn.execute(stmt)
            self.conn.commit()

        # create
        def add_item(self, values, columns):
            # Check for single column insert
            if isinstance(columns, str):
                values, columns = (values,), (columns,)

            assert len(values) == len(columns), 'Mismatch between values and columns'

            template = """INSERT INTO users ({}) VALUES ({})"""

            cols = ','.join([f'"{col}"' for col in columns])
            placeholders = ','.join(['?'] * len(values))
            stmt = template.format(cols, placeholders)

            self.conn.execute(stmt, values)
            self.conn.commit()

        # read
        def get_items(self, column):
            rows = self.conn.execute("SELECT " + column + " FROM users").fetchall()
            self.conn.commit()
            return rows

        # update
        def update_item(self, first, second, third, fourth):
            stmt = "UPDATE users SET " + first + " = ? WHERE " + third + " = ?"
            args = (second, fourth,)
            self.conn.execute(stmt, args)
            self.conn.commit()

        # delete
        def delete_item(self, column, item):
            stmt = "DELETE FROM users WHERE " + column + " = (?)"
            args = (item,)
            self.conn.execute(stmt, args)
            self.conn.commit()

    def __init__(self, dbname="kubera.sqlite"):
        if not DBEngine.__instance:
            DBEngine.instance = DBEngine.__DBEngine(dbname)
        else:
            DBEngine.instance.dbname = dbname

    def __getattr__(self, name):
        return getattr(self.instance, name)
