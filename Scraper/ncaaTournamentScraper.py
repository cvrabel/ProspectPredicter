from bs4 import BeautifulSoup as BS

import requests

'''
Script to scrape the NCAA tournament pages on sports-reference.
Scrape each boxscore in the tournament, and find average pace.
'''

def scrapeAllTournaments():
	tournamentBaseUrl = "https://www.sports-reference.com/cbb/postseason/"
	tournamentEndUrl = "-ncaa.html"
	for i in range(1987, 2000):
		url = tournamentBaseUrl + str(i) + tournamentEndUrl
		page = requests.get(url)
		soup = BS(page.content, "html.parser")
		boxscores = soup.select("a[href*=boxscores/" + str(i) + "]")

def scrapeAllBoxscores():
	scrapedUrls = []
	gamePaces = []
	for boxscore in boxscores:
		boxscoreUrl = boxscore.get('href')
		if boxscoreUrl not in scrapedUrls:
			scrapedUrls.append(boxscoreUrl)
			gamePace = scrapeBoxscore(boxscoreUrl)
			gamePaces.append(gamePace)
			

def scrapeBoxscore(boxscoreUrl):
	sportsReferenceBase = "https://www.sports-reference.com"
	boxscorePage = requests.get(sportsReferenceBase + boxscoreUrl)
	boxscoreSoup = BS(boxscorePage.content, "html.parser")

	teamTotals = boxscoreSoup.find_all("tfoot")
	team1Stats = teamTotals[0].get_text("/").split("/")
	team2Stats = teamTotals[1].get_text("/").split("/")

	return calculateGamePace(team1Stats, team2Stats)


def calculateGamePace(team1Stats, team2Stats):
	return -1


