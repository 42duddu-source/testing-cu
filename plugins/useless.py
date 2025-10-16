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
from asyncio import sleep
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges, ReplyKeyboardRemove
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from plugins.start import *
from config import *
from helper_func import *
from database.database import *


BAN_SUPPORT = f"{BAN_SUPPORT}"

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
"""@Bot.on_message(filters.command("setfile") & filters.private & admin)
async def set_file_cmd(client: Bot, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ Usage:\n`/setfile <number>`\nTʜᴇɴ ʀᴇᴘʟʏ ᴛᴏ ᴀ ғɪʟᴇ.")

    key = message.command[1].strip()
    if not key.isdigit():
        return await message.reply_text("❌ Oɴʟʏ ɴᴜᴍʙᴇʀs ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ ᴀs ᴋᴇʏs.")

    if not message.reply_to_message:
        return await message.reply_text("❌ Rᴇᴘʟʏ ᴛᴏ ᴀ ғɪʟᴇ ᴛᴏ ʙɪɴᴅ ɪᴛ.")

    file_msg = message.reply_to_message
    if not (file_msg.document or file_msg.video or file_msg.audio or file_msg.photo):
        return await message.reply_text("❌ Oɴʟʏ ᴍᴇᴅɪᴀ ᴍᴇssᴀɢᴇs (ᴠɪᴅᴇᴏ, ᴅᴏᴄᴜᴍᴇɴᴛ, ᴀᴜᴅɪᴏ, ᴘʜᴏᴛᴏ) ᴀʀᴇ sᴜᴘᴘᴏʀᴛᴇᴅ.")

    await db.set_file(key, file_msg.chat.id, file_msg.id)
    await message.reply_text(f"✅ Fɪʟᴇ sᴀᴠᴇᴅ ғᴏʀ ᴋᴇʏ `{key}`.")


# =========================
# /listfile Command
# =========================
@Bot.on_message(filters.command("listfile") & filters.private & admin)
async def list_files_cmd(client: Bot, message: Message):
    files = await db.list_files()
    if not files:
        return await message.reply_text("📂 Nᴏ ғɪʟᴇs sᴀᴠᴇᴅ ʏᴇᴛ.")

    text = "📁 𝗦𝗮𝘃𝗲𝗱 𝗙𝗶𝗹𝗲:\n\n"
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
        return await message.reply_text(f"❌ Nᴏ ғɪʟᴇ ғᴏᴜɴᴅ ғᴏʀ ᴋᴇʏ `{key}`.")
    
    await message.reply_text(f"🗑 Fɪʟᴇ ғᴏʀ ᴋᴇʏ `{key}` ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")"""

# =========================
# /setfile Command (Multi-file Input)
# =========================
@Bot.on_message(filters.command("setfile") & filters.private & admin)
async def set_file_cmd(client: Bot, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "⚠️ Usage:\n`/setfile <number>`\nThen send multiple files or messages."
        )

    key = message.command[1].strip()
    if not key.isdigit():
        return await message.reply_text("❌ Only numbers are allowed as keys.")

    collected = []
    STOP_KEYBOARD = ReplyKeyboardMarkup([["STOP"]], resize_keyboard=True)

    await message.reply(
        "📥 Send all media messages you want to include under this key.\n\n"
        "Press STOP when you're done.",
        reply_markup=STOP_KEYBOARD
    )

    while True:
        try:
            user_msg = await client.ask(
                chat_id=message.chat.id,
                text="Waiting for media messages...\nPress STOP to finish.",
                timeout=30  # wait 30 seconds for next input
            )
        except asyncio.TimeoutError:
            break

        # Stop condition
        if user_msg.text and user_msg.text.strip().upper() == "STOP":
            break

        # Allow only media
        if not (user_msg.document or user_msg.video or user_msg.audio or user_msg.photo):
            await message.reply("❌ Unsupported message type, ignored.")
            continue

        # Get file_id
        if user_msg.document:
            fid = user_msg.document.file_id
        elif user_msg.video:
            fid = user_msg.video.file_id
        elif user_msg.audio:
            fid = user_msg.audio.file_id
        elif user_msg.photo:
            fid = user_msg.photo[-1].file_id
        else:
            continue

        collected.append((user_msg.chat.id, fid))
        await message.reply(f"✅ Added ({len(collected)} total)")

    await message.reply("✅ Collection finished.", reply_markup=ReplyKeyboardRemove())

    if not collected:
        return await message.reply("❌ No valid media messages were added.")

    # Store all collected file_ids under key
    for chat_id, fid in collected:
        await db.add_file_to_key(key, chat_id, fid)

    await message.reply(f"✅ All {len(collected)} files stored under key `{key}` successfully.")


# =========================
# /listfile Command
# =========================
@Bot.on_message(filters.command("listfile") & filters.private & admin)
async def list_files_cmd(client: Bot, message: Message):
    files = await db.list_files()
    if not files:
        return await message.reply_text("📂 No files saved yet.")

    text = "📁 <b>Saved Files:</b>\n\n"
    for f in files:
        links = []
        for fid in f["file_ids"]:
            links.append(f"[📎](https://t.me/c/{str(f['chat_id']).replace('-100','')}/{fid})")
        text += f"🔹 <code>{f['key']}</code> → {' '.join(links)}\n"

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

    await message.reply_text(f"🗑 Deleted all files under key `{key}` successfully.")


# =========================
# Auto Send by Key
# =========================
@Bot.on_message(filters.private & filters.text)
async def send_saved_file(client: Bot, message: Message):
    user_id = message.from_user.id

    # Ensure user present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    # Check if banned
    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        return await message.reply_text(
            "<b>⛔️ You are banned from using this bot.</b>\n\n"
            "<i>Contact support if you think this is a mistake.</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Contact Support", url=BAN_SUPPORT)]]
            )
        )

    # Check subscription
    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)

    text = message.text.strip()
    if text.startswith("/") or not text.isdigit():
        return

    data = await db.get_file(text)
    if not data:
        return await message.reply_text("❌ No files found for this key.")

    try:
        FILE_AUTO_DELETE = await db.get_del_timer()
        sent_msgs = []

        for fid in data["file_ids"]:
            sent = await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=fid
            )
            sent_msgs.append(sent)

        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"<b><blockquote>This file(s) will be deleted in {get_exp_time(FILE_AUTO_DELETE)}.\n"
                f"Please save or forward them before they are removed.</blockquote></b>"
            )
            await asyncio.sleep(FILE_AUTO_DELETE)

            for s in sent_msgs:
                try:
                    await s.delete()
                except:
                    pass

            try:
                await notification_msg.delete()
            except:
                pass

    except Exception as e:
        await message.reply_text(f"⚠️ Failed to send files:\n<code>{e}</code>")