import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta

from filemanager import FileManager


class TelegramClient:
    def __init__(self, filemanager: FileManager):
        self.__filemanager = filemanager

        self.__app = Client(
            os.getenv("CLIENT_NAME"), api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"),
            workdir=self.__filemanager.session_dir, app_version=os.getenv("APP_VERSION"),
            device_model=os.getenv("DEVICE_NAME"), system_version=os.getenv("SYSTEM")
        )

    @property
    def filemanager(self) -> FileManager:
        return self.__filemanager

    @property
    def app(self) -> Client:
        return self.__app

    def run(self) -> None:
        self.__app.run()


class MessageHandler:
    def __init__(self, tg_client: TelegramClient):
        self.__client = tg_client

        @self.__client.app.on_message(filters.incoming & filters.private)
        async def answer(client: Client, message: Message) -> None:
            try:
                user_id = message.from_user.id
                username = message.from_user.username
                message_text = self.__client.filemanager.get_message_text()
            except ...:
                pass
            else:
                if user_id in self.__client.filemanager.get_processed_users():
                    return

                if self.__client.filemanager.except_mode ^ (user_id in self.__client.filemanager.get_except_users()):
                    return

                self.__client.filemanager.write_answered_user(str(user_id), username)

                if message.date < datetime.now() - timedelta(seconds=10):
                    return

                await asyncio.sleep(int(os.getenv("ANSWER_TIMEING")))
                await client.send_message(user_id, message_text)

                print(f"Answered: {user_id} {'- @' + username if username else ''}")
