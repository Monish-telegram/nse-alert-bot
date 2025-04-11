import time
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = '7273216211:AAGL_i-MgswUU1TDlabLvKn90_YHhjmQrq4'
CHAT_ID = '6832850562'
RSS_FEED_URL = 'http://www.nseindia.com/content/RSS/Financial_Results.xml'

sent_titles = set()

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'disable_web_page_preview': True
    }
    requests.post(url, data=payload)

def check_rss():
    try:
        response = requests.get(RSS_FEED_URL)
        root = ET.fromstring(response.content)

        for item in root.findall('./channel/item'):
            title = item.find('title').text
            link = item.find('link').text
            pubDate = item.find('pubDate').text

            if title not in sent_titles:
                sent_titles.add(title)
                message = f"📢 *New NSE Earnings Released!*\n\n{title}\n📅 {pubDate}\n🔗 {link}"
                send_telegram_message(message)
    except Exception as e:
        print(f"Error fetching or sending update: {e}")

send_telegram_message("✅ Test Alert: This is a simulated earnings release.")

while True:
    check_rss()
    time.sleep(120)
