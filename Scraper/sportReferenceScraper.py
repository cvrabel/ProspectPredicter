# Chris Vrabel, 2018
# A script to scrap the sport reference page for college basketball players
# Gets the per game data for each season played

import requests
import json
import sys
import playerStatsDao as dao
from PlayerData import PlayerData

from bs4 import BeautifulSoup as BS

CURRENT_PLAYER = ""

def execute(year):
	with open('players.json') as f:
		playersJson = json.load(f)
	playerUrls = constructUrlAndScrape(playersJson["players"+year], playersJson["twos"], playersJson["threes"], playersJson["fours"])


def constructUrlAndScrape(playerList, twosList, threesList, foursList):
	baseString = "https://www.sports-reference.com/cbb/players/"
	endString = ".html";

	for player in playerList:
		playerNum = determinePlayerNum(player, twosList, threesList, foursList)
		nameList = player.split(" ")
		global CURRENT_PLAYER 
		CURRENT_PLAYER = nameList[0].lower() + "-" + nameList[1].lower() + "-" + playerNum
		url = baseString + CURRENT_PLAYER + endString
		scrapeUrl(url)


def determinePlayerNum(player, twosList, threesList, foursList):
	if player in twosList:
		return "2" 
	elif player in threesList:
		return "3"
	elif player in foursList:
		return "4"
	else:
		return "1"

def scrapeUrl(url):
	page = requests.get(url)
	soup = BS(page.content, 'html.parser')

	relevantData = soup.find_all("tr")
	for i in range(1, len(relevantData)):
		dataString = relevantData[i].get_text("/")
		listStats = dataString.split("/")
		if len(listStats) < 24:
			print("CHECK OUT: " + url)
		# Stop once we got all the individual season data
		if dataString[:6] == "Career":
			break

		valuesList = relevantData[i].find_all("td")
		
		seasonData = PlayerData(
			CURRENT_PLAYER, i, valuesList[0].text, valuesList[1].text, valuesList[2].text, valuesList[3].text, 
			valuesList[4].text, valuesList[5].text, valuesList[6].text, valuesList[7].text, valuesList[8].text, 
			valuesList[9].text, valuesList[10].text, valuesList[11].text, valuesList[12].text, valuesList[13].text, 
			valuesList[14].text, valuesList[15].text, valuesList[16].text, valuesList[17].text, valuesList[18].text, 
			valuesList[19].text, valuesList[20].text, valuesList[21].text, valuesList[22].text, valuesList[23].text, 
			valuesList[24].text, valuesList[25].text, valuesList[27].text)

		if sys.argv[2].lower() == 'true':
			dao.addItem(seasonData)

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
	
	print(CURRENT_PLAYER)
	return PlayerData(CURRENT_PLAYER, seasonNum, listStats[1], listStats[2], listStats[3], listStats[4],
		listStats[5], listStats[6], listStats[7], listStats[8], listStats[9], listStats[10], listStats[11], 
		listStats[12], listStats[13], threePointPercentage, listStats[14], listStats[15], listStats[16], 
		listStats[17], listStats[18], listStats[19], listStats[20], listStats[21], listStats[22], 
		listStats[23], listStats[24], listStats[25], listStats[26])

if __name__ == '__main__':
	if len(sys.argv) > 2:
		execute(sys.argv[1])
	else:
		print("Please enter \'true\' or \'false\' for if you want to write to DDB.")
