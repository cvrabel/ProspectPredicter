# Script to get yearly stats, get school pace from that year
# Then calculate the players' per100 stats for the year.
# Dumps the per100 stats into a CSV.
import json
import boto3
import numpy

from Scraper.PlayerData import PlayerData
from boto3.dynamodb.conditions import Key, Attr

def main():
	dynamodb = boto3.resource("dynamodb")
	table = dynamodb.Table("PlayerCollegePerGame")
	paceTable = dynamodb.Table("CollegeTeamPace")
	response = table.scan()
	data = response['Items']


	previousPlayer = data[0]["player"]
	playerGamesPlayedEachSeason = []
	playerPer100StatsEachSeason = []
	careerYear = None
	for row in range(0, len(data)):
		item = data[row]
		player = item["player"]


		if player != previousPlayer:
			previousPlayer = player
			careerPer100Stats = calculatePer100StatsForCareer(playerGamesPlayedEachSeason, playerPer100StatsEachSeason)
			writePer100StatsToCSV(careerPer100Stats)
			continue

		year = item["season"]
		print(year)
		paceYear = str(year - 1)
		school = item["school"]
		if year > 5:
			# yearData = PlayerData(item["player"], item["season"], item["school"])
		
			paceResponse = paceTable.query(
				KeyConditionExpression=Key('team').eq(school) & Key('year').eq(paceYear))
			paceItem = paceResponse[u'Items']
			print(paceItem)
			# calculatePer100StatsForYear(yearData, )


# def getAverageRatings():
def calculatePer100StatsForCareer(playerGamesPlayedEachSeason, playerPer100StatsEachSeason):
	print("TODO")

def writePer100StatsToCSV(lst):
	header = ["Name", "Season", "School", "Games", "Games Started", "2P"]


if __name__ == '__main__':
	main()