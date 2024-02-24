import os
import dotenv

pardir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv.load_dotenv(dotenv_path=os.path.join(pardir, ".env"))


class FileManager:
    def __init__(self):
        self.__session_dir = os.path.join(pardir, "session")
        self.__message_text_path = os.path.join(pardir, "message.txt")

        self.__processed_users_list_path = os.path.join(pardir, "processed.txt")
        self.__exception_list_path = os.path.join(pardir, "exceptions.txt")

        self.__except_mode = True if int(os.getenv("EXCEPT_MODE")) == 1 else False
        self.__check_input_files()

    @property
    def session_dir(self) -> str:
        return self.__session_dir

    @property
    def except_mode(self) -> bool:
        return self.__except_mode

    @property
    def processed_users(self) -> list[int]:
        return self.__get_users_list(self.__processed_users_list_path)

    @property
    def except_users(self) -> list[int]:
        return self.__get_users_list(self.__exception_list_path)

    @staticmethod
    def __get_filedata(filepath: str, clear_voids: bool) -> list[str]:
        with open(filepath, "r", encoding="utf-8") as file:
            input_data = file.readlines()
            filedata = input_data if not clear_voids else [
                data.replace("\n", "") for data in input_data
            ]
            file.close()
            return filedata

    def __check_input_files(self) -> None:
        if not os.path.exists(self.__message_text_path):
            open(self.__message_text_path, "a")
            raise FileNotFoundError(
                "The file with the message text was missing and was"
                "created automatically! Fill it out and restart the program!"
            )

        if not self.__get_filedata(self.__message_text_path, False):
            raise ValueError("The message text file is empty!")

        if not os.path.exists(self.__exception_list_path):
            open(self.__exception_list_path, "a")

        if not os.path.exists(self.__processed_users_list_path):
            open(self.__processed_users_list_path, "a")

        if not os.path.exists(self.__session_dir):
            os.mkdir(self.__session_dir)

    def __get_users_list(self, path: str) -> list[int]:
        return [
            int(user_id.split(":")[0])
            for user_id in self.__get_filedata(path, True)
        ]

    def get_message_text(self) -> str:
        return "\n".join(self.__get_filedata(self.__message_text_path, False))

    def write_answered_user(self, user_id: str, username: str) -> None:
        with open(self.__processed_users_list_path, "a") as file:
            file.write(f"{user_id}:{username}\n")
            file.close()
