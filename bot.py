import config
import telebot
import vedisclient
import reqforms

metros = {'Авиамоторная': 1, 'Автозаводская': 2, 'Академическая': 3}
cyanreq = reqforms.CyanRequest()
domreq = reqforms.DomofondRequest()
avreq = reqforms.AvitoRequest()

bot = telebot.TeleBot(config.token)
telebot.apihelper.proxy = {'https': 'socks5://telegram:telegram@kaisq.tgvpnproxy.me:1080'}


@bot.message_handler(commands=['start'])
def cmd_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                   ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
    msg = bot.send_message(message.chat.id, "Привет! Введи параметры квартиры твоей мечты ->", reply_markup=keyboard)
    vedisclient.set_state(message.chat.id, config.States.S_PARAMETERS.value)
    bot.register_next_step_handler(msg, param_select)


def param_select(message):
    if message.text == 'Ближайшее метро':
        vedisclient.set_state(message.chat.id, config.States.S_METRO.value)
        msg = bot.send_message(message.chat.id, 'Отправь название станции метро',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, set_metro)
    elif message.text == 'От':
        vedisclient.set_state(message.chat.id, config.States.S_LOWER.value)
        msg = bot.send_message(message.chat.id, 'Отправь минимальную цену аренды',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, set_ot)
    elif message.text == 'До':
        vedisclient.set_state(message.chat.id, config.States.S_UPPER.value)
        msg = bot.send_message(message.chat.id, 'Отправь максимальную цену аренды',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, set_ot)
    elif message.text == 'Количество комнат':
        vedisclient.set_state(message.chat.id, config.States.S_ROOMS.value)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Студия', '1', '2', '3', '4+']])
        msg = bot.send_message(message.chat.id, 'Выбери желаемое количество комнат', reply_markup=keyboard)
        bot.register_next_step_handler(msg, set_rooms)
    elif message.text == 'Поиск':
        vedisclient.set_state(message.chat.id, config.States.S_RESULTS.value)
        msg = bot.send_message(message.chat.id, 'Результаты поиска:',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, show_results)


def set_metro(message):
    metro_code = metros.get(message.text)
    if metro_code is None:
        msg = bot.send_message(message.chat.id, 'В Москве нет метро с таким названием! Попробуй еще раз.')
        bot.register_next_step_handler(msg, set_metro)
    else:
        cyanreq.metro = metro_code
        domreq.metro = metro_code
        avreq.metro = metro_code
        vedisclient.set_state(message.chat.id, config.States.S_PARAMETERS)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                       ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
        msg = bot.send_message(message.chat.id, 'введенные параметры',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, param_select)


def set_ot(message):
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'Ты ввел(-а) не цифру, попробуй еще раз')
        bot.register_next_step_handler(msg, set_ot)
    else:
        minprice = int(message.text)
        cyanreq.minprice = minprice
        domreq.PriceFrom = minprice
        avreq.pmin = minprice
        vedisclient.set_state(message.chat.id, config.States.S_PARAMETERS)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                       ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
        msg = bot.send_message(message.chat.id, 'Введенные параметры:',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, param_select)


def set_do(message):
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'Ты ввел(-а) не цифру, попробуй еще раз')
        bot.register_next_step_handler(msg, set_ot)
    else:
        maxprice = int(message.text)
        cyanreq.maxprice = maxprice
        domreq.PriceTo = maxprice
        avreq.pmax = maxprice
        vedisclient.set_state(message.chat.id, config.States.S_PARAMETERS)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                       ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
        msg = bot.send_message(message.chat.id, 'Введенные параметры:',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, param_select)


def set_rooms(message):
    if message.text == 'Студия':
            cyanreq.room9=1
    elif message.text == '1':
        cyanreq.room1 = 1
    elif message.text == '2':
        cyanreq.room2 = 1
    elif message.text == '3':
        cyanreq.room3 = 1
    else:
        cyanreq.room4 = 1
    vedisclient.set_state(message.chat.id, config.States.S_PARAMETERS)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                   ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
    msg = bot.send_message(message.chat.id, 'Введенные параметры:',
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, param_select)


def show_results(message):
    bot.last_update_id


if __name__ == '__main__':
    bot.polling(none_stop=True)
