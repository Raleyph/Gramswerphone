# Gramswerphone
 
Autoresponder for Telegram. Powered by Pirogram.

Curren version: 1.2

## 👩‍🏫 Usage

1. Install Python 3.11+ and pip.
2. Install **requirements.txt**.
3. Setup **.env** file.
4. Create a file called message.txt and enter answer text there.
5. Setup blacklist/whitelist (optional).
6. Go to *src/* and run **main.py** file.

## ⚙️ Environment variables

Before running the program, make sure that the correct settings are specified in the .env file.

* **CLIENT_NAME** - name of client session (by default "client").
* **API_ID** - API ID of Telegram App.
* **API_HASH** - API hash of Telegram App.
* **APP_VERSION** - version of the application, shown in the session description.
* **SYSTEM** - OS, shown in session description.
* **DEVICE_NAME** - device name, shown in the session description.
* **START_DEVICE_NAME** - device name, shown in the session description first two minutes (optional).
* **ANSWER_TIMEING** - delay before response.
* **EXCEPT_MODE** - mode of file **exceptions.txt** (0 - this is blacklist, 1 - this is whitelist)
