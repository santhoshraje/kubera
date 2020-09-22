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
                self.conn = None
            self.create_table('users', 'id integer, username text, first text, last text, persona text')
            self.create_table('stocks', 'ticker text, volume float')

        def create_table(self, table, columns):
            table = "CREATE TABLE IF NOT EXISTS " + table + " (" + columns + ")"
            self.conn.execute(table)
            self.conn.commit()

        # create
        def add_item(self, table, columns, values):
            # Check for single column insert
            if isinstance(columns, str):
                values, columns = (values,), (columns,)

            assert len(values) == len(columns), 'Mismatch between values and columns'

            template = "INSERT INTO " + table + " ({}) VALUES ({})"

            cols = ','.join([f'"{col}"' for col in columns])
            placeholders = ','.join(['?'] * len(values))
            stmt = template.format(cols, placeholders)

            self.conn.execute(stmt, values)
            self.conn.commit()

        # read
        def get_items(self, table, column):
            rows = self.conn.execute("SELECT " + column + " FROM " + table)
            self.conn.commit()
            return rows

        # update
        def update_item(self, table, first, second, third, fourth):
            stmt = "UPDATE " + table + " SET " + first + " = ? WHERE " + third + " = ?"
            args = (second, fourth,)
            self.conn.execute(stmt, args)
            self.conn.commit()

        # delete
        def delete_item(self, table, column, item):
            stmt = "DELETE FROM " + table + " WHERE " + column + " = (?)"
            args = (item,)
            self.conn.execute(stmt, args)
            self.conn.commit()

        # custom commands
        def custom_command(self, command):
            rows = self.conn.execute(command)
            self.conn.commit()
            return rows

    def __init__(self, dbname="kubera.sqlite"):
        if not DBEngine.__instance:
            DBEngine.instance = DBEngine.__DBEngine(dbname)
        else:
            DBEngine.instance.dbname = dbname

    def __getattr__(self, name):
        return getattr(self.instance, name)
