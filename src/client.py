import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from datetime import datetime, timedelta
from filemanager import FileManager


class TelegramClient:
    def __init__(self, filemanager: FileManager, use_start_device: bool):
        self.__filemanager = filemanager

        client_settings = {
            "name": str(os.getenv("CLIENT_NAME")),
            "api_id": int(os.getenv("API_ID")),
            "api_hash": str(os.getenv("API_HASH")),
            "app_version": str(os.getenv("APP_VERSION")),
            "system_version": str(os.getenv("SYSTEM")),
            "workdir": self.filemanager.session_dir
        }

        start_device_name = str(os.getenv("START_DEVICE_NAME"))
        device_name = str(os.getenv("DEVICE_NAME"))

        self.__app = Client(
            **client_settings,
            device_model=device_name
            if (not use_start_device or os.listdir(filemanager.session_dir)) or start_device_name == ""
            else start_device_name
        )

        self.__app.add_handler(MessageHandler(self.answer, filters.incoming & filters.private & ~filters.bot))

    @property
    def filemanager(self) -> FileManager:
        return self.__filemanager

    def run(self) -> None:
        self.__app.run()

    def auth(self) -> None:
        self.__app.start()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.sleep(120))

        self.__app.stop()

    async def answer(self, client: Client, message: Message) -> None:
        try:
            user_id = message.from_user.id
            username = message.from_user.username
            message_text = self.filemanager.get_message_text()
        except ...:
            pass
        else:
            if user_id in self.filemanager.processed_users:
                return

            if self.filemanager.except_mode ^ (user_id in self.filemanager.except_users):
                return

            self.filemanager.write_answered_user(str(user_id), username)

            if message.date < datetime.now() - timedelta(seconds=10):
                return

            await asyncio.sleep(int(os.getenv("ANSWER_TIMEING")))
            await client.send_message(user_id, message_text)

            print(f"Answered: {user_id} {'- @' + username if username else ''}")
