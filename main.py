
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
import Bot
import mining
import add


def default(update, context):
    print("default triggered")
    update.message.reply_text('default triggered. try /start')


def fallback(update, context):
    print("fallback triggered")
    update.message.reply_text('fallback triggered. try /start')


def main():
    bot_token = "772700511:AAGDECkjwAt1bePvmz_jdLlWworqHm0aO68"

    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    conversation_handler = ConversationHandler(

        # A list of Handler objects that can trigger
        # the start of the conversation.
        # Type:	List[telegram.ext.Handler]
        entry_points=[
            CommandHandler(Bot.cmd_start, Bot.cmd_start_func),
            MessageHandler(Filters.all, default)],

        # A dict that defines the different states of conversation
        # a user can be in and one or more associated Handler
        # objects that should be used in that state.
        # Type:	Dict[object, List[telegram.ext.Handler]]
        states=
        {
            Bot.MENU:
            [
                CommandHandler(Bot.cmd_mining,
                               mining.start),
                CommandHandler(Bot.cmd_add,
                               add.start),
                # CommandHandler(conversation.cmd_edit, conversation.cmd_edit_func),
                # CommandHandler(conversation.cmd_timer, conversation.cmd_timer_func),
                MessageHandler(Filters.all,
                               default)
            ],
            Bot.MINING:
            [
                MessageHandler(Filters.text,
                               mining.collect)
            ],
            Bot.ADD1:
            [
                MessageHandler(Filters.text,
                               add.question_text_defined)
            ],
            Bot.ADD2:
            [
                MessageHandler(Filters.text('normal'),
                               add.std_keyb_used),
                MessageHandler(Filters.text('new custom keyboard'),
                               add.use_custom_keyb),
            ],
            Bot.ADD3:
                [
                    CommandHandler(Bot.cmd_next_row,
                                   add.next_row),
                    CommandHandler(Bot.cmd_prev_col,
                                   add.prev_col),
                    CommandHandler(Bot.cmd_prev_row,
                                   add.prev_row),
                    CommandHandler(Bot.cmd_keyboard_finished,
                                   add.keyb_done),
                    MessageHandler(Filters.text,
                                   add.set_key),
                ]
        },

        # A list of handlers that might be used if the user is in a
        # conversation, but every handler for their current
        # state returned False on check_update.
        # Type:	List[telegram.ext.Handler]
        fallbacks=[CommandHandler('cancel', fallback)]
    )
    dispatcher.add_handler(conversation_handler)
    print("start polling...")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
