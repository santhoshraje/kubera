import sqlite3
from Utils.logging import get_logger as log


class DBEngine:
    __instance = None

    class __DBEngine:
        def __init__(self, dbname):
            self.dbname = dbname
            try:
                self.conn = sqlite3.connect(dbname)
                self.cursor = self.conn.cursor()
                self.create_table('watchlist', 'id integer, ticker text')
            except sqlite3.Error as e:
                log().critical('local database initialisation error: "%s"', e)
                self.conn = None

        # create a new table
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

            try:
                self.conn.execute(stmt, values)
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

        # read
        def get_items(self, table, column):
            rows = self.conn.execute("SELECT " + column + " FROM " + table)
            self.conn.commit()
            return rows

        def get_distinct_items(self, table, column, item):
            stmt = self.conn.execute("SELECT ticker FROM " + table + " WHERE " + column + " = ?")
            args = (item,)
            rows = self.conn.execute(stmt, args)
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

        def count(self, command):
            self.cursor.execute(command)
            results = self.cursor.fetchone()
            return results[0]

        # show all the columns in a table
        def show_all_columns(self, table):
            stmt = "PRAGMA table_info(" + table + ")"
            columns = self.conn.execute(stmt)
            self.conn.commit()
            return columns

    def __init__(self, dbname="sqlite"):
        if not DBEngine.__instance:
            DBEngine.instance = DBEngine.__DBEngine(dbname)
        else:
            DBEngine.instance.dbname = dbname

    def __getattr__(self, name):
        return getattr(self.instance, name)
