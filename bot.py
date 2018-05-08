import requests
import telebot
from fake_useragent import UserAgent
from lxml import html

import config
import reqforms
import vedisclient

ua = UserAgent()
metros = {'Авиамоторная': 1, 'Автозаводская': 2, 'Академическая': 3}
# cyanreq = reqforms.CyanRequest()
domreq = reqforms.DomofondRequest()
avreq = reqforms.AvitoRequest()
allres = []

bot = telebot.TeleBot(config.token)
telebot.apihelper.proxy = {'https': 'socks5://telegram:telegram@kaisq.tgvpnproxy.me:1080'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}
proxy = {'https': 'socks5://telegram:telegram@kaisq.tgvpnproxy.me:1080'}


@bot.message_handler(commands=['start'])
def cmd_start(message):
    global allres
    allres = []
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                   ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
    msg = bot.send_message(message.chat.id, "Привет! Введи параметры квартиры твоей мечты ->", reply_markup=keyboard)
    vedisclient.set_state(message.chat.id, config.States.S_PARAMETERS.value)
    bot.register_next_step_handler(msg, param_select)


def set_metro(message):
    metro_code = metros.get(message.text)
    if metro_code is None:
        msg = bot.send_message(message.chat.id, 'В Москве нет метро с таким названием! Попробуй еще раз.')
        bot.register_next_step_handler(msg, set_metro)
    else:
        # cyanreq.metro = metro_code
        # domreq.metro = metro_code
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
        # cyanreq.minprice = minprice
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
        # cyanreq.maxprice = maxprice
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
        # cyanreq.room9 = 1
        avreq.link = 'https://www.avito.ru/moskva/kvartiry/sdam/studii'
    elif message.text == '1':
        # cyanreq.room1 = 1
        avreq.link = 'https://www.avito.ru/moskva/kvartiry/sdam/1-komnatnye'
    elif message.text == '2':
        # cyanreq.room2 = 1
        avreq.link = 'https://www.avito.ru/moskva/kvartiry/sdam/2-komnatnye'
    elif message.text == '3':
        # cyanreq.room3 = 1
        avreq.link = 'https://www.avito.ru/moskva/kvartiry/sdam/3-komnatnye'
    else:
        # cyanreq.room4 = 1
        avreq.link = 'https://www.avito.ru/moskva/kvartiry/sdam/4-komnatnye'
    vedisclient.set_state(message.chat.id, config.States.S_PARAMETERS)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in
                   ['Ближайшее метро', 'От', 'До', 'Количество комнат', 'Поиск']])
    msg = bot.send_message(message.chat.id, 'Введенные параметры:',
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, param_select)


'''
def get_flats_cyan():
    cyanres = requests.get(cyanreq.link, vars(cyanreq), headers={'User-Agent': str(ua.random)}, proxies=proxy)
    print(cyanres.url)
    parsed_cyan_search = html.fromstring(cyanres.text)
    flat_numbers = parsed_cyan_search.xpath('//head/script[6]/text()')[0]
    regexp = re.compile('\"searchResults\"\:\[.[\d,]*\]')
    search_results = regexp.search(flat_numbers).group(0)[17:].replace(']', '').split(',')
    search_results = [int(i) for i in search_results]
    results = []
    for i in range(len(search_results)):
        results.append(get_flat_cyan('https://www.cian.ru/rent/flat/' + str(search_results[i])))
        sleep(2)
    return results


def get_flat_cyan(url):
    page = requests.get(url, headers={'User-Agent': str(ua.random)}, proxies=proxy)
    print(page.url)
    parsed_flat = html.fromstring(page.text)
    title = parsed_flat.xpath('//h1/text()')[0]
    price = parsed_flat.xpath('//span[@class="price_value--XlUfS"]/span/@content')[0].replace('\xa0', '')
    geo = parsed_flat.xpath('//div[@class="geo--1poV5"]/span/@content')[0]
    metroname = parsed_flat.xpath('//a[@class="underground_link--1qgA6"]/text()')
    metrotime = parsed_flat.xpath('//span[@class="underground_time--3SZFY"]/text()')
    result = title + '\n' + price + '\n' + geo + '\n'
    if len(metroname) != 0:
        for i in range(len(metroname)):
            result += metroname[i] + metrotime[i] + '\n'
    result += page.url
    return result
'''


def get_flats_dom():
    domres = requests.get(domreq.link, vars(domreq), headers=headers)
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
    for i in range(len(flat_links)):
        results.append(
            dom_titles[i] + '\n' + dom_prices_cut[i] + '\n' + dom_comission_cut[i] + '\n' + dom_addresses[i] +
            '\n' + dom_metros_cut[i] + '\n' + 'https://www.domofond.ru' + flat_links[i])
    return results


'''def get_flat_dom(url):
    page = requests.get(url, headers=headers)
    parsed_flat = html.fromstring(page.text)
    title = parsed_flat.xpath('//h1/text()')[0]
    price = parsed_flat.xpath('//div[@itemprop = "price"]/text()')[0].replace('\xa0', '')
    address = parsed_flat.xpath('//a[@class = "e-listing-address-line"]/text()')[0]
    metro = parsed_flat.xpath('//div[@class="e-listing-address"]/p/text()')[1][2:-10]
    result = title + '\n' + price + '\n' + address + '\n' + metro + '\n' + url
    return result'''


def get_flats_av():
    av_prop_dict = vars(avreq);
    av_prop_dict.pop('link', None)
    avres = requests.get(avreq.link, av_prop_dict, headers=headers)
    parsed_av_search = html.fromstring(avres.text)
    links = parsed_av_search.xpath('//a[@class = "item-description-title-link"]/@href')
    for i in links:
        print(i)
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
    for i in range(0, len(title_cut)):
        results.append(
            title_cut[i] + '\n' + price_cut[i] + '\n' + address_cut[i] + '\n' + 'https://www.avito.ru/' + links[i])
    return results


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
        print('Search!!!')
        vedisclient.set_state(message.chat.id, config.States.S_RESULTS.value)
        # cyanres = get_flats_cyan()
        domres = get_flats_dom()
        avres = get_flats_av()
        global allres
        allres = avres
        try:
            first_mes_text = allres[0]
        except:
            bot.send_message(message.chat.id, 'По твоему запросу ничего не нашлось!')
            cmd_start()
            return
        bot.send_message(message.chat.id, first_mes_text, reply_markup=results_keyboard(0), )


def results_keyboard(page):
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = []
    if page > 0:
        buttons.append(telebot.types.InlineKeyboardButton(
            text='⬅', callback_data=str((page - 1))))
    if page < len(allres):
        buttons.append(telebot.types.InlineKeyboardButton(
            text='➡', callback_data=str(page + 1)))
    keyboard.add(*buttons)
    return keyboard


@bot.callback_query_handler(func=lambda c: c.data)
def pages(c):
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=allres[int(c.data)],
        parse_mode='Markdown',
        reply_markup=results_keyboard(int(c.data)))


if __name__ == '__main__':
    bot.polling(none_stop=True)
