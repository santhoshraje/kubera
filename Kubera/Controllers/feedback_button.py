from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters

import Controllers.global_states as states

from Utils.logging import get_logger as log

from telegram.ext import MessageHandler

GETFEEDBACK = range(1)

class FeedbackButton:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        cancel_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.__show_message, pattern='^' + str(states.FEEDBACK) + '$')],
            states={
                GETFEEDBACK: [
                    # message handler
                    MessageHandler(Filters.text, self.__store_feedback)
                ]
            },
            fallbacks=[]
        )
        self.__dp.add_handler(cancel_handler)

    def __show_message(self, update, context):
        user = update.effective_user
        query = update.callback_query
        query.answer()
        query.edit_message_text('Please enter your feedback')
        return GETFEEDBACK

    def __store_feedback(self, update, context):
        feedback = update.message.text
        user = update.effective_user
        log().info("User %s entered feedback: %s", user.first_name, feedback)
        update.message.reply_text("Your feedback has been recorded. Thank you!\nUse /start to go back to the main menu")
        return ConversationHandler.END

