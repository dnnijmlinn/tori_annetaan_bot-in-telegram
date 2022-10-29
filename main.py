import telebot
import requests
import urllib.request
from telebot import types 
from sched import scheduler
from bs4 import BeautifulSoup as b

URL = 'https://www.tori.fi/uusimaa?q=&cg=0&w=109&st=g&ca=18&l=0&md=th'
API_KEY = '5679270918:AAGCFWgdMVWwICeNcAk8AZyXJTmMuL2QZWc'

bot = telebot.TeleBot(API_KEY)
@bot.message_handler(commands=['start'])

def cont(message): 
    cke = 1
    while True:
        def parser(url):
            r = requests.get(url)
            soup = b(r.text, 'html.parser')
            anekdots = soup.find_all('div', class_='li-title')
            return [c.text for c in anekdots]
        list_of_nimi = parser(URL)

        def hinta(url):
            r = requests.get(url)
            soup = b(r.text, 'html.parser')
            anekdots = soup.find_all('div', class_='list-details-container')
            return [c.text for c in anekdots]
        list_of_price = hinta(URL)

        html_page = urllib.request.urlopen("https://www.tori.fi/uusimaa?q=&cg=0&w=109&st=g&ca=18&l=0&md=th")
        def livcnk(html_page):
            soup = b(html_page, "html.parser")
            for link in soup.find_all('a', class_='item_row_flex'):
                return(link.get('href'))
        list_of_r = livcnk(html_page)
        
        markup = types.InlineKeyboardMarkup()
        btn_my_site= types.InlineKeyboardButton(text='Näytä mainos', url=list_of_r)
        markup.add(btn_my_site)
        if list_of_price[0] != cke:
            bot.send_message(message.chat.id,  'Nimi: ' + list_of_nimi[0] + ' \nHintä: ' + 'ilmainen', reply_markup = markup) # ' \nHintä: ' + list_of_price[0].strip()
            cke = list_of_price[0]
    scheduler.every(1).seconds.do(cont)

bot.polling(none_stop=True)