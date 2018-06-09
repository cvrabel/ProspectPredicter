import boto3
from decimal import Decimal
from PlayerData import PlayerData
from boto3.dynamodb.types import TypeSerializer

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PlayerCollegePerGame')

def addItem(item: PlayerData):
	response = table.put_item(
		Item={
			'player' 				: item.player,
			'season' 				: item.season,
			'school' 				: item.school,
			'conference'			: item.conference,
			'games'					: serialize(item.games),
			'gamesStarted'			: serialize(item.gamesStarted),
			'minutes'				: serialize(item.minutes),
			'fieldGoalsMade'		: serialize(item.fieldGoalsMade),
			'fieldGoalsAttempted'	: serialize(item.fieldGoalsAttempted),
			'fieldGoalPercentage'	: serialize(item.fieldGoalPercentage),
			'twoPointersMade'		: serialize(item.twoPointersMade),
			'twoPointersAttempted'	: serialize(item.twoPointersAttempted),
			'twoPointPercentage'	: serialize(item.twoPointPercentage),
			'threePointersMade'		: serialize(item.threePointersMade),
			'threePointersAttempted': serialize(item.threePointersAttempted),
			'threePointPercentage'	: serialize(item.threePointPercentage),
			'freeThrowsMade'		: serialize(item.freeThrowsMade),
			'freeThrowsAttempted'	: serialize(item.freeThrowsAttempted),
			'freeThrowPercentage'	: serialize(item.freeThrowPercentage),
			'offensiveRebounds'		: serialize(item.offensiveRebounds),
			'defensiveRebounds'		: serialize(item.defensiveRebounds),
			'totalRebounds'			: serialize(item.totalRebounds),
			'assists'				: serialize(item.assists),
			'steals'				: serialize(item.blocks),
			'turnovers'				: serialize(item.turnovers),
			'personalFouls'			: serialize(item.personalFouls),
			'points'				: serialize(item.points),
			'strengthOfSchedule'	: serialize(item.strengthOfSchedule)
		})
	print("PutItem Succeeded")

def serialize(floatValue):
	if floatValue == '':
		floatValue = 0
	return Decimal(str(floatValue))


if __name__ == '__main__':
	print("NOPE")