import telebot
import pandas as pd
import requests
import emoji
import time as tm
from telebot import types
from bs4 import BeautifulSoup
from collections import defaultdict



TOKEN = ''

HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
           'accept': '*/*'}

LINK = 'https://auto.ria.com'

bot = telebot.TeleBot(TOKEN)

def create_csv(brand):
    
    def get_url_brand(brand):
        
        if brand.lower() == 'audi' or brand.lower() == 'ауди':
            URL = 'https://auto.ria.com/uk/newauto/marka-audi/'

        elif brand.lower() == 'mercedes' or brand.lower() == 'mercedes-benz' or brand.lower() == 'мерседес':
            URL = 'https://auto.ria.com/uk/newauto/marka-mercedes-benz/'

        elif brand.lower() == 'bmw' or brand.lower() == 'бмв':
            URL = 'https://auto.ria.com/uk/newauto/marka-bmw/'  

        elif brand.lower() == 'volkswagen' or brand.lower() == 'фольц' or brand.lower() == 'фольцваген':
            URL = 'https://auto.ria.com/uk/newauto/marka-volkswagen/' 

        elif brand.lower() == 'skoda' or brand.lower() == 'шкода':
            URL = 'https://auto.ria.com/uk/newauto/marka-skoda/'

        elif brand.lower() == 'renault' or brand.lower() == 'рено':
            URL = 'https://auto.ria.com/uk/newauto/marka-renault/'

        elif brand.lower() == 'toyota' or brand.lower() == 'тойота' or brand.lower() == 'тайота':
            URL = 'https://auto.ria.com/uk/newauto/marka-toyota/'

        elif brand.lower() == 'opel' or brand.lower() == 'опель':
            URL = 'https://auto.ria.com/uk/newauto/marka-opel/'

        elif brand.lower() == 'ford' or brand.lower() == 'форд':
            URL = 'https://auto.ria.com/uk/newauto/marka-ford/'

        elif brand.lower() == 'kia' or brand.lower() == 'киа':
            URL = 'https://auto.ria.com/uk/newauto/marka-kia/'

        elif brand.lower() == 'mazda' or brand.lower() == 'мазда':
            URL = 'https://auto.ria.com/uk/newauto/marka-mazda/'

        elif brand.lower() == 'porsche' or brand.lower() == 'порш' or brand.lower() == 'порше':
            URL = 'https://auto.ria.com/uk/newauto/marka-porsche/'

        elif brand.lower() == 'honda' or brand.lower() == 'хонда':
            URL = 'https://auto.ria.com/uk/newauto/marka-honda/'

        elif brand.lower() == 'nissan' or brand.lower() == 'нисан' or brand.lower() == 'ниссан':
            URL = 'https://auto.ria.com/uk/newauto/marka-nissan/'

        elif brand.lower() == 'mitsubishi' or brand.lower() == 'мицубиси':
            URL = 'https://auto.ria.com/uk/newauto/marka-mitsubishi/'

        elif brand.lower() == 'lexus' or brand.lower() == 'лексус':
            URL = 'https://auto.ria.com/uk/newauto/marka-lexus/'

        elif brand.lower() == 'fiat' or brand.lower() == 'фиат':
            URL = 'https://auto.ria.com/uk/newauto/marka-fiat/'

        elif brand.lower() == 'jaguar' or brand.lower() == 'ягуар':
            URL = 'https://auto.ria.com/uk/newauto/marka-jaguar/'

        elif brand.lower() == 'volvo' or brand.lower() == 'вольво' or brand.lower() == 'вольва':
            URL = 'https://auto.ria.com/uk/newauto/marka-volvo/'

        elif brand.lower() == 'citroen' or brand.lower() == 'ситроен':
            URL = 'https://auto.ria.com/uk/newauto/marka-citroen/'

        elif brand.lower() == 'land rover' or brand.lower() == 'ленд ровер':
            URL = 'https://auto.ria.com/uk/newauto/marka-land-rover/'

        elif brand.lower() == 'subaru' or brand.lower() == 'субару' or brand.lower() == 'субара' :
            URL = 'https://auto.ria.com/uk/newauto/marka-subaru/'

        elif brand.lower() == 'suzuki' or brand.lower() == 'сузуки':
            URL = 'https://auto.ria.com/uk/newauto/marka-suzuki/'

        elif brand.lower() == 'chery' or brand.lower() == 'чери':
            URL = 'https://auto.ria.com/uk/newauto/marka-chery/'

        return URL

    URL = get_url_brand(brand)


    def get_html(url, params=None):
        r = requests.get(url, headers=HEADERS, params=params)
        return r

    def get_parse_count(html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find_all('span', class_='mhide')
        if pagination:
            return int(pagination[-1].get_text())
        else:
            return 1


    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='proposition')

        cars = []
        
        for item in items:
            cars.append({
                'title': item.find('div', class_='proposition_title').get_text().strip(),
                'transmition':  item.find('div', class_='proposition_information').get_text().rsplit('  ', 4)[3].strip(),
                'region': item.find('div', class_='proposition_information').find_next('span', class_='item region').get_text().strip(),
                'drive_unit': item.find('div', class_='proposition_information').get_text().rsplit('  ', 4)[4].strip(),
                'engine_volume': item.find('div', class_='proposition_information').get_text().rsplit('  ', 4)[0].rsplit('•')[-1].strip(),
                'engine_fuel': item.find('div', class_='proposition_information').get_text().rsplit('  ', 4)[0].rsplit('•')[0].strip(),
                'link': LINK + item.find('a', class_='proposition_link').get('href').strip(),
                'price_uan': item.find('span', class_='size16').get_text().strip(),
                'price_usd': int(item.find('div', class_='proposition_price').get_text().rsplit('•')[0].rsplit('$')[0].replace(' ', '').strip())
            })
        #print(len(cars))
        return cars


    def parse():
        
        html = get_html(URL)
        if html.status_code == 200:
            cars = []
            all_cars = []
            pages_count = get_parse_count(html.text)

            for page in range(1, pages_count + 1):
                #print(f'Парсинг страницы {page} из {pages_count}')
                html = get_html(URL, params={'page': page})
                cars.extend(get_content(html.text))
                all_cars = cars 
    
        return all_cars

    #parse()

    def all_cars_to_dataframe(all_cars):
        
        cars = defaultdict(list)

        for car in all_cars:
            cars['title'].append(car['title'])
            cars['engine_fuel'].append(car['engine_fuel'])
            cars['engine_volume'].append(car['engine_volume'])
            cars['transmition'].append(car['transmition'])
            cars['drive_unit'].append(car['drive_unit'])
            cars['region'].append(car['region'])
            cars['link'].append(car['link'])
            cars['price_uan'].append(car['price_uan'])
            cars['price_usd'].append(car['price_usd'])

        
        all_cars_data = pd.DataFrame(cars)
        all_cars_data.to_csv(f'Cars.csv')
            
    all_cars_to_dataframe(parse())

def create_region_csv(region):

    cars = pd.read_csv('Cars.csv', index_col=0)

    def input_region(cars, region):
 
        cars_by_region = cars.loc[cars['region'] == region]

        cars_by_region.to_csv('Cars_by_region.csv')

        return cars_by_region
    
    input_region(cars, region)


def create_price_csv(price):

    cars = pd.read_csv('Cars_by_region.csv')

    def replaced_price(input_price):

        input_price = input_price.rsplit('-')
        price = []
        for item in input_price:
            price.append(int(item.strip()))

        return price

    price = replaced_price(price)
    

    def input_price(cars, price):


        cars_by_price = cars.loc[(cars['price_usd'] >= price[0]) & (cars['price_usd'] <= price[-1])]

        cars_by_price.to_csv('Cars_by_price.csv')

        return cars_by_price
    
    input_price(cars, price)


def get_car(cars):

    cars = pd.read_csv('Cars_by_price.csv')
    cars.sample()
    car = cars.to_dict()

    return 



@bot.message_handler(commands=['start'])
def command_start(message):
    start_message = emoji.emojize("Доброго здоров'ячка, дорогий друг.\n"
    "           Тебя вітає Marcus🤖\n""Я бот для пошуку твого майбутнього авто :recycle:\n\nМої можливості:\n:white_check_mark:"
    "Пошук авто по ціні;\n:white_check_mark:Пошук авто по регіону.", use_aliases=True)
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/info', '/brand')
    bot.send_message(message.chat.id, start_message)
    bot.send_message(message.from_user.id, emoji.emojize("Для повно розуміння, як працює бот натисніть /info :blue_book::closed_book:", use_aliases=True), reply_markup=start_markup)
    bot.send_message(message.from_user.id, "Введіть ⌨️ /hide для видалення клавіатури ", reply_markup=start_markup)

@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_message(message.chat.id, "🤖 /start - Введи старт для початку співбесіди\n")

@bot.message_handler(commands=['info'])
def command_info(message):

    info_message = emoji.emojize("1) Бот взаємодіє з сайтом auto.ria.com :car::small_orange_diamond::blue_car:\n\n"
                                 "2) :soon:Чому бот, так довго реагує на функцію /brand:warning:?\n"
                                 "Бот сортує інформацію (її може бути дуже багато)\n"
                                 "В середньму, ця функція виконується на протязі 30 секунд, якщо автівок данної марки більше за 200 екземлярів.\n\n"
                                 "3) Зауваження::bangbang:БОТ ВИКОРИСТОВЄ ТІЛЬКИ НОВІ АВТО:bangbang:\n\n"
                                 "            :point_right:Дякую за увагу:point_left:\n\n"
                                 "Натисніть /start для початку взаємодії з боттом:kissing_heart::boom:", use_aliases=True)

    info_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    info_markup.row('/start')
    bot.send_message(message.from_user.id, info_message  ,reply_markup=info_markup)


@bot.message_handler(commands=['hide'])
def command_hide(message):
	hide_markup = types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, "⌨Очікую команду /start 💤...", reply_markup=hide_markup)

@bot.message_handler(commands=['brand'])
def command_get_brand(message):
    brand_markup = types.ReplyKeyboardMarkup(True, True)
    brand_markup.row('Audi', 'Mercedes', 'BMW') 
    brand_markup.row('Volkswagen', 'Skoda', 'Renault') 
    brand_markup.row('Toyota', 'Opel', 'Ford')
    brand_markup.row('Kia', 'Mazda', 'Porsche')
    brand_markup.row('Honda', 'Nissan', 'Mitsubishi') 
    brand_markup.row('Lexus', 'Fiat', 'Jaguar') 
    brand_markup.row('Volvo', 'Citroen', 'Land Rover') 
    brand_markup.row('Subaru', 'Suzuki', 'Chery')
    brand_markup.row('/hide')
    sent = bot.send_message(message.chat.id, emoji.emojize(':heavy_check_mark:Введи бренд авто:', use_aliases=True), reply_markup=brand_markup)
    bot.register_next_step_handler(sent, add_brand)							  
	
def add_brand(message):

    if message.text == '/hide':
        hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "⌨Очікую команду /start 💤...", reply_markup=hide_markup)
    
    else:
   
        try:
            bot.send_message(message.chat.id, emoji.emojize("Аналізую данні :recycle:", use_aliases=True))
            create_csv(message.text)
            
            
        except:
            bot.send_message(message.chat.id, "❌ Ви ввели не коректну назву!")
        
        #brand = open('Cars.csv', 'rb')
        #bot.send_document(message.chat.id, brand)

        region_markup = types.ReplyKeyboardMarkup(True, True)
        region_markup.row('Київ','Вінниця', 'Дніпро (Дніпропетровськ)') 
        region_markup.row('Донецька обл.', 'Житомир') 
        region_markup.row('Запоріжжя', 'Івано-Франківськ')
        region_markup.row('Кропивницький (Кіровоград)', 'Луцьк')
        region_markup.row('Львів', 'Миколаїв', 'Одеса') 
        region_markup.row('Полтава', 'Рівне' 'Суми') 
        region_markup.row('Тернопіль', 'Ужгород', 'Харків') 
        region_markup.row('Херсон', 'Хмельницький')
        region_markup.row('Черкаси', 'Чернівці', 'Чернігів')
        region_markup.row('/hide', '/brand')
        sent = bot.send_message(message.chat.id, emoji.emojize(':heavy_check_mark:Тепер введи регіон для пошуку:', use_aliases=True), reply_markup=region_markup)
        bot.register_next_step_handler(sent, add_region)

def add_region(message):

    if message.text == '/hide':
        hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "⌨Очікую команду /start 💤...", reply_markup=hide_markup)

    elif message.text == '/brand':
        brand_markup = types.ReplyKeyboardMarkup(True, True)
        brand_markup.row('Audi', 'Mercedes', 'BMW') 
        brand_markup.row('Volkswagen', 'Skoda', 'Renault') 
        brand_markup.row('Toyota', 'Opel', 'Ford')
        brand_markup.row('Kia', 'Mazda', 'Porsche')
        brand_markup.row('Honda', 'Nissan', 'Mitsubishi') 
        brand_markup.row('Lexus', 'Fiat', 'Jaguar') 
        brand_markup.row('Volvo', 'Citroen', 'Land Rover') 
        brand_markup.row('Subaru', 'Suzuki', 'Chery')
        brand_markup.row('/hide')
        sent = bot.send_message(message.chat.id, emoji.emojize(':heavy_check_mark:Введи бренд авто:', use_aliases=True), reply_markup=brand_markup)
        bot.register_next_step_handler(sent, add_brand)							  

    else:

        try: 
            create_region_csv(message.text)
        
        except:
            bot.send_message(message.chat.id, "❌ Ви ввели не коректну назву!")
        
        #region = open('Cars_by_region.csv', 'rb')
        region_csv = pd.read_csv('Cars_by_region.csv')

        if region_csv.empty == True:
            bot.send_message(message.chat.id, 'В данному регіоні авто не знайдено!')

            region_markup = types.ReplyKeyboardMarkup(True, True)
            region_markup.row('Київ','Вінниця', 'Дніпро (Дніпропетровськ)') 
            region_markup.row('Донецька обл.', 'Житомир') 
            region_markup.row('Запоріжжя', 'Івано-Франківськ')
            region_markup.row('Кропивницький (Кіровоград)', 'Луцьк')
            region_markup.row('Львів', 'Миколаїв', 'Одеса') 
            region_markup.row('Полтава', 'Рівне' 'Суми') 
            region_markup.row('Тернопіль', 'Ужгород', 'Харків') 
            region_markup.row('Херсон', 'Хмельницький')
            region_markup.row('Черкаси', 'Чернівці', 'Чернігів')
            region_markup.row('/hide','/brand')
            sent = bot.send_message(message.chat.id, emoji.emojize(':heavy_check_mark:Введи регіон для пошуку:', use_aliases=True), reply_markup=region_markup)
            bot.register_next_step_handler(sent, add_region)
        
        else:
            #bot.send_document(message.chat.id, region)

            cost_markup = types.ReplyKeyboardMarkup(True, True)
            cost_markup.row('2000 - 4000', '4000 - 8000') 
            cost_markup.row('8000 - 12000', '12000 - 16000') 
            cost_markup.row('16000 - 22000', '22000 - 30000')
            cost_markup.row('30000 - 45000', '45000 - 90000')
            cost_markup.row('100000 - 200000', '200000 - 500000')
            cost_markup.row('/hide', '/brand')
            sent = bot.send_message(message.chat.id, emoji.emojize(':heavy_check_mark:Введи ціну:money_with_wings: для пошуку:', use_aliases=True), reply_markup=cost_markup)
            bot.register_next_step_handler(sent, add_price)

def add_price(message):

    if message.text == '/hide':
        hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "⌨Очікую команду /start 💤...", reply_markup=hide_markup)
    
    elif message.text == '/brand':
        brand_markup = types.ReplyKeyboardMarkup(True, True)
        brand_markup.row('Audi', 'Mercedes', 'BMW') 
        brand_markup.row('Volkswagen', 'Skoda', 'Renault') 
        brand_markup.row('Toyota', 'Opel', 'Ford')
        brand_markup.row('Kia', 'Mazda', 'Porsche')
        brand_markup.row('Honda', 'Nissan', 'Mitsubishi') 
        brand_markup.row('Lexus', 'Fiat', 'Jaguar') 
        brand_markup.row('Volvo', 'Citroen', 'Land Rover') 
        brand_markup.row('Subaru', 'Suzuki', 'Chery')
        brand_markup.row('/hide')
        sent = bot.send_message(message.chat.id, emoji.emojize(':heavy_check_mark:Введи бренд авто:', use_aliases=True), reply_markup=brand_markup)
        bot.register_next_step_handler(sent, add_brand)		
    else:

        try:
            create_price_csv(message.text)
        
        except:
            bot.send_message(message.chat.id, "❌ Ви ввели не коректну назву!")
        
        #price =  open('Cars_by_price.csv', 'rb')
        price_csv = pd.read_csv('Cars_by_price.csv')
        if price_csv.empty == True:
            bot.send_message(message.chat.id, emoji.emojize('За такою ціною авто не знайдено!', use_aliases=True))
            
            cost_markup = types.ReplyKeyboardMarkup(True, True)
            cost_markup.row('2000 - 4000', '4000 - 8000') 
            cost_markup.row('8000 - 12000', '12000 - 16000') 
            cost_markup.row('16000 - 22000', '22000 - 30000')
            cost_markup.row('30000 - 45000', '45000 - 90000')
            cost_markup.row('100000 - 200000', '200000 - 500000')
            cost_markup.row('/hide', '/brand')
            sent = bot.send_message(message.chat.id, emoji.emojize('Введи ціну:money_with_wings: для пошуку:', use_aliases=True), reply_markup=cost_markup)
            bot.register_next_step_handler(sent, add_price)
        
        else:
            #bot.send_document(message.chat.id, price)
            
            cars = pd.read_csv('Cars_by_price.csv')
            car = cars.sample(n=1).to_dict()
            car_to_user_title = f'{car["title"]}'.replace('{', '').replace('}', '').rsplit(':')[-1].replace("'",'').strip()
            car_to_user_link = f'{car["link"]}'.replace('{', '').replace('}', '').rsplit(':')[-1].replace("'",'').replace('//','').strip()
            output = f'{car_to_user_title}\n\n {car_to_user_link}'
            bot.send_message(message.chat.id, emoji.emojize('Як вам ця ластівка:car::interrobang:', use_aliases=True))
            bot.send_message(message.chat.id, output)


while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		tm.sleep(1)
    
    