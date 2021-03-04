import telegram.ext
from GoogleNews import GoogleNews
from telegram import TelegramError
from Kubera.Model.db import DBEngine
import time


class NewsTracker:
    def __init__(self):
        self.latest_hash = None
        self.latest_article = None
        self.new_article_available = False
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
            self.gn.get_news(name, True)
            result = self.gn.result()[0]
            # hash the title and compare it with db
            new_hash = hash(result['title'])
            # if different, update db and send message
            if new_hash != hash_value:
                DBEngine().update_item('news', 'hash', new_hash, 'name', name)
                users = DBEngine().get_items('usernews', '*')
                # loop thru users
                for user in users:
                    check_name = user[0]
                    id = user[1]
                    # if the current search matches the users saved searches
                    if name == check_name:
                        try:
                            context.bot.send_message(chat_id=id, text=result['title'], parse_mode='HTML')
                            time.sleep(1)
                        except TelegramError:
                            DBEngine().delete_item('users', 'id', user[0])
                            continue
            time.sleep(10)

    def track(self, name, id):
        DBEngine().add_item('news', 'name', name)
        # DBEngine().update_item('news', 'hash', 0, 'name', name)
        DBEngine().add_item('usernews', 'name', name)
        DBEngine().update_item('usernews', 'id', id, 'name', name)

# NewsTracker().update_tracked_news()