from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday2 = os.environ['BIRTH']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_other = os.environ["USER_OTHER"]
template_id = os.environ["TEMPLATE_ID"]
wedding = os.environ["WEDDING"]

def get_weather():
  url = "https://v0.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid=&city=江夏"
  res = requests.get(url).json()
  weather = res['data'][1]
  return weather['wea'], weather['tem1'], weather['tem2']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days+1

def get_wed_count():
  delta = datetime.strptime(wedding, "%Y-%m-%d")-today
  return delta.days+1

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days+1

def get_birthday2():
  next = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days+1

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temhigh, temlow = get_weather()
data = {"weather":{"value":wea},"temhigh":{"value":temhigh},"temlow":{"value":temlow},"love_days":{"value":get_count()},"wedding_days":{"value":get_wed_count()},"birthday_left":{"value":get_birthday()},"birthday_left_2":{"value":get_birthday2()},"words":{"value":get_words(), "color":get_random_color()}}
wm.send_template(user_id, template_id, data)
wm.send_template(user_other, template_id, data)
