import random
from time import sleep

from telegram import TelegramError
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters

import ShasaBot.modules.sql.users_sql as sql
from ShasaBot import LOGGER, OWNER_ID, dispatcher
from ShasaBot.modules.disable import DisableAbleCommandHandler
from ShasaBot.modules.helper_funcs.chat_status import user_admin
from ShasaBot.modules.helper_funcs.filters import CustomFilters

USERS_GROUP = 4

MESSAGES = (
    "Happy birthday ",
    "Heppi burfdey ",
    "Hep burf ",
    "Happy day of birthing ",
    "Sadn't deathn't-day ",
    "Oof, you were born today ",
)


def banall(update, context):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        all_mems = sql.get_chat_members(chat_id)
    else:
        chat_id = str(update.effective_chat.id)
        all_mems = sql.get_chat_members(chat_id)
    for mems in all_mems:
        try:
            bot.kick_chat_member(chat_id, mems.user)
            update.effective_message.reply_text("Tried banning " + str(mems.user))
            sleep(0.1)
        except BadRequest as excp:
            update.effective_message.reply_text(excp.message + " " + str(mems.user))
            continue


def snipe(update, context):
    args = context.args
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            context.bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of that group?"
            )


@user_admin
def birthday(update, context):
    args = context.args
    if args:
        username = str(",".join(args))
    context.bot.sendChatAction(
        update.effective_chat.id, "typing"
    )  # Bot typing before send messages
    for i in range(5):
        bdaymessage = random.choice(MESSAGES)
        update.effective_message.reply_text(bdaymessage + username)


__mod_name__ = "Birthday"

SNIPE_HANDLER = CommandHandler(
    "snipe", snipe, pass_args=True, filters=CustomFilters.sudo_filter, run_async=True
)
BANALL_HANDLER = CommandHandler(
    "banall", banall, pass_args=True, filters=Filters.user(OWNER_ID), run_async=True
)
BIRTHDAY_HANDLER = DisableAbleCommandHandler(
    "birthday",
    birthday,
    pass_args=True,
    filters=Filters.chat_type.groups,
    run_async=True,
)

dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(BANALL_HANDLER)
dispatcher.add_handler(BIRTHDAY_HANDLER)
