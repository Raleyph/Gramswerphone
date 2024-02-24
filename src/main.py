from filemanager import FileManager
from client import TelegramClient

from pyrogram.errors.exceptions.unauthorized_401 import AuthKeyUnregistered

auth_error = "Auth error! Most likely, the session was deleted from the Telegram account. Delete files from the " \
             "session folder, restart the program and log in again."


def main():
    print("Program started!")

    try:
        file_manager = FileManager()
    except (FileNotFoundError, ValueError) as error:
        print(error)
        return

    auth_client = TelegramClient(file_manager, True)

    try:
        auth_client.auth()
    except AuthKeyUnregistered:
        print(auth_error)
        return
    else:
        del auth_client

    client = TelegramClient(file_manager, False)

    try:
        client.run()
    except AuthKeyUnregistered:
        print(auth_error)
        return


if "__main__" == __name__:
    try:
        main()
    except KeyboardInterrupt:
        pass
