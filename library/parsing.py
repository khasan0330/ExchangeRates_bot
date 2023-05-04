import requests
from bs4 import BeautifulSoup


def aloqabank():
    Aloqabank = 'https://aloqabank.uz/ru/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    html = requests.get(Aloqabank, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    block = soup.find('table', class_='exchange__table')
    currencies = block.find_all('tr')
    value = []
    for currency in currencies:
        value_purchase = currency.find_all('div', class_='exchange-value')
        if len(value_purchase) > 2:
            value.append(value_purchase[0].find('span').get_text())
            value.append(value_purchase[1].find('span').get_text())
            value.append(value_purchase[2].find('span').get_text())
            break
    return value


aloqabank()
