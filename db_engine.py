import sqlite3
from Utils.logging import get_logger as log


class DBEngine:
    __instance = None

    class __DBEngine:
        def __init__(self, dbname):
            self.dbname = dbname
            try:
                log().info('connecting to local database')
                self.conn = sqlite3.connect(dbname)
                log().info(sqlite3.version)
                log().info('connected to local database')
            except sqlite3.Error as e:
                log().critical('local database initialisation error: "%s"', e)

        def setup(self):
            stmt = "CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY)"
            self.conn.execute(stmt)
            self.conn.commit()

        def add_item(self, item):
            stmt = "INSERT INTO users (id) VALUES (?)"
            args = (item,)
            try:
                self.conn.execute(stmt, args)
                self.conn.commit()
            except sqlite3.IntegrityError as e:
                log().critical('user id ' + str(item) + ' already exists in database')

        def delete_item(self, item):
            stmt = "DELETE FROM users WHERE id = (?)"
            args = (item,)
            self.conn.execute(stmt, args)
            self.conn.commit()

        def get_items(self):
            stmt = "SELECT id FROM users"
            return [x[0] for x in self.conn.execute(stmt)]

    def __init__(self, dbname="kubera.sqlite"):
        if not DBEngine.__instance:
            DBEngine.instance = DBEngine.__DBEngine(dbname)
        else:
            DBEngine.instance.dbname = dbname

    def __getattr__(self, name):
        return getattr(self.instance, name)
