heroku login ksergeychuk2092@ya.ru Lazsxdcf2!
heroku create --region eu main #имя приложения
heroku addons:create heroku-redis:hobby-dev -a main 
heroku buildpacks:set heroku/python
git push heroku master
heroku ps:scale bot=1 # запускаем бота
heroku logs --tail #включаем логи

import json
import sqlite3
import telebot
from telebot import types
import tinvest
from requests import get

# То что касается бота
TOKEN = "5259140715:AAGHkZ42Ty1UPd5ate3NUURr4MP3c_1o6MU"
bot = telebot.TeleBot(TOKEN)


# То что касается Тинькофф
# tin_api_token = "t.j6Edg-Y5GML1VQ0IgO85_Eh2zCTIfa1RaI6TzmVsbKB-Ci6palE8xBj-g976kuG9bwxflBLJ1yYWRd0iVPagdg"
# user_tin = tinvest.SyncClient(tin_api_token)
# user_tin_portfolio = user_tin.get_portfolio()
# print(user_tin_portfolio.json())


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} 👋, меня зовут Олег!\nДля того чтобы "
                                      f"начать отслеживать свой портфель, вам нужно будет передать нам свой токен.\nДля"
                                      f" этого воспользуйтесь командой \"/token_portfolio\"")


@bot.message_handler(commands=['token_portfolio'])
def help_user(message):
    msg = bot.send_message(message.chat.id, "Для получения своего токена вам нужно:\n1) перейти на сайт и войти в свой "
                                            "личный кабинет -> https://id.tinkoff.ru/auth/step?cid=eHWUYA9ZONPN\n2)"
                                            "Перейти в раздел -> Инвестиции -> Настройки\n3) Пролистайте вниз и нажмите"
                                            " получить токен\nДальше мне лень писать Кирилл напишет ))\nВведите токен:")
    bot.register_next_step_handler(msg, setter_token_users)


def setter_token_users(message):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS name_and_token(
                name TEXT,
                token TEXT
            )""")

    db.commit()  # Подтверждаем наше действие

    #  это типо чисто проверка есть ли в нашей таблице в поле token введёный пользователем token
    c = cursor.execute(f"SELECT * FROM name_and_token WHERE token=?", (message.text, ))
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO name_and_token VALUES(?, ?)", (message.from_user.first_name, message.text, ))
        db.commit()
        bot.send_message(message.chat.id, 'Если вы следовали инструкции, то ваш токен был сохранён👍')
    else:
        bot.send_message(message.chat.id, 'Такой пользователь уже существует!🚫')


bot.polling()


"""Это хуита для удаления в дальнейшем может пригодится!!!"""
# sql.execute('DELETE FROM name_and_token WHERE name = ?', ('Gleb',))
