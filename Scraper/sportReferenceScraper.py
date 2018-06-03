# Chris Vrabel, 2018
# A script to scrap the sport reference page for college basketball players
# Gets the per game data for each season played

import requests
import json
import sys
import playerStatsDao as dao
from SeasonStats import SeasonStats
from bs4 import BeautifulSoup as BS

CURRENT_PLAYER = ""
WRITE_TO_DB = "False"

def execute(year, write_to_db):
	global WRITE_TO_DB
	WRITE_TO_DB = write_to_db
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
		
		# Stop once we got all the individual season data
		if dataString[:6] == "Career":
			break

		seasonData = parseSeasonString(dataString, i)

		# Add the season data to DDB if true
		if WRITE_TO_DB.lower() == 'true':
			dao.addItem(seasonData)

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
	return SeasonStats(CURRENT_PLAYER, seasonNum, listStats[1], listStats[2], listStats[3], listStats[4], listStats[5],
		listStats[6], listStats[7], listStats[8], listStats[9], listStats[10], listStats[11], listStats[12], 
		listStats[13], threePointPercentage, listStats[14], listStats[15], listStats[16], listStats[17], listStats[18], 
		listStats[19], listStats[20], listStats[21], listStats[22], listStats[23], listStats[24], listStats[25], listStats[26])


if __name__ == '__main__':
	execute("2013", sys.argv[1])
