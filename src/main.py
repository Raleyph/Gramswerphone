from filemanager import FileManager
from client import TelegramClient, MessageHandler


def main():
    print("Program started!")

    try:
        file_manager = FileManager()
    except (FileNotFoundError, ValueError) as error:
        print(error)
    else:
        client = TelegramClient(file_manager)
        MessageHandler(client)

        client.run()


if "__main__" == __name__:
    try:
        main()
    except KeyboardInterrupt:
        pass
