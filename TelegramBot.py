import telebot
from telebot import types

# Створення екземпляру бота з токеном доступу
bot = telebot.TeleBot('6310883087:AAHsjJsUtSL10SNvfoAAPacCPtFhLJuG_XM')

# Список питань і відповідей (лише частина, для прикладу)
list_1 = [
{'question': 'Запустив профіль, крутиться кружок -- нічого не відбувається', 'answer': "Для Windows:\n" 
            "Закрий долфін\n" +
            "Запусти командний рядок (win+r)\n" +
            "Впиши: explorer %AppData%\n" +
            "Знайди папку dolphin_anty\n" +
            "Перейменуй її на __dolphin_anty\n" +
            "Запусти долфін\n" +
            "Запусти профіль ще раз\n" +
            "Після цього проблема має піти з усіма профілями\n\n" +
            "Для MacOS:\n" +
            "Закрий долфін\n" +
            "Знайди папку dolphin_anty (через Application Support)\n" +
            "Перейменуй її на __dolphin_anty\n" +
            "Запусти Долфін"},
    {'question': 'Дуже багато спроб вводу Captcha y Dolphin', 'answer': "Спробуйте зайти ще раз використовуючи Vpn.\n" +
            "Ось посилання: https://turbovpn.com/ru/download/windows"},
    {'question': 'Багато разів неправильно ввів пароль y Dolphin', 'answer': 'На жаль, для вирішення цієї проблеми потрібен час (зазвичай 1 година).'},
    {'question': 'Ввів логін i пароль y Dolphin -- нічого не відбулось та знову просить ввести Captcha', 'answer': 'Перезапустіть Dolphin i введіть логін та пароль ще раз.'},
    {'question': 'Викинуло на сторінку введення логіна i пароля (OF)', 'answer': 'Ця проблема не може бути вирішена оператором. Закрийте повністю Dolphin та зверніться до @CA_dima .'},
    {'question': 'Не заходить у профіль (Error: Помилка перевірки з’єднання з проксі)', 'answer': 'Дана проблема пов’язана з тимчасовими проблемами проксі сервера, зверніться будь ласка до @CA_dima .'},
    {'question': 'Не відкривається Dolphin (проблема з локальним API)', 'answer': 'Спочатку перезапустіть Dolphin. Якщо проблема не зникла, перевірте чи не блокує ваш Антивірус програму Dolphin. Якщо так, то відключіть тимчасово ваш Антивірус.'},
    {'question': 'У мене інше питання', 'answer': 'Якщо ви не знайшли своєї проблеми у списку, зверніться до технічного менеджера і напишіть йому свою проблему.\n\n'
        "@CA_dima"}
]

# Welcome message
welcome_message = "Привіт! Я technical support bot компанії 'Crush Agency'. Я готовий відповідати на твої запитання.\n\n" \
                  "<b>Перед тим як звертатися до технічого бота підтримки або ж нашого менеджера, переконайся " \
                  "що у вас встановлена 10 або вище версія Windows, версії Windows від 7 до 8.1 не підтримують Dolphin</b>\n\n" \
                  "<i>Щоб переглянути список команд -- натисніть кнопку 'Меню'</i>" \
                  


# Функція для обробки команди /start 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, welcome_message, parse_mode="HTML")
    send_questions(message)

# Функція для обробки команди /stop
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    response_text = "Дякую, що скористалися нашим ботом. Бажаю вам гарного дня! " \
                    "Щоб задати питання, натисніть кнопку /questions."
    bot.send_message(message.chat.id, response_text)
    # Припинення обміну повідомленнями
    bot.stop_polling()

# Функція для обробки команди /questions
@bot.message_handler(commands=['questions'])
def handle_questions(message):
    send_questions(message)

    # Функція для обробки команди /help або /info
@bot.message_handler(commands=['info'])
def send_help_info(message):
    help_info = "Цей бот допомагає вирішувати різні технічні проблеми з програмою Dolphin.\n\n" \
                "Для початку оберіть питання зі списку доступних, а я видам відповідний варіант вирішення проблеми.\n" \
                "Якщо вашої проблеми немає у списку, ви можете звернутися до технічного менеджера @CA_dima \n\n" \
                "Для повернення до списку питань скористайтесь командою /questions."

    bot.send_message(message.chat.id, help_info)

# Функція для відправки питань у вигляді кнопок
def send_questions(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in list_1:
        markup.add(types.KeyboardButton(item['question']))

    bot.send_message(message.chat.id, "Обери питання:", reply_markup=markup)

# Обробник відповіді на питання
@bot.message_handler(func=lambda message: message.text in [item['question'] for item in list_1])
def handle_question(message):
    question = message.text
    answer = next(item['answer'] for item in list_1 if item['question'] == question)

    # Відправка відповіді на питання
    bot.send_message(message.chat.id, answer)

    # Створення нової клавіатури з кнопками "Мою проблему вирішено",
    # "Мою проблему не вирішено" та "Назад до питань"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Мою проблему вирішено"),
        types.KeyboardButton("Мою проблему не вирішено"),
        types.KeyboardButton("Назад до питань")
    )

    bot.send_message(message.chat.id, "Вашу проблему вирішено?", reply_markup=markup)

# Обробник вибору варіанту "Мою проблему вирішено",
# "Мою проблему не вирішено" або "Назад до питань"
@bot.message_handler(func=lambda message: message.text in ["Мою проблему вирішено", "Мою проблему не вирішено", "Назад до питань"])
def handle_choice(message):
    choice = message.text

    if choice == "Мою проблему вирішено":
        bot.send_message(message.chat.id, "Завжди радий вам допомогти!")
    elif choice == "Мою проблему не вирішено":
        bot.send_message(message.chat.id, "Мені дуже шкода, що вам не вдалось вирішити свою проблему, зверніться будь ласка з цим питанням до технічного менеджера @CA_dima")

    send_questions(message)

    # Функція для обробки команди /feedback
@bot.message_handler(commands=['feedback'])
def get_feedback(message):
    bot.send_message(message.chat.id, "Напишіть ваш відгук або питання до технічного менеджера:")
    bot.register_next_step_handler(message, save_feedback)

# Функція для збереження відгуків
def save_feedback(message):
    with open("feedback.txt", "a", encoding="utf-8") as file:
        file.write(f"{message.from_user.username}: {message.text}\n")
    bot.send_message(message.chat.id, "Дякуємо за ваш відгук! Ваше повідомлення було збережено.")

# Обробник для некоректних повідомлень
@bot.message_handler(func=lambda message: True)
def handle_invalid(message):
    bot.send_message(message.chat.id, "Вибачте, я не розумію це запитання.")

# Запуск бота
bot.polling()
