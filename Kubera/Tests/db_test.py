from Kubera.Model.db import DBEngine


def main():
    db = DBEngine('test.sqlite')

    # # setup table
    # db.setup()
    # # add single item to database
    # db.add_item('watchlist', ['id', 'ticker'], ['1234', 'v03'])
    # db.add_item('watchlist', ['id', 'ticker'], ['1234', 'u11'])
    # db.add_item('watchlist', ['id', 'ticker'], ['1234', 'c6l'])
    row = db.custom_command('SELECT DISTINCT id FROM watchlist ')
    # for each id
    for r in row:
        print(r[0])
        rowx = db.custom_command('SELECT ticker FROM watchlist WHERE id=' + str(r[0]))
        # for each ticker that belongs to the user
        for x in rowx:
            print(x[0])
    # # add multiple items to database
    # db.add_item(['Tom', 'Sawyer'], ['first', 'last'])
    # # get all columns
    # print(db.get_items('*'))
    # # delete column
    # db.delete_item('id', 125)
    # # update column
    # db.update_item('id', 127, 'last', 'Tom')
    # print(db.get_items('*'))


main()