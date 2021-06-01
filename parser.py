import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict


HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
           'accept': '*/*'}

LINK = 'https://auto.ria.com'

def create_csv(brand):

    def get_url_brand(brand):

        if brand == 'audi' or brand == 'ауди':
            URL = 'https://auto.ria.com/uk/newauto/marka-audi/'

        elif brand == 'mercedes' or brand == 'mercedes-benz' or brand == 'мерседес':
            URL = 'https://auto.ria.com/uk/newauto/marka-mercedes-benz/'

        elif brand == 'bmw' or brand == 'бмв':
            URL = 'https://auto.ria.com/uk/newauto/marka-bmw/'  

        elif brand == 'volkswagen' or brand == 'фольц' or brand == 'фольцваген':
            URL = 'https://auto.ria.com/uk/newauto/marka-volkswagen/' 

        elif brand == 'skoda' or brand == 'шкода':
            URL = 'https://auto.ria.com/uk/newauto/marka-skoda/'

        elif brand == 'renault' or brand == 'рено':
            URL = 'https://auto.ria.com/uk/newauto/marka-renault/'

        elif brand == 'toyota' or brand == 'тойота' or brand == 'тайота':
            URL = 'https://auto.ria.com/uk/newauto/marka-toyota/'

        elif brand == 'opel' or brand == 'опель':
            URL = 'https://auto.ria.com/uk/newauto/marka-opel/'

        elif brand == 'ford' or brand == 'форд':
            URL = 'https://auto.ria.com/uk/newauto/marka-ford/'

        elif brand == 'kia' or brand == 'киа':
            URL = 'https://auto.ria.com/uk/newauto/marka-kia/'

        elif brand == 'mazda' or brand == 'мазда':
            URL = 'https://auto.ria.com/uk/newauto/marka-mazda/'

        elif brand == 'porsche' or brand == 'порш' or brand == 'порше':
            URL = 'https://auto.ria.com/uk/newauto/marka-porsche/'

        elif brand == 'honda' or brand == 'хонда':
            URL = 'https://auto.ria.com/uk/newauto/marka-honda/'

        elif brand == 'nissan' or brand == 'нисан' or brand == 'ниссан':
            URL = 'https://auto.ria.com/uk/newauto/marka-nissan/'

        elif brand == 'mitsubishi ' or brand == 'мицубиси':
            URL = 'https://auto.ria.com/uk/newauto/marka-mitsubishi/'

        elif brand == 'lexus' or brand == 'лексус':
            URL = 'https://auto.ria.com/uk/newauto/marka-lexus/'

        elif brand == 'fiat' or brand == 'фиат':
            URL = 'https://auto.ria.com/uk/newauto/marka-fiat/'

        elif brand == 'jaguar' or brand == 'ягуар':
            URL = 'https://auto.ria.com/uk/newauto/marka-jaguar/'

        elif brand == 'volvo' or brand == 'вольво' or brand == 'вольва':
            URL = 'https://auto.ria.com/uk/newauto/marka-volvo/'

        elif brand == 'citroen' or brand == 'ситроен':
            URL = 'https://auto.ria.com/uk/newauto/marka-citroen/'

        elif brand == 'land rover' or brand == 'ленд ровер':
            URL = 'https://auto.ria.com/uk/newauto/marka-land-rover/'

        elif brand == 'subaru' or brand == 'субару' or brand == 'субара' :
            URL = 'https://auto.ria.com/uk/newauto/marka-subaru/'

        elif brand == 'suzuki' or brand == 'сузуки':
            URL = 'https://auto.ria.com/uk/newauto/marka-suzuki/'

        elif brand == 'chery' or brand == 'чери':
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
            
        else:
            print('ERROR')

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
        print(all_cars_data)
        all_cars_data.to_csv(f'Cars.csv')
            

    all_cars_to_dataframe(parse())

create_csv()
