import psycopg2
from telegram.error import NetworkError
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from config import Config
from db import connect_to_database
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return bcrypt_context.hash(password)

TOKEN = Config.TOKEN

USERNAME, PASSWORD, AUTHENTICATED = range(3)
PERIODICITY, PERIODICITY_CHOICE = range(3, 5)

def check_user_authorization(context, tg_id):
    conn, cursor = connect_to_database()
    cursor.execute(f"SELECT * FROM users WHERE telegram_id = {tg_id}")
    result = cursor.fetchone()
    conn.close()
    return result


def stage_start(update: Update, context: CallbackContext) -> int:
    tg_id = update.message.from_user.id
    if check_user_authorization(context, tg_id):
        update.message.reply_text('Вы уже авторизованы!')
        return AUTHENTICATED
    else:
        update.message.reply_text('Добро пожаловать! Введите свой username:')
        return USERNAME


def stage_login(update: Update, context: CallbackContext) -> int:
    username = update.message.text
    user_id = update.message.from_user.id
    context.user_data['username'] = username
    context.user_data['telegram_id'] = user_id
    update.message.reply_text('Теперь введите email:')
    return PASSWORD


def stage_password(update: Update, context: CallbackContext) -> int:
    email = update.message.text
    username = context.user_data.get('username')
    telegram_id = context.user_data.get('telegram_id')

    if check_login_password(context, email, username):
        save_user_authorization(context, telegram_id, username)
        update.message.reply_text('Вы успешно авторизовались! Введите переодичность отправки сообщений (1 день|7 дней|1 месяц)')
    else:
        update.message.reply_text('Неверные учетные данные. Попробуйте еще раз.')

    return PERIODICITY


def save_user_authorization(context, telegram_id, username):
    print('GO SAVE')
    conn, cursor = connect_to_database()
    cursor.execute(
        f"UPDATE users SET telegram_id = '{telegram_id}' WHERE username = '{username}'")
    conn.commit()
    conn.close()


def check_login_password(context, email, username):
    conn, cursor = connect_to_database()
    # password = get_password_hash(password)
    # print(password)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND email = '{email}'")
    result = cursor.fetchone()
    conn.close()
    return result


def set_periodicity(update: Update, context: CallbackContext) -> int:
    # Handle the user's choice of periodicity here
    periodicity_choice = update.message.text
    context.user_data['periodicity'] = periodicity_choice

    # You can save this information to the database or perform any other necessary actions
    # For example, you might want to associate the periodicity with the user's data in the database

    update.message.reply_text(f'Вы выбрали: {periodicity_choice}. Теперь вы можете начать использовать бота с установленной переодичностью.')

    return ConversationHandler.END

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", stage_start)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, stage_login)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, stage_password)],
            PERIODICITY: [MessageHandler(Filters.regex('^(1 день|7 дней|1 месяц)$'), set_periodicity)],
            AUTHENTICATED: []
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except NetworkError:
        main()
