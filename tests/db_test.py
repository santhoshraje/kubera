from db_engine import DBEngine


def main():
    db = DBEngine('test.sqlite')
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
