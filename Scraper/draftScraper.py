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

	for i in range(2010, 2019):
		url = baseUrl + str(i) + endUrl
		page = requests.get(url)
		soup = BS(page.content, "html.parser")
		tables = soup.find_all("tr")
		# scrapeTablesForPlayerNames(str(i), tables)
		scrapeEachDraftTableAndGetRatings(str(i), tables)


def scrapeEachDraftTableAndGetRatings(year, tables):
	for i in range(2, len(tables)):
		try:
			playerRow = tables[i]
			playerName, rating = getPlayerRating(playerRow)
			if rating != -1:
				createRatingMappingJson(playerName, rating)

		except:
			print("FAILED: " + playerRow.get_text("/")[3])
			continue


def getPlayerRating(playerRow):
	rating = 0
	try:
		playerLinkObject = playerRow.select("a[href*=/players/]")[0]
		playerUrl = playerLinkObject["href"]
		url = "https://www.basketball-reference.com" + playerUrl
		page = requests.get(url)
		soup = BS(page.content, "html.parser")
		playerName = playerLinkObject.text
		# createNameMappingJson(playerName, playerUrl)

		blingSoup = soup.find(id="bling")
		firstYear = float(soup.find_all("tr")[1].get_text("/")[:4])
		ratingFromBling = True
		if blingSoup is not None :
			bling = blingSoup.get_text("/").split("/")
			allDef = 0.5
			allStar = 1.5
			allNba = 2
			dpoy = 2
			mvp = 5
			fmvp = 3
			
			for award in bling:
				if "All-Defensive" in award:
					rating += parseAwardForNumber(award)*allDef
				elif "All Star" in award:
					rating += parseAwardForNumber(award)*allStar
				elif "All-NBA" in award or "All-ABA" in award:
					rating += parseAwardForNumber(award)*allNba
				elif "Def. POY" in award:
					rating += parseAwardForNumber(award)*dpoy
				elif "Finals MVP" in award:
					rating += parseAwardForNumber(award)*fmvp
				elif "AS MVP" in award:
					continue
				elif "MVP" in award:
					rating += parseAwardForNumber(award)*mvp
		if (rating == 0):
			ratingFromBling = False
			minutesPlayed = float(playerRow.find_all("td")[6].text)
			rating = min(46, minutesPlayed*0.0018)
		if (firstYear > 2006):
			rating *= 11/(2018-firstYear)
		if ratingFromBling:
			rating += 45
	except:
		rowToArray = playerRow.get_text("/").split("/")
		for i in range(2,4):
			if rowToArray[i].find(" ") != -1:
				return rowToArray[i], rating
		return -1
	return playerName, rating

def parseAwardForNumber(award):
	indexOfX = award.find('x')
	if indexOfX != -1:
		return float(award[:indexOfX])
	return 1

def scrapeTablesForPlayerNames(year, tables):
	players = []
	for i in range(2, len(tables)):
		try:
			player = tables[i].select("a[href*=/players/]")[0].text
			players.append(player)
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

def createNameMappingJson(playerName, playerUrl):
	brefAlias = playerUrl[11:playerUrl.find(".")]
	playerDict = {playerName : brefAlias }
	mappingsJson = {}

	try:
		with open('brefNameMappings.json') as f:
			mappingsJson = json.load(f)
		mappingsJson.update(playerDict)
	except:
		mappingsJson = playerDict

	with open('brefNameMappings.json', 'w') as f:
		json.dump(mappingsJson, f, indent=2)

def createRatingMappingJson(playerName, rating):
	playerDict = {playerName : rating }
	mappingsJson = {}
	print(playerDict)

	jsonFileName = 'playerRatings.json'

	try:
		with open(jsonFileName) as f:
			mappingsJson = json.load(f)
		mappingsJson.update(playerDict)
	except:
		mappingsJson = playerDict

	with open(jsonFileName, 'w') as f:
		json.dump(mappingsJson, f, indent=2)

if __name__ == '__main__':
	scrapeDrafts()
