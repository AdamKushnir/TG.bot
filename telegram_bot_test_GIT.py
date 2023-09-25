import telebot
import requests
from bs4 import BeautifulSoup

slash = "-"*30

#Telegram bot
bot = telebot.TeleBot('BOT ID')
chat_id = "CHAT ID"

#Websides
url = 'fotball web'

#Def for actual parse
def parse_html():
   response = requests.get(url)
   soup = BeautifulSoup(response.text, 'html.parser')
   return soup

#NEWS

#daily news finder
def get_news_data_1(soup):
    daily_news = soup.find_all("h2", class_="titleH2")[0]
    daily_news1 = soup.find_all("h2", class_="titleH2")[1]
    daily_news_text1 = daily_news1.text
    daily_news_link1 = daily_news1.find("a")["href"]
    daily_news_text = daily_news.text
    daily_news_link = daily_news.find("a")["href"]
    return daily_news_text, daily_news_link, daily_news_text1, daily_news_link1

#Chelsea News
def get_news_data(soup):
   news = soup.find_all("a", class_="short-text")[0]
   news1 = soup.find_all("a", class_="short-text")[1]
   news_text = news.text
   news_link = news.get('href')
   news_text1 = news1.text
   news_link1 = news1.get('href')
   return news_text, news_link, news_text1, news_link1

#CHLSEA STANDING
def parse_and_fill_data(soup):
   table = soup.find_all("td", {'class': 'bordR'})[13:25]
   data = "🔵🦁 Chelsea:\n"
   headers = ["Место в турнире", "Сыграно игр", "Выигрыши", "Ничьи", "Поражения", "Забито голов", "Пропущено голов", "Разница заб./про.", "Очки"]
   standing_data = [table[i].text for i in range(9)]

   #formatting text for message
   for header, standing_value in zip(headers, standing_data):
       data += f"{header} | {standing_value}\n"
       data += f"{slash}\n"

   return data

#LAST MATCH

#Takes data for last match
def get_last_match_data(soup):
   #clubs
   LastMatch = soup.find_all("meta",{'itemprop': 'name'})[0]
   Last_Clubs = LastMatch["content"]

   #date-time
   Last_startDates = soup.find_all("meta",{'itemprop': 'startDate'})[0]
   last_date_time = Last_startDates["content"]
   L_date = last_date_time[:4]
   L_date1 = last_date_time[5:7]
   L_date2 = last_date_time[8:10]
   L_time = last_date_time[11:16]

   #score
   last_match_orange = soup.find_all('div', {'class': 'score-orange'})
   last_match_green = soup.find_all('div', {'class': 'score score-green'})
   last_match_red = soup.find_all('div', {'class': 'score score-red'})
   last_match_gray = soup.find_all('div', {'class': 'score score-gray'})

   Orange, Green, Red, Gray = None, None, None, None

   #check for the result of the game Win,Lose,Draw,Now
   if last_match_orange:
       Orange = f"{last_match_orange[0].text[2:3]}:{last_match_orange[0].text[6:7]}"
   if last_match_green:
       Green = f"{last_match_green[0].text[2:3]}:{last_match_green[0].text[6:7]}"
   if last_match_red:
       Red = f"{last_match_red[0].text[2:3]}:{last_match_red[0].text[6:7]}"
   if last_match_gray:
       Gray = f"{last_match_gray[0].text[2:3]}:{last_match_gray[0].text[6:7]}"

   result_message = None

   #check in locals variable
   if Orange:
       result_message = Orange
   elif Green:
       result_message = Green
   elif Red:
       result_message = Red
   elif Gray:
       result_message = Gray

   return Last_Clubs, L_date, L_date1, L_date2, L_time, result_message

#UPCOMING MATCH

#Takes data for next match
def get_next_match_data(soup):
   startDates = soup.find_all("meta",{'itemprop': 'startDate'})[1]
   startClub = soup.find_all('meta', {'itemprop': 'name'})[2]
   
   #formating data
   datetime = startDates["content"]
   Clubs = startClub["content"]
   date = datetime[:4]
   date1 = datetime[5:7]
   date2 = datetime[8:10]
   Time = datetime[11:16]

   return Clubs, date, date1, date2, Time

boosty = """
Привет! 🔵

Если вы хотите смотреть матчи с комментированием и наслаждаться английским футболом, подпишитесь на "Бусти".

Там вы найдете много чего, включая матчи с комментариями по подписке Disasi.

https://boosty.to/breakevens
"""

start_message = """
Добро пожаловать в чат с ботом Челси! 🌟 Здесь мы разделяем любовь к Челси. 

Если у вас есть идеи или предложения, не стесняйтесь написать мне @nougnt. 

Буду рад улучшать бота вместе с вами, Come on Blues!!! 💙🔵
"""

arizabalaga_stats = """
Кепа Аризабалага

Статистика в сезоне 2022/23:

Матчи - 20
Пропущенные голы - 18
Сухие матчи - 7
Пенальти отражено - 2
"""

silva_stats = """  
Thiago Silva

Статистика в сезоне 2022/23:

Матчи - 20
Пропущенные голы - 18
Сухие матчи - 7
"""

@bot.message_handler(commands=['start'])
def start(message):
   bot.send_message(message.chat.id, start_message)

@bot.message_handler(commands=['boosty'])
def start(message):
   bot.send_message(message.chat.id, boosty)

a = "Kepa"
@bot.message_handler(commands=['Arizabalaga'])
def arizabalaga(message):
   photo = open(f'c:/Users/kusni/OneDrive/Obrázky/PLAYERS/{a}.png', 'rb')
   bot.send_photo(message.chat.id, photo)
   bot.send_message(message.chat.id, arizabalaga_stats)
   

@bot.message_handler(commands=['Silva'])  
def silva(message):
   photo = open(r'c:/Users/kusni/OneDrive/Obrázky/PLAYERS/Silva.png', 'rb')
   bot.send_photo(message.chat.id, photo)
   bot.send_message(message.chat.id, silva_stats)

#News message
@bot.message_handler(commands=['news'])
def news_message(message):
   soup = parse_html()
   news_text, news_link, news_text1, news_link1 = get_news_data(soup)
   bot.send_message(message.chat.id,
f"""
⚡️⚡️⚡️
{news_text}
{slash[0:28]}
{news_link}

⚡️⚡️⚡️
{news_text1}
{slash[0:28]}
{news_link1}
""")
   
#Daily News message
@bot.message_handler(commands=['daily_news'])
def news_message(message):
   soup = parse_html()
   daily_news_text, daily_news_link, daily_news_text1, daily_news_link1 = get_news_data_1(soup)
   bot.send_message(message.chat.id,
f"""
⚡️⚡️⚡️
{daily_news_text}
{slash[0:28]}
{daily_news_link}

⚡️⚡️⚡️
{daily_news_text1}
{slash[0:28]}
{daily_news_link1}
""")
   
#upcoming match message
@bot.message_handler(commands=['match'])
def match(message):
   soup = parse_html()
   Clubs, date, date1, date2, Time = get_next_match_data(soup)
   bot.send_message(message.chat.id, 
f"""
⏳⏳⏳
{Clubs}
{slash[0:22]}
{date2}.{date1}.{date} - {Time}
{slash[0:22]}
Comon Blues 💙🔵
""")

#last match result message
@bot.message_handler(commands=['lastmatch'])
def lastmatch(message):
   soup = parse_html()
   Last_Clubs, L_date, L_date1, L_date2, L_time, result_message = get_last_match_data(soup)
   bot.send_message(message.chat.id, f"""
🔚🔚🔚
{Last_Clubs}
{slash[0:22]}
{L_date2}.{L_date1}.{L_date} - {L_time}
{slash[0:22]}
Счёт: {result_message}
""")

#standing message  
@bot.message_handler(commands=['standing'])
def show_standing(message):
   soup = parse_html()
   data = parse_and_fill_data(soup)
   bot.send_message(message.chat.id, data)

#Starting bot
bot.polling(none_stop=True)