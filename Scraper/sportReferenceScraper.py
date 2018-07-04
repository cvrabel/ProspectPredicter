# Chris Vrabel, 2018
# A script to scrap the sport reference page for college basketball players
# Gets the per game data for each season played

import requests
import json
import sys
import playerStatsDao as dao
from PlayerData import PlayerData
from PlayerData import PlayerDataEuro

from bs4 import BeautifulSoup as BS

CURRENT_PLAYER = ""
ratingsJson = {}
with open('playerRatings.json') as f:
	ratingsJson = json.load(f)
sortedRatings = sorted(ratingsJson, key=ratingsJson.get)

def execute(start, end):
	with open('players.json') as f:
			playersJson = json.load(f)
	# for year in range(int(start), int(end)+1):
	# 	playerUrls = constructUrlAndScrape(playersJson["players"+str(year)], playersJson["twos"], playersJson["threes"], playersJson["fours"], playersJson["fives"])
	
	playerUrls = constructUrlAndScrape(playersJson["playersUndrafted"], playersJson["twos"], playersJson["threes"], playersJson["fours"], playersJson["fives"])	


def constructUrlAndScrape(playerList, twosList, threesList, foursList, fivesList):
	baseString = "https://www.basketball-reference.com/euro/players/" if (sys.argv[1] == 'EURO') else "https://www.sports-reference.com/cbb/players/"
	endString = ".html"

	for player in playerList:
		playerNum = determinePlayerNum(player, twosList, threesList, foursList, fivesList)
		playerNoPunctuation = player.replace("'", "").replace(".", "")
		nameList = playerNoPunctuation.split(" ")
		global CURRENT_PLAYER 
		CURRENT_PLAYER = nameList[0].lower() + "-" + nameList[1].lower() + "-" + playerNum
		url = baseString + CURRENT_PLAYER + endString
		scrapeUrl(url, player)


def determinePlayerNum(player, twosList, threesList, foursList, fivesList):
	if player in twosList:
		return "2" 
	elif player in threesList:
		return "3"
	elif player in foursList:
		return "4"
	elif player in fivesList:
		return "5"
	else:
		return "1"

def scrapeUrl(url, playerName):
	page = requests.get(url)
	soup = BS(page.content, 'html.parser')

	relevantData = soup.find_all("tr")
	breakAfter = False
	for i in range(1, len(relevantData)):
		dataString = relevantData[i].get_text("/")
		listStats = dataString.split("/")
		if len(listStats) < 22:
			print("CHECK OUT: " + url)
		# Stop once we got all the individual season data
		valuesList = relevantData[i].find_all("td")
		conference = valuesList[1].text
		year = i-1
		if dataString[:6] == "Career":
			breakAfter = True
			conference = "Conf"
		else:
			linkYearText = valuesList[0].find('a', href=True)["href"]
			year = int(linkYearText[len(linkYearText)-9:len(linkYearText)-5])
		rating = -1
		ratingsStanding = -1
		try:
			rating = ratingsJson[playerName]
			ratingsStanding = sortedRatings.index(playerName)
		except: 
			pass


		seasonData = PlayerData(
			CURRENT_PLAYER, year, valuesList[0].text, conference, valuesList[2].text, valuesList[3].text, 
			valuesList[4].text, valuesList[5].text, valuesList[6].text, valuesList[7].text, valuesList[8].text, 
			valuesList[9].text, valuesList[10].text, valuesList[11].text, valuesList[12].text, valuesList[13].text, 
			valuesList[14].text, valuesList[15].text, valuesList[16].text, valuesList[17].text, valuesList[18].text, 
			valuesList[19].text, valuesList[20].text, valuesList[21].text, valuesList[22].text, valuesList[23].text, 
			valuesList[24].text, valuesList[25].text, valuesList[27].text, rating, ratingsStanding)
		print(seasonData.player + " --- " + str(year))

		if sys.argv[3].lower() == 'true':
			dao.addItem(seasonData)

		if breakAfter:
			break

		# try:
		# 	seasonData = parseSeasonString(dataString, i)
		# 	# Add the season data to DDB if true
		# 	if sys.argv[2].lower() == 'true':
		# 		dao.addItem(seasonData)
		# except:
		# 	try:
		# 		seasonDataShort = parseSeasonStringShort(dataString, i)
		# 		# Add the season data to DDB if true
		# 		if sys.argv[2].lower() == 'true':
		# 			dao.addItemShort(seasonDataShort)
		# 	except:
		# 		print("Could not scrape: " + url)


def parseSeasonString(data, seasonNum):
	listStats = data.split("/")

	# Some players don't have a 3 point percentage in the stats.
	# At index14 is usually 3p%, so if the string is longer than 3 it is a percentage and we'll remove it.
	# If the string isn't longer than 3, then it is the FTM and this player doesn't have 3p% already.
	if len(listStats[14]) > 3:
		del listStats[14]
	# Because we deleted 3p%, we must calculate it.
	threePointPercentage = round(float(listStats[12])/float(listStats[13]), 4) if float(listStats[13]) else 0
	
	return PlayerData(CURRENT_PLAYER, seasonNum, listStats[1], listStats[2], listStats[3], listStats[4],
		listStats[5], listStats[6], listStats[7], listStats[8], listStats[9], listStats[10], listStats[11], 
		listStats[12], listStats[13], threePointPercentage, listStats[14], listStats[15], listStats[16], 
		listStats[17], listStats[18], listStats[19], listStats[20], listStats[21], listStats[22], 
		listStats[23], listStats[24], listStats[25], listStats[26])

if __name__ == '__main__':
	if len(sys.argv) > 3:
		execute(sys.argv[1], sys.argv[2])
	else:
		print("Please enter startyear, endyear, and \'true\' or \'false\' for if you want to write to DDB.")
