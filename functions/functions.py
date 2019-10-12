import requests
import bs4
import json

def getHtml(url):
	r = requests.get(url)
	return r.text

def getAds(html):
	soup = bs4.BeautifulSoup(html,'lxml')
	section = soup.find('section', class_ = 'board-list')
	container = section.find('div', class_ = 'container')
	div = container.find('div', class_ = 'list-item__table')
	div = div.find('div', class_ = 'list')
	ads = div.find_all('div', class_ = 'item-wrp')
	return ads

def getHref(ad):
	item = ad.find('div', class_ = 'item')
	a = item.find('a', class_ = 'item__photo')
	href = a.get('href')
	return href

def checkRepeat(adsList,ads,admins,botApiUrl,bot):
	for ad in ads:
		if getHref(ad) in adsList:
			break
		else:
			href = getHref(ad)
			adsList.append(href)
			info = getInfo(href)
			if len(info) == 2:
				p = requests.get(info[1])
				out = open("photo/1.jpg", "wb")
				out.write(p.content)
				out = open("photo/1.jpg",'rb')
				bot.send_photo(photo = out, chat_id = admins[0],caption = info[0])
				out.close()
				
			else:
				bot.send_message(chat_id = admins[0], text = info[0])
			with open('database/ads.json','w') as f:
				json.dump(adsList,f)


def getInfo(href):
	html = getHtml(href)
	soup = bs4.BeautifulSoup(html, 'lxml')
	description = getDesctiption(soup)
	try:
		photo = getPhoto(soup)
	except Exception as e:
		print(e,1)
		photo = 0
	title = getTitle_Price(soup)
	text = title.strip() + description.strip() + '\n' + href
	if photo:
		infoList = [text, photo]
	else:
		infoList = [text]
	return infoList


def getDesctiption(soup):
	mainDiv = soup.find('div', class_ = 'col-main item-main')
	mainDiv = mainDiv.find('div',class_ = 'item-tabs')
	descriptionDiv = mainDiv.find('div', class_ = 'tab active')
	descriptionText = descriptionDiv.find('div', class_ = 'text').text
	return descriptionText

def getPhoto(soup):
	mainDiv = soup.find('div', class_ = 'col-main item-main')
	mainDiv = mainDiv.find('div',class_ = 'item-main-info')
	photoDiv = mainDiv.find('img')
	href = photoDiv.get('src')
	return href

def getTitle_Price(soup):
	mainDiv = soup.find('div', class_ = 'col-main item-main')
	titleDiv = mainDiv.find('div', class_ = 'item-main-sutitle')
	h1 = titleDiv.find('h1').text
	price = titleDiv.find('strong').text
	text = '{0}\n{1}'.format(h1,price)
	return text

