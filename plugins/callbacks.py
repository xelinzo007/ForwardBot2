from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client
from script import scripts
from utils import temp_utils
import logging
from database.data_base import db
from .functions import start_forward

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_callback_query()
async def query_handler(bot: Client, query: CallbackQuery):
    if query.data == "close":
        await query.message.delete()
    elif query.data == "about":
        btn = [[
            InlineKeyboardButton("Go Back", callback_data="home"),
            InlineKeyboardButton("Close", callback_data="close")
        ]]
        await query.message.edit_text(
            text=scripts.ABOUT_TXT.format(temp_utils.BOT_NAME),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    elif query.data == "home":
        btn = [[
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Souce Code", callback_data="source")
        ],[
            InlineKeyboardButton("Close", callback_data="close"),
            InlineKeyboardButton("Help", callback_data="help")
        ]]
        await query.message.edit_text(
            text=scripts.START_TXT.format(query.from_user.mention, temp_utils.USER_NAME, temp_utils.BOT_NAME),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    elif query.data == "source":
        btn = [[
            InlineKeyboardButton("Go Back", callback_data="home"),
            InlineKeyboardButton("Close", callback_data="close")
        ]]
        await query.message.edit_text(
            text=scripts.SOURCE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    elif query.data == "cancel_forward":
        temp_utils.CANCEL[int(query.from_user.id)] = True
        await query.answer("Cancelling Process !\n\nIf the bot is sleeping, It will cancell only after the sleeping is over !", show_alert=True)
    elif query.data == "help":
        btn = [[
            InlineKeyboardButton("Go Back", callback_data="home"),
            InlineKeyboardButton("Close", callback_data="close")
        ]]
        await query.message.edit_text(
            text=scripts.HELP_TXT.format(temp_utils.BOT_NAME),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    elif query.data.startswith("forward"):
        ident, userid = query.data.split("#")
        if int(query.from_user.id) != int(userid):
            return await query.answer("You can't touch this !")
        user = await db.get_user(int(userid))
        await query.message.delete()
        await start_forward(bot, userid, user['skip'])
