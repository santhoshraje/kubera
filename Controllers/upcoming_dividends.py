import Controllers.global_states as states
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from Utils.logging import get_logger as log
from db_engine import DBEngine


class UpcomingDividends:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        ud_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(
                self.get_upcoming_dividends, pattern='^' + str(states.DIVIDENDUP) + '$')],
            states={
            },
            fallbacks=[]
        )
        self.__dp.add_handler(ud_handler)

    @staticmethod
    def get_upcoming_dividends(update, context):
        user = update.effective_user
        db = DBEngine()
        log().info("User %s pressed the upcoming dividends button.", user.first_name)
        query = update.callback_query
        query.answer()

        rows = db.get_items('dividends', '*')

        tmp = ''
        for row in rows:
            tmp += '<b>' + row[0].lstrip() + ' (' + row[1] + ')</b>\n‣ Market Cap: ' + row[2] \
                    + '\n‣ Price: ' + row[3] + \
                    '\n‣ Amount: ' + row[4] + '\n‣ Yield: ' + row[5] + '\n‣ Date: ' + row[6] + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        return ConversationHandler.END
