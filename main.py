import telebot
from settings.settings import token, apiHash, apiToken, admins, botApiUrl
import functions.functions as func
import json
import requests
import time

bot = telebot.Telebot(token)
bot.remove_webhook()

with open('database/ads.json') as file:
	adsList = json.load(file)

def main():
	try:
		url = 'https://jdbiz.ru'
		html = func.getHtml(url)
		func.checkRepeat(adsList,func.getAds(html),admins,botApiUrl,bot)
		time.sleep(60)
	except Exception as e:
		print(e,2)
		main()

if __name__ == '__main__':
	while True:
		main()


	
