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
                   "stocks text, persona text, actions text) "
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
        def get_items(self):
            stmt = "SELECT id FROM users"
            return [x[0] for x in self.conn.execute(stmt)]
        # update


        # delete
        def delete_item(self, item):
            stmt = "DELETE FROM users WHERE id = (?)"
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
