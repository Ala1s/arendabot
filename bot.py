from random import shuffle
from sqlite3 import IntegrityError

import requests
import telebot
from lxml import html

import config
import reqforms
from sqlite_data_tables import AccessTables

db = AccessTables()
bot = telebot.TeleBot(config.token)
# telebot.apihelper.proxy = {'https': 'socks5://telegram:telegram@kaisq.tgvpnproxy.me:1080'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}


@bot.message_handler(commands=['start'])
def cmd_start(message):
    restart(message)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                   ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
    msg = bot.send_message(message.chat.id, "Привет! Введи параметры квартиры для сьёма ->", reply_markup=keyboard)
    bot.register_next_step_handler(msg, param_select)
    try:
        db.add_user(message.chat.id)
    except IntegrityError:
        print('old user')


def set_metro(message):
    metro = db.check_metro(message.text)
    if metro is None:
        msg = bot.send_message(message.chat.id, 'В Москве нет метро с таким названием! Попробуй еще раз.')
        bot.register_next_step_handler(msg, set_metro)
    else:
        db.set_metro(metro, message.chat.id)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                       ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
        rooms = str(db.get_rooms(message.chat.id))
        if rooms == '5':
            rooms = 'Студия'
        msg = bot.send_message(message.chat.id, 'Введенные параметры:\nСтанция: ' + str(db.get_metro(message.chat.id))
                               + '\nКомнаты:' + rooms + '\nЦена:'
                               + str(db.get_minprice(message.chat.id)) + '-' + str(db.get_maxprice(message.chat.id)),
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, param_select)


def set_ot(message):
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'Ты ввел(-а) не цифру, попробуй еще раз')
        bot.register_next_step_handler(msg, set_ot)
    elif len(message.text) > 7:
        msg = bot.send_message(message.chat.id, 'Ты ввел(-а) слишком большую цифру, попробуй еще раз')
        bot.register_next_step_handler(msg, set_ot)
    else:
        minprice = int(message.text)
        db.set_minprice(minprice, message.chat.id)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                       ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
        rooms = str(db.get_rooms(message.chat.id))
        if rooms == '5':
            rooms = 'Студия'
        msg = bot.send_message(message.chat.id,
                               'Введенные параметры:\nСтанция: ' + str(db.get_metro(message.chat.id)) + '\nКомнаты:'
                               + rooms + '\nЦена:' + str(db.get_minprice(message.chat.id)) + '-'
                               + str(db.get_maxprice(message.chat.id)),
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, param_select)


def set_do(message):
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'Ты ввел(-а) не цифру, попробуй еще раз')
        bot.register_next_step_handler(msg, set_do)
    elif len(message.text) > 7:
        msg = bot.send_message(message.chat.id, 'Ты ввел(-а) слишком большую цифру, попробуй еще раз')
        bot.register_next_step_handler(msg, set_do)
    else:
        maxprice = int(message.text)
        db.set_maxprice(maxprice, message.chat.id)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                       ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])

        rooms = str(db.get_rooms(message.chat.id))
        if rooms == '5':
            rooms = 'Студия'
        msg = bot.send_message(message.chat.id,
                               'Введенные параметры:\nСтанция: ' + str(db.get_metro(message.chat.id)) + '\nКомнаты:'
                               + rooms + '\nЦена:' + str(db.get_minprice(message.chat.id)) + '-'
                               + str(db.get_maxprice(message.chat.id)),
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, param_select)


def set_rooms(message):
    if message.text == 'Студия':
        db.set_rooms(5, message.chat.id)
    elif message.text == '1':
        db.set_rooms(1, message.chat.id)
    elif message.text == '2':
        db.set_rooms(2, message.chat.id)
    elif message.text == '3':
        db.set_rooms(3, message.chat.id)
    else:
        db.set_rooms(4, message.chat.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                   ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
    rooms = str(db.get_rooms(message.chat.id))
    if rooms == '5':
        rooms = 'Студия'
    msg = bot.send_message(message.chat.id,
                           'Введенные параметры:\nСтанция: ' + str(db.get_metro(message.chat.id)) + '\nКомнаты:'
                           + rooms + '\nЦена:' + str(db.get_minprice(message.chat.id)) + '-'
                           + str(db.get_maxprice(message.chat.id)),
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, param_select)


def get_flats_cyan(message):
    cyanreq = reqforms.CyanRequest()
    cyanreq.maxprice = db.get_maxprice(message.chat.id)
    cyanreq.minprice = db.get_minprice(message.chat.id)
    cyanreq.metro = db.get_cyan_metro(db.get_metro(message.chat.id))
    room_num = db.get_rooms(message.chat.id)
    if room_num is not None and room_num != 'None':
        rn = int(room_num)
        if rn == 5:
            cyanreq.room9 = 1
        elif rn == 1:
            cyanreq.room1 = 1
        elif rn == 2:
            cyanreq.room2 = 1
        elif rn == 3:
            cyanreq.room3 = 1
        elif rn == 4:
            cyanreq.room4 = 1
    print(vars(cyanreq))
    cyanres = requests.get('https://www.cian.ru/cat.php', vars(cyanreq), headers=headers)
    print(cyanres.url)
    parsed_cyan_search = html.fromstring(cyanres.text)
    cyan_links = parsed_cyan_search.xpath('//a [@class="header--28QlS"]/@href')
    cyan_titles = parsed_cyan_search.xpath('//div [@class="title--32t2O"]/text()')
    cyan_prices = parsed_cyan_search.xpath('//div [@class="header--29P2q"]/text()')
    cyan_metro_distance_cut = []
    cyan_address = parsed_cyan_search.xpath('//span [@itemprop="name"]/@content')
    results = []
    if db.get_metro(message.chat.id) == 'None':
        for i in range(len(cyan_links)):
            results.append(
                cyan_titles[i] + '\n' + cyan_prices[i] + '\n' + cyan_address[i] + '\n' + '\n' + str(cyan_links[i]))
    else:
        cyan_metro = parsed_cyan_search.xpath('//div [@class="underground-name--ExtF1"]/text()')
        cyan_metro_distance = parsed_cyan_search.xpath('//div [@class="remoteness--3GbHK"]/text()')
        for m in cyan_metro_distance:
            cyan_metro_distance_cut.append(m.replace('\xa0', ' ').replace('\n', '').replace('\r', ''))
        for i in range(len(cyan_links)):
            results.append(
                cyan_titles[i] + '\n' + cyan_prices[i] + '\n' + cyan_address[i] + '\n'
                + cyan_metro[i] + ' ' + cyan_metro_distance_cut[i] + '\n' + str(cyan_links[i]))
    return results


def get_flats_dom(message):
    if db.get_minprice(message.chat.id) > db.get_maxprice(message.chat.id):
        return []
    domreq = reqforms.DomofondRequest()
    domreq.PriceFrom = db.get_minprice(message.chat.id)
    domreq.PriceTo = db.get_maxprice(message.chat.id)
    if db.get_dom_room(db.get_rooms(message.chat.id)) is None and \
            db.get_dom_metro(db.get_metro(message.chat.id)) is None:
        link = 'https://www.domofond.ru/arenda-kvartiry-moskva-c3584'
    elif db.get_dom_room(db.get_rooms(message.chat.id)) is None and db.get_dom_metro(
            db.get_metro(message.chat.id)) is not None:
        link = 'https://www.domofond.ru/arenda-kvartiry-' + db.get_dom_metro(db.get_metro(message.chat.id))
    elif db.get_dom_metro(db.get_metro(message.chat.id)) is None and db.get_dom_room(
            db.get_rooms(message.chat.id)) is not None:
        link = 'https://www.domofond.ru' + db.get_dom_room(db.get_rooms(message.chat.id)) + 'moskva-c3584'
    else:
        link = 'https://www.domofond.ru' + db.get_dom_room(db.get_rooms(message.chat.id)) \
               + db.get_dom_metro(db.get_metro(message.chat.id))
    domres = requests.get(link, vars(domreq), headers=headers)
    print(domres.url)
    parsed_dom_search = html.fromstring(domres.text)
    flat_links = parsed_dom_search.xpath('//a [@itemprop="sameAs"]/@href')
    dom_titles = parsed_dom_search.xpath('//span[@class="e-tile-type m-max-width text-overflow"]/strong/text()')
    dom_prices = parsed_dom_search.xpath('//h2[@class="e-tile-price m-blue-link"]/text()')
    dom_prices_cut = []
    for i in dom_prices:
        dom_prices_cut.append(i.replace('\xa0', ''))
    dom_comission = parsed_dom_search.xpath('//span[@class="e-price-breakdown"]/text()')
    dom_comission_cut = []
    for c in dom_comission:
        dom_comission_cut.append(c.replace('\xa0', ' '))
    dom_addresses = parsed_dom_search.xpath('//span[@class="m-blue-link text-overflow m-max-width"]/text()')
    dom_metros = parsed_dom_search.cssselect('.e-metro-distance')
    dom_metros_cut = []
    for m in dom_metros:
        dom_metros_cut.append(m.text_content().replace('\r', ' ').replace('\n', '').lstrip().rstrip())
    results = []
    if len(flat_links) == len(dom_metros_cut):
        for i in range(len(flat_links)):
            results.append(
                dom_titles[i] + '\n' + dom_prices_cut[i] + '\n' + dom_comission_cut[i] + '\n' + dom_addresses[i] +
                '\n' + dom_metros_cut[i] + '\n' + 'https://www.domofond.ru' + flat_links[i])
    return results


def get_flats_av(message):
    if db.get_minprice(message.chat.id) > db.get_maxprice(message.chat.id):
        return []
    avreq = reqforms.AvitoRequest()
    avreq.pmin = db.get_minprice(message.chat.id)
    avreq.pmax = db.get_maxprice(message.chat.id)
    avreq.metro = db.get_avito_metro(db.get_metro(message.chat.id))
    if db.get_avito_room(db.get_rooms(message.chat.id)) is None:
        link = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok'
    else:
        link = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok' + \
               db.get_avito_room(db.get_rooms(message.chat.id))
    avres = requests.get(link, vars(avreq), headers=headers)
    print(avres.url)
    parsed_av_search = html.fromstring(avres.text)
    links = parsed_av_search.xpath('//a[@class = "item-description-title-link"]/@href')
    title = parsed_av_search.xpath('//a[@class = "item-description-title-link"]/text()')
    title_cut = []
    for s in title:
        title_cut.append(s[2:-2])
    price = parsed_av_search.xpath('//div[@class = "about "]/text()')
    price_cut = []
    for s in price:
        st = s[2:].rstrip()
        if st != '':
            price_cut.append(st)
    address = parsed_av_search.cssselect('.address')
    address_cut = []
    for s in address:
        address_cut.append(s.text_content().replace('\xa0', ' ').replace('\n', '').lstrip().rstrip())
    results = []
    print(len(title_cut))
    print(len(price_cut))
    print(len(address_cut))
    print(len(links))
    if len(price_cut) == len(title_cut):
        for i in range(0, len(title_cut)):
            results.append(
                title_cut[i] + '\n' + price_cut[i] + '\n' + address_cut[i] + '\n' + 'https://www.avito.ru' + links[i])
    return results


def param_select(message):
    if message.text == 'Ближайшее метро':
        msg = bot.send_message(message.chat.id, 'Отправь название станции метро',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, set_metro)
    elif message.text == 'От':
        msg = bot.send_message(message.chat.id, 'Отправь минимальную цену аренды',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, set_ot)
    elif message.text == 'До':
        msg = bot.send_message(message.chat.id, 'Отправь максимальную цену аренды',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, set_do)
    elif message.text == 'Количество комнат':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Студия', '1', '2', '3', '4+']])
        msg = bot.send_message(message.chat.id, 'Выбери желаемое количество комнат', reply_markup=keyboard)
        bot.register_next_step_handler(msg, set_rooms)
    elif message.text == 'Поиск':
        print('Search!!!')
        cyanres = get_flats_cyan(message)
        domres = get_flats_dom(message)
        avres = get_flats_av(message)
        full_res = domres + avres + cyanres
        shuffle(full_res)
        for r in full_res:
            db.write_result(message.chat.id, r)
        al_res = db.get_results(message.chat.id)
        try:
            first_mes_text = al_res[0]
        except:
            bot.send_message(message.chat.id, 'По твоему запросу ничего не нашлось!')
            restart(message)
            return
        bot.send_message(message.chat.id, first_mes_text, reply_markup=results_keyboard(0, message.chat.id))


def restart(message):
    db.delete_results(message.chat.id)
    db.delete_user(message.chat.id)


def results_keyboard(page, uid):
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = []
    if page > 0:
        buttons.append(telebot.types.InlineKeyboardButton(
            text='⬅', callback_data=str((page - 1))))
    buttons.append(telebot.types.InlineKeyboardButton(text='✔', callback_data='DONE'))
    if page < len(db.get_results(uid)) - 1:
        buttons.append(telebot.types.InlineKeyboardButton(
            text='➡', callback_data=str(page + 1)))
    keyboard.add(*buttons)
    return keyboard


@bot.callback_query_handler(func=lambda c: c.data)
def pages(c):
    if c.data == 'DONE':
        cmd_start(c.message)
        return
    try:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=db.get_results(c.message.chat.id)[int(c.data)],
            reply_markup=results_keyboard(int(c.data), c.message.chat.id))
    except IndexError:
        return


if __name__ == '__main__':
    bot.polling(none_stop=True)
