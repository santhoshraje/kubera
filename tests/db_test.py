import db_engine


def main():
    db = db_engine.DBHelper('test.sqlite')
    db.setup()
    db.add_item(345)
    db.add_item(235)
    db.add_item(634)
    print(db.get_items())
    db.delete_item(123)
    db.delete_item(423)
    db.delete_item(321)
    print(db.get_items())


main()
