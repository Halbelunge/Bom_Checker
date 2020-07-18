import requests
from bs4 import BeautifulSoup
import urllib.request


#sources to check
#actual Source name you check for
fail_source = ['ebay.de','ebay.com','ebay.de','ebay.com','aliexpress'] 
#names that will appear in message
fail_source_name = ['ebay_de','ebay_com','ebay_wrong_link_de','ebay_wrong_link_com','aliexpress']
#bussword lines that are checked for
fail_strings = ['Artikel nicht mehr verfügbar ist','the item is no longer available','Anscheinend existiert diese Seite nicht','Looks like this page is missing.','the page you requested can not be found']

#false Links for failsafe check
faillink = [requests.get('https://www.ebay.de/itm/333310834326')]
faillink.append(requests.get('https://www.ebay.com/itm/333310834326'))
faillink.append(requests.get('https://www.ebay.de/itm/2-x-433-Mhz-Antenne-fur-Sender-Empfanger-Helical-Spiral-Arduino-Raspberry-ESP/333257247255'))
faillink.append(requests.get('https://www.ebay.com/itm/2-x-433-Mhz-Antenne-fur-Sender-Empfanger-Helical-Spiral-Arduino-Raspberry-ESP/333257247255'))
faillink.append(requests.get('https://de.aliexpress.com/item/4000917929337.html'))

#Links for BOM and Telegram Bot
BOM_URL = ""
BOT_Token = 'BOTTOKEN'
CHAT_ID = CHAT_ID
BOT_URL = 'https://api.telegram.org/bot' + BOT_Token + '/' 

#global_Variables
failsafe = 0
failsafe_fail = -1
number_of_died_links = 0

#Printstrings; change if you want an other language
toomanysources = 'Zu viele Quellen oder Fehlertext fehlend!'
failsafe_works = 'Failsafe works!'
failsafe_died = 'Failsafe died at '
time_to_panic = '! Time to panic!'
link_died_in = 'Link gestorben in '
all_links_are_working = "Alle Links funktionieren noch"
x_links_died = " sind insgesamt gestorben!"

def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id

def last_update():
    response = requests.get(BOT_URL + "getUpdates")
    response = response.json()
    result = response["result"]
    return result[len(result)-1]

def send_telegram_message(message_text):
    chat_id = CHAT_ID #get_chat_id(last_update())
    params = {"chat_id": chat_id, "text": message_text}
    response = requests.post(BOT_URL + "sendMessage", data=params)
    return response


#print('Artikel nicht mehr verfügbar ist.' in r.text)
if(len(fail_source) != len(fail_strings)):
    print(toomanysources)
    send_telegram_message(toomanysources)

for searching in range(len(fail_source)):
    if(fail_strings[searching] in faillink[searching].text):
        failsafe += 1
        print(' '+fail_source_name[searching]+'  ', end='')
        print(fail_strings[searching] in faillink[searching].text)
    else:
        print(' '+fail_source[searching], end='')
        print(fail_strings[searching] in faillink[searching].text)
        failsafe_fail = searching
if(failsafe == len(fail_source)):
   send_telegram_message(failsafe_works)
else: 
    send_telegram_message(failsafe_died + fail_source_name[failsafe_fail] + time_to_panic)

html_page = urllib.request.urlopen(BOM_URL)
soup = BeautifulSoup(html_page, "html.parser")
for link in soup.findAll('a'):
   # print(link.get('href'))
    if(link.get('href') != ''):
        link_contens = requests.get(link.get('href'))
        print(link.get('href'))
        for searching in range(len(fail_source)):
            if(fail_source[searching] in link.get('href')):
                if(fail_strings[searching] in link_contens):
                    send_telegram_message(link_died_in + fail_source[searching])
                    send_telegram_message(link.get('href'))
                    number_of_died_links += 1
                else:
                    print('nope',fail_source[searching])
if(number_of_died_links <= 0):
    send_telegram_message(all_links_are_working)
else:
    send_telegram_message(number_of_died_links + x_links_died)
#print('finish')



   
