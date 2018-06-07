from bs4 import BeautifulSoup as BS
from decimal import Decimal

import requests
import boto3

'''
Script to scrape the NCAA tournament pages on sports-reference.
Scrape each boxscore in the tournament, find average pace, add to DDB.
'''

def scrapeAllTournaments():
	tournamentBaseUrl = "https://www.sports-reference.com/cbb/postseason/"
	tournamentEndUrl = "-ncaa.html"
	for i in range(1987, 1997):
		year = str(i)
		url = tournamentBaseUrl + year + tournamentEndUrl
		page = requests.get(url)
		soup = BS(page.content, "html.parser")
		boxscores = soup.select("a[href*=boxscores/" + year + "]")
		paceForYear = scrapeAllBoxscoresFindAvgPace(boxscores)
		if(sys.argv[1].lower == "true"):
			addItem(str(i), 'Average', paceForYear)
		else:
			print('Not putting item for ' + year)

def scrapeAllBoxscoresFindAvgPace(boxscores):
	scrapedUrls = []
	gamePaces = []
	for boxscore in boxscores:
		boxscoreUrl = boxscore.get('href')
		if boxscoreUrl not in scrapedUrls:
			scrapedUrls.append(boxscoreUrl)
			try:
				gamePace = scrapeBoxscore(boxscoreUrl)
				gamePaces.append(gamePace)
			except:
				print("Can't get pace for " + boxscoreUrl)

	return sum(gamePaces) / len(gamePaces)
			
def scrapeBoxscore(boxscoreUrl):
	sportsReferenceBase = "https://www.sports-reference.com"
	boxscorePage = requests.get(sportsReferenceBase + boxscoreUrl)
	boxscoreSoup = BS(boxscorePage.content, "html.parser")

	teamTotals = boxscoreSoup.find_all("tfoot")
	team1Stats = teamTotals[0].get_text("/").split("/")
	team2Stats = teamTotals[1].get_text("/").split("/")
	# print(team1Stats)
	# print(team2Stats)
	return calculateGamePace(team1Stats, team2Stats)

def calculateGamePace(team1Stats, team2Stats):
	team1FGA = float(team1Stats[3])
	team1FTA = float(team1Stats[12])
	team1ORB = float(team1Stats[15])
	team1TOV = float(team1Stats[21])

	team2FGA = float(team2Stats[3])
	team2FTA = float(team2Stats[12])
	team2ORB = float(team2Stats[15])
	team2TOV = float(team2Stats[21])

	return 0.5*(team1FGA + team1TOV - 0.9*team1ORB + 0.475*team1FTA) + 0.5*(team2FGA + team2TOV - 0.9*team2ORB + 0.475*team2FTA)

def addItem(year: str, team: str, pace):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('CollegeTeamPace')
	response = table.put_item(
		Item={
			'team' 	: team,
			'year'	: year,
			'pace' 	: Decimal(str(pace)),
		})
	print("Put item for the " + year + " " + team)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		scrapeAllTournaments()
	else:
		print("Please enter \'true\' or \'false\' for if you want to write to DDB.")
