import telegram.ext
from GoogleNews import GoogleNews
from telegram import TelegramError
from Kubera.Model.db import DBEngine
import time
import hashlib


class NewsTracker:
    def __init__(self):
        self.gn = GoogleNews()
        self.gn.set_lang('en')
        self.gn.set_period('2d')
        self.gn.set_encode('utf-8')

    def update_tracked_news(self, context: telegram.ext.CallbackContext):
        # loop thru each name in db
        rows = DBEngine().get_items('news', '*')
        for row in rows:
            name = row[0]
            hash_value = row[1]
            # get latest article for name
            self.gn.get_news(name)
            result = self.gn.result(True)[0]
            # hash the title and compare it with db
            new_hash = hashlib.md5(result['title'].encode()).hexdigest()
            # if different, update db and send message
            if new_hash != hash_value:
                DBEngine().update_item('news', 'hash', new_hash, 'name', name)
                users = DBEngine().get_items('usernews', '*')
                # loop thru users
                for user in users:
                    check_name = user[0]
                    id = user[1]
                    # if the current search matches the users saved searches
                    if check_name == name:
                        try:
                            caption = '<b>' + result['title'] + '</b> - ' + result['date'] + '\n\n' + result['desc'] + '\n\n' + 'Source: <a href="' + result['link'] + '">' + result['site'] + '</a>'
                            context.bot.send_photo(chat_id=id, photo=result['link'], caption=caption, parse_mode='HTML')
                            time.sleep(1)
                        except TelegramError:
                            DBEngine().delete_item('users', 'id', user[0])
                            continue
            time.sleep(10)
            self.gn.clear()

    def track(self, name, id):
        DBEngine().add_item('news', 'name', name)
        DBEngine().add_item('usernews', 'name', name)
        DBEngine().update_item('usernews', 'id', id, 'name', name)

