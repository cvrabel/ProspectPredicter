from decimal import Decimal

import pandas as pd
import boto3
import sys

'''
Script to read the data from CollegeBasketballPace.xlsx
and add the data to DDB in the correct format.
'''

def main():
	excel = pd.ExcelFile("CollegeBasketballPace.xlsx")
	for sheet_name in excel.sheet_names:
		if sheet_name != 'Master':
			sheet = excel.parse(sheet_name)
			handleSheet(sheet_name, sheet)
			print(sheet_name)

def handleSheet(year, sheet):
	numCols = len(sheet['Team'])
	for i in range(numCols):
		team = sheet['Team'][i]
		if sys.argv[1].lower() == 'true':
			addItem(year, team, sheet['Pace'][i])
		else:
			print('Not putting item for ' + year + " " + team)

def addItem(year, team, pace):
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
		main()
	else:
		print("Please enter \'true\' or \'false\' for if you want to write to DDB.")