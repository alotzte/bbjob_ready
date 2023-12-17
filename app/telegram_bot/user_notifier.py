import time
from telegram import Bot
import schedule
from db import connect_to_database
from config import Config
import requests


class MyApiBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "http://178.170.192.197:8000/"
        self.login_url = self.base_url + "auth/"
        self.export_csv_url = self.base_url + "employees/export-csv"
        self.session = requests.Session()

    def login(self):
        login_payload = {'username': self.username, 'password': self.password}
        response = self.session.post(self.login_url, data=login_payload)
        return response.status_code == 200

    def download_csv(self, file_path='exported_data.csv'):
        response_export_csv = self.session.get(self.export_csv_url)
        if response_export_csv.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response_export_csv.content)
            return True
        else:
            return False


def send_greetings(bot, chat_id):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    message = f"Скидываю свежий отчет! Текущее время: {current_time}"
    bot.send_message(chat_id, message)


def check_and_notify_users(bot):
    conn, cursor = connect_to_database()
    cursor.execute("SELECT id, username, telegram_id FROM users WHERE telegram_id <> 0")
    results = cursor.fetchall()
    conn.close()

    for user_id, username, telegram_id in results:
        send_greetings(bot, telegram_id)
        my_bot = MyApiBot(username, 'test')
        if my_bot.login():
            if my_bot.download_csv():
                with open('exported_data.csv', 'rb') as file:
                    bot.send_document(telegram_id, document=file)


def job():
    bot_token = Config.TOKEN
    bot = Bot(token=bot_token)
    check_and_notify_users(bot)


schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
