import json
import boto3
import numpy

def main():
	dynamodb = boto3.resource("dynamodb")
	table = dynamodb.Table("PlayerCollegePerGame")
	response = table.scan()
	data = response['Items']

	previousPlayer = data[0]["player"]
	for row in range(0, len(data)):




def findRatingAndPut():


def getAverageRatings():


def writeListToCSV(lst):
	header = ["Name", "Season", "School", "Games", "Games Started", "2P"]