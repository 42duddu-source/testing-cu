#Codeflix_Botz
#rohit_1888 on Tg

import motor, asyncio
import motor.motor_asyncio
import time
import pymongo, os
from config import DB_URI, DB_NAME
import logging
from datetime import datetime, timedelta

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

logging.basicConfig(level=logging.INFO)


class Rohit:

    def __init__(self, DB_URI, DB_NAME):
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.database = self.dbclient[DB_NAME]

        self.channel_data = self.database['channels']
        self.admins_data = self.database['admins']
        self.user_data = self.database['users']
        self.banned_user_data = self.database['banned_user']
        self.autho_user_data = self.database['autho_user']
        self.del_timer_data = self.database['del_timer']
        self.fsub_data = self.database['fsub']   
        self.rqst_fsub_data = self.database['request_forcesub']
        self.rqst_fsub_Channel_data = self.database['request_forcesub_channel']
        self.file_store = self.database['file_store']
        
# ======================
# FILE STORE MANAGEMENT (Multi-file Support)
# ======================

    async def add_file_to_key(self, key: str, chat_id: int, file_id: int):
        """
        Add or append a file to an existing key.
        If key doesn't exist, create it.
        """
        await self.file_store.update_one(
            {"key": key},
            {
                "$set": {"chat_id": chat_id},
                "$addToSet": {"file_ids": file_id}
            },
            upsert=True
        )

    async def set_file(self, key: str, chat_id: int, file_id: int):
        """
        Backward-compatible single file bind (used by /setfile legacy).
        Converts older single file entries to list format internally.
        """
        existing = await self.file_store.find_one({"key": key})
        if existing:
            # If old structure, convert to list format
            if "file_id" in existing:
                await self.file_store.update_one(
                    {"key": key},
                    {
                        "$set": {
                            "chat_id": chat_id,
                            "file_ids": [existing["file_id"], file_id]
                        },
                        "$unset": {"file_id": ""}
                    }
                )
            else:
                await self.file_store.update_one(
                    {"key": key},
                    {"$addToSet": {"file_ids": file_id}}
                )
        else:
            await self.file_store.insert_one({
                "key": key,
                "chat_id": chat_id,
                "file_ids": [file_id]
            })

    async def get_file(self, key: str):
        """
        Fetch file record by key.
        Always returns a consistent structure:
        {
          'key': '12',
          'chat_id': 123456,
          'file_ids': [111, 222, 333]
        }
        """
        data = await self.file_store.find_one({"key": key})
        if not data:
            return None

        # Normalize old single-file entries
        if "file_id" in data:
            data["file_ids"] = [data["file_id"]]
            del data["file_id"]
        return data

    async def delete_file(self, key: str):
        """Delete all files bound to a key."""
        return await self.file_store.delete_one({"key": key})

    async def list_files(self):
        """
        List all stored keys with file IDs.
        Returns a list like:
        [
            {'key': '1', 'chat_id': 123, 'file_ids': [111, 112]},
            {'key': '2', 'chat_id': 123, 'file_ids': [113]},
        ]
        """
        files = await self.file_store.find().to_list(length=None)
        for f in files:
            if "file_id" in f:  # Normalize old entries
                f["file_ids"] = [f["file_id"]]
                del f["file_id"]
        return files


    # USER DATA
    async def present_user(self, user_id: int):
        found = await self.user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_user(self, user_id: int):
        await self.user_data.insert_one({'_id': user_id})
        return

    async def full_userbase(self):
        user_docs = await self.user_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in user_docs]
        return user_ids

    async def del_user(self, user_id: int):
        await self.user_data.delete_one({'_id': user_id})
        return


    # ADMIN DATA
    async def admin_exist(self, admin_id: int):
        found = await self.admins_data.find_one({'_id': admin_id})
        return bool(found)

    async def add_admin(self, admin_id: int):
        if not await self.admin_exist(admin_id):
            await self.admins_data.insert_one({'_id': admin_id})
            return

    async def del_admin(self, admin_id: int):
        if await self.admin_exist(admin_id):
            await self.admins_data.delete_one({'_id': admin_id})
            return

    async def get_all_admins(self):
        users_docs = await self.admins_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids


    # BAN USER DATA
    async def ban_user_exist(self, user_id: int):
        found = await self.banned_user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_ban_user(self, user_id: int):
        if not await self.ban_user_exist(user_id):
            await self.banned_user_data.insert_one({'_id': user_id})
            return

    async def del_ban_user(self, user_id: int):
        if await self.ban_user_exist(user_id):
            await self.banned_user_data.delete_one({'_id': user_id})
            return

    async def get_ban_users(self):
        users_docs = await self.banned_user_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids



    # AUTO DELETE TIMER SETTINGS
    async def set_del_timer(self, value: int):        
        existing = await self.del_timer_data.find_one({})
        if existing:
            await self.del_timer_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.del_timer_data.insert_one({'value': value})

    async def get_del_timer(self):
        data = await self.del_timer_data.find_one({})
        if data:
            return data.get('value', 600)
        return 0


    # CHANNEL MANAGEMENT
    async def channel_exist(self, channel_id: int):
        found = await self.fsub_data.find_one({'_id': channel_id})
        return bool(found)

    async def add_channel(self, channel_id: int):
        if not await self.channel_exist(channel_id):
            await self.fsub_data.insert_one({'_id': channel_id})
            return

    async def rem_channel(self, channel_id: int):
        if await self.channel_exist(channel_id):
            await self.fsub_data.delete_one({'_id': channel_id})
            return

    async def show_channels(self):
        channel_docs = await self.fsub_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids

    
# Get current mode of a channel
    async def get_channel_mode(self, channel_id: int):
        data = await self.fsub_data.find_one({'_id': channel_id})
        return data.get("mode", "off") if data else "off"

    # Set mode of a channel
    async def set_channel_mode(self, channel_id: int, mode: str):
        await self.fsub_data.update_one(
            {'_id': channel_id},
            {'$set': {'mode': mode}},
            upsert=True
        )

    # REQUEST FORCE-SUB MANAGEMENT

    # Add the user to the set of users for a   specific channel
    async def req_user(self, channel_id: int, user_id: int):
        try:
            await self.rqst_fsub_Channel_data.update_one(
                {'_id': int(channel_id)},
                {'$addToSet': {'user_ids': int(user_id)}},
                upsert=True
            )
        except Exception as e:
            print(f"[DB ERROR] Failed to add user to request list: {e}")


    # Method 2: Remove a user from the channel set
    async def del_req_user(self, channel_id: int, user_id: int):
        # Remove the user from the set of users for the channel
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': channel_id}, 
            {'$pull': {'user_ids': user_id}}
        )

    # Check if the user exists in the set of the channel's users
    async def req_user_exist(self, channel_id: int, user_id: int):
        try:
            found = await self.rqst_fsub_Channel_data.find_one({
                '_id': int(channel_id),
                'user_ids': int(user_id)
            })
            return bool(found)
        except Exception as e:
            print(f"[DB ERROR] Failed to check request list: {e}")
            return False  


    # Method to check if a channel exists using show_channels
    async def reqChannel_exist(self, channel_id: int):
    # Get the list of all channel IDs from the database
        channel_ids = await self.show_channels()
        #print(f"All channel IDs in the database: {channel_ids}")

    # Check if the given channel_id is in the list of channel IDs
        if channel_id in channel_ids:
            #print(f"Channel {channel_id} found in the database.")
            return True
        else:
            #print(f"Channel {channel_id} NOT found in the database.")
            return False


db = Rohit(DB_URI, DB_NAME)
