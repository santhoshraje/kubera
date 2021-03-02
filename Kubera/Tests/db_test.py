from Kubera.Model.db import DBEngine


def main():
    db = DBEngine('test.sqlite')
    # setup table
    db.setup()
    # add single item to database
    db.add_item('Tom', 'first')
    # add multiple items to database
    db.add_item(['Tom', 'Sawyer'], ['first', 'last'])
    # get all columns
    print(db.get_items('*'))
    # delete column
    db.delete_item('id', 125)
    # update column
    db.update_item('id', 127, 'last', 'Tom')
    print(db.get_items('*'))


main()