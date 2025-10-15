# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

#=====================================================================================##

@Bot.on_message(filters.command('stats') & admin)
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))


#=====================================================================================##

WAIT_MSG = "<b>Working....</b>"

#=====================================================================================##


@Bot.on_message(filters.command('users') & filters.private & admin)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await db.full_userbase()
    await msg.edit(f"{len(users)} ᴜsᴇʀs ᴀʀᴇ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ")

# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

#=====================================================================================##

#AUTO-DELETE

@Bot.on_message(filters.private & filters.command('dlt_time') & admin)
async def set_delete_time(client: Bot, message: Message):
    try:
        duration = int(message.command[1])

        await db.set_del_timer(duration)

        await message.reply(f"<b>Dᴇʟᴇᴛᴇ Tɪᴍᴇʀ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴛᴏ <blockquote>{duration} sᴇᴄᴏɴᴅs.</blockquote></b>")

    except (IndexError, ValueError):
        await message.reply("<b>Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs.</b> Usage: /dlt_time {duration}")

@Bot.on_message(filters.private & filters.command('check_dlt_time') & admin)
async def check_delete_time(client: Bot, message: Message):
    duration = await db.get_del_timer()

    await message.reply(f"<b><blockquote>Cᴜʀʀᴇɴᴛ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ ɪs sᴇᴛ ᴛᴏ {duration}sᴇᴄᴏɴᴅs.</blockquote></b>")

#=====================================================================================##

# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#


# =========================
# /setfile Command
# =========================
@Bot.on_message(filters.command("setfile") & filters.private & admin)
async def set_file_cmd(client: Bot, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ Usage:\n`/setfile <number>`\nThen reply to a file.")

    key = message.command[1].strip()
    if not key.isdigit():
        return await message.reply_text("❌ Only numbers are allowed as keys.")

    if not message.reply_to_message:
        return await message.reply_text("❌ Reply to a file to bind it.")

    file_msg = message.reply_to_message
    if not (file_msg.document or file_msg.video or file_msg.audio or file_msg.photo):
        return await message.reply_text("❌ Only media messages (video, document, audio, photo) are supported.")

    await db.set_file(key, file_msg.chat.id, file_msg.id)
    await message.reply_text(f"✅ File saved for key `{key}`.")


# =========================
# /listfile Command
# =========================
@Bot.on_message(filters.command("listfile") & filters.private & admin)
async def list_files_cmd(client: Bot, message: Message):
    files = await db.list_files()
    if not files:
        return await message.reply_text("📂 No files saved yet.")

    text = "📁 **Saved Files:**\n\n"
    for f in files:
        text += f"🔹 `{f['key']}` → [Message Link](https://t.me/c/{str(f['chat_id']).replace('-100','')}/{f['file_id']})\n"
    await message.reply_text(text, disable_web_page_preview=True)


# =========================
# /delfile Command
# =========================
@Bot.on_message(filters.command("delfile") & filters.private & admin)
async def delete_file_cmd(client: Bot, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ Usage:\n`/delfile <number>`")

    key = message.command[1].strip()
    result = await db.delete_file(key)
    if result.deleted_count == 0:
        return await message.reply_text(f"❌ No file found for key `{key}`.")
    
    await message.reply_text(f"🗑 File for key `{key}` deleted successfully.")


# =========================
# Auto Reply for Number Messages
# =========================
@Bot.on_message(filters.private & filters.text)
async def send_saved_file(client: Bot, message: Message):
    text = message.text.strip()
    if not text.isdigit():
        return

    data = await db.get_file(text)
    if not data:
        return await message.reply_text("❌ No file set for this number.")

    try:
        await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=data["chat_id"],
            message_id=data["file_id"]
        )
    except Exception as e:
        await message.reply_text(f"⚠️ Failed to send file:\n`{e}`")