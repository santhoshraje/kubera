from telegram.ext import ConversationHandler, CommandHandler
from Kubera.Model.news_tracker import NewsTracker as nt

class TrackNews:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        handler = ConversationHandler(
            entry_points=[CommandHandler('tracknews', self.__track_news)],
            states={
            },
            fallbacks=[]
        )
        self.__dp.add_handler(handler)

    def __track_news(self, update, context):
        try:
            name = context.args[0]
            nt().track(name, update.effective_user.id)
            update.message.reply_text('Tracking latest news for ' + name)
        except (IndexError, ValueError):
            update.message.reply_text('Incorrect usage. Please use as follows: /tracknews bitcoin')

        return ConversationHandler.END

