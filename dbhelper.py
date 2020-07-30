from telegram.ext import BasePersistence


class DBHelper(BasePersistence):
    def __init__(self, store_user_data=True, store_chat_data=True, store_bot_data=True):
        super().__init__(store_user_data=store_user_data, store_chat_data=store_chat_data, store_bot_data=store_bot_data)

