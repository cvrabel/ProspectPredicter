import requests
import json

from bs4 import BeautifulSoup as BS


def scrapeNbaRating():
	with open('players.json') as f:
		playersJson = json.load(f)
	playerUrls = constructUrlAndScrape(playersJson["playersUndrafted"], playersJson["twos"], playersJson["threes"], playersJson["fours"])

def constructUrlAndScrape(playerList, twosList, threesList, foursList):
	baseString = "https://www.basketball-reference.com/players/"
	endString = ".html"

	for player in playerList:
		print(player)
		playerNum = determinePlayerNum(player, twosList, threesList, foursList)
		nameList = player.split(" ")
		playerUrl = nameList[1].lower()[:5] + nameList[0].lower()[:2]  + playerNum
		url = baseString + nameList[1].lower()[:1] + "/" + playerUrl + endString
		createNameMappingJson(player, playerUrl)
		rating = getPlayerRating(url)
		createRatingMappingJson(player, rating)

def determinePlayerNum(player, twosList, threesList, foursList):
	if player in twosList:
		return "02" 
	elif player in threesList:
		return "03"
	elif player in foursList:
		return "04"
	else:
		return "01"

def getPlayerRating(url):
	page = requests.get(url)
	soup = BS(page.content, 'html.parser')
	rating = 0
	try:
		blingSoup = soup.find(id="bling")
		firstYear = float(soup.find_all("tr")[1].get_text("/")[:4])
		ratingFromBling = True
		print("here")
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
			careerStats = soup.find("tfoot").get_text("/").split("/")
			minutesPlayed = float(careerStats[2]) * float(careerStats[4])
			rating = min(46, minutesPlayed*0.0018)
		if (firstYear > 2006):
			rating *= 11/(2018-firstYear)
		if ratingFromBling:
			rating += 45
	except:
		pass
	return rating

def parseAwardForNumber(award):
	indexOfX = award.find('x')
	if indexOfX != -1:
		return float(award[:indexOfX])
	return 1

def createNameMappingJson(playerName, playerUrl):
	playerDict = {playerName : playerUrl }
	print(playerDict)
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

	try:
		with open('playerRatings.json') as f:
			mappingsJson = json.load(f)
		mappingsJson.update(playerDict)
	except:
		mappingsJson = playerDict

	with open('playerRatings.json', 'w') as f:
		json.dump(mappingsJson, f, indent=2)

if __name__ == '__main__':
	scrapeNbaRating()
