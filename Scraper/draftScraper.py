from bs4 import BeautifulSoup as BS

import requests
import json

'''
Script to scrape the drafts and get the players.
Add the players to the existing players json which originally only had 2013.
'''

def scrapeDrafts():
	baseUrl = "https://www.basketball-reference.com/draft/NBA_"
	endUrl = ".html"

	for i in range(1987, 2012):
		url = baseUrl + str(i) + endUrl
		page = requests.get(url)
		soup = BS(page.content, "html.parser")
		tables = soup.find_all("tr")
		scrapeTables(str(i), tables)

def scrapeTables(year, tables):
	players = []
	for i in range(2, len(tables)):
		try:
			player = tables[i].select("a[href*=/players/]")[0].text
			players.append(player)
			print(player)
		except:
			continue
	addToJson(year, players)

def addToJson(year, players):
	playerDict = {"players"+year : players }

	with open('players.json') as f:
		playerJson = json.load(f)

	playerJson.update(playerDict)

	with open('players.json', 'w') as f:
		json.dump(playerJson, f, indent=2)

if __name__ == '__main__':
	scrapeDrafts()
