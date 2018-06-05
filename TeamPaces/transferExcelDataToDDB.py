# Chris Vrabel
# 5/25/17
# Prediting Game Probabilities

# This python file contains some helper methods used throughout the project.

import pandas as pd
import numpy as np
import os
import pickle
import classifier3
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import math
#Take in the master csv, and separate it into csv by game
def separateGames():

	data = pd.read_csv("pbp.csv")

	prevID = data["game_id"][0]
	first = True

	for row in data.itertuples():
		if(first==True):
			arr = np.array(list(row)[1:])
			print(arr)
			first=False
		elif(row.game_id == prevID):
			nextRow = list(row)[1:]
			print(nextRow)
			arr = np.vstack([arr, nextRow])

		else:
			filename = str(prevID) + '.csv'
			df = pd.DataFrame(data=arr, columns=list(data))
			df.to_csv('games/'+filename, index=False)
			
			arr = np.array(list(row)[1:])
			print(arr)

		prevID = row.game_id


def getScores(score):
	index = score.index('-')
	home = int(score[0 : index-1])
	away = int(score[index+2 : ])
	return home, away

def getTime(clock):
	index = clock.index(':')
	minutes = int(clock[0:index])
	seconds = int(clock[index+1:])
	return minutes*60 + seconds


def updateArray(arr, clock, score_diff, increment):
	if clock >= 540:
		arr[0] += increment
	elif clock < 540 and clock >= 360:
		arr[1] += increment
	elif clock < 360 and clock >= 180 and score_diff > 9:
		arr[2] += increment
	elif clock < 360 and clock >=180 and score_diff <= 9:
		arr[3] += increment
	elif clock < 180 and clock >=60 and score_diff > 7:
		arr[4] += increment
	elif clock < 180 and clock >=60 and score_diff <= 7:
		arr[5] += increment
	elif clock < 60 and score_diff > 5:
		arr[6] += increment
	elif clock < 60 and score_diff <= 5:
		arr[7] += increment

	return arr


def getExpectedPPP():

	possessions = [0]*8
	points = [0]*8
	for file in os.listdir("games/"):
		print(file)
		data = pd.read_csv("games/" + file)
		prev_home, prev_away = getScores(data.irow(0).score)
		prev_score = prev_home + prev_away
		prev_clock = 720
		for i in range(1, len(data)):
			row = data.irow(i)
			clock = getTime(row.play_clock)

			if str(row.score) != 'nan':
				new_home, new_away = getScores(row.score)
				new_score = new_home + new_away
				points = updateArray(points, clock, abs(new_home - new_away), new_score-prev_score)

				prev_home = new_home
				prev_away = new_away
				prev_score = new_score

			if "Made Shot" in row.event_type or ("Rebound" in row.event_type and "Normal" not in row.event_description) or \
				("Turnover" in row.event_type and prev_clock != clock) or "Free Throw 2 of 2" in str(row.event_description) or \
				"Free Throw 3 of 3" in str(row.event_description) or "End Period" in str(row.event_type):
				possessions = updateArray(possessions, clock, abs(prev_home-prev_away), 1)

			prev_clock = clock

			

	for p in range(0,8):
		print(str(points[p]) + " --- " + str(possessions[p]) + " --- " + str(points[p]/possessions[p]))



def getTimeoutPPP():

	timeouts = 0
	timeoutPoints = 0
	for file in os.listdir("games/"):
		print(file)
		data = pd.read_csv("games/" + file)
		
		for i in range(0, len(data)):
			row = data.iloc[i]

			if str(row.score) != 'nan':
				prev_home, prev_away = getScores(row.score)
				prev_score = prev_home + prev_away

			if("Timeout" in str(row.event_type)):
				new_home, new_away = prev_home, prev_away
				new_score = new_home + new_away
				timeouts += 1
				print("Timeouts: " + str(timeouts))
				print("timeoutPoints: " + str(timeoutPoints))
				n = i+1
				nxt = data.iloc[n]
				while True:
					if str(data.iloc[n].score) != 'nan':
						new_home, new_away = getScores(data.iloc[n].score)
						new_score = new_home + new_away

					if 'Made Shot' in nxt.event_type or 'Free Throw 2 of 2' in str(nxt.event_description) \
						or 'Free Throw 3 of 3' in str(nxt.event_description):
						timeoutPoints += new_score - prev_score
						prev_home = new_home
						prev_away = new_away
						prev_score = new_score
						break
					elif 'Missed Shot' in nxt.event_type or 'Turnover' in nxt.event_type or 'End Period' in nxt.event_type:
						break
					n += 1
					nxt = data.iloc[n]

	print(timeouts)
	print(timeoutPoints)


def getGameNames():
# Get teams playing the game
	games = []
	for file in os.listdir("games/"):
		df = pd.read_csv("games/" + file)
		homeName = ''
		awayName = ''
		for i in range(0, len(df)):
			row = df.iloc[i]
			if str(row.home_description) != 'nan' and str(row.player1_team) != 'nan':
				homeName = str(row.player1_team)
			if str(row.home_description) == 'nan' and str(row.away_description) != 'nan' and str(row.player1_team) != 'nan':
				awayName = str(row.player1_team)
			if str(row.home_description) != 'nan' and str(row.away_description) != 'nan':
				homeName = str(row.player1_team)
				if str(row.player2_team) != 'nan':
					awayName = str(row.player2_team)
				else:
					awayName = str(row.player3_team)

			if len(homeName) != 0 and len(awayName) != 0:
				games.append(homeName + '-' + awayName + " (" + file + ")")
				break

	games.sort()
	print(games)
	with open('game_names.pkl', 'wb') as f:
		pickle.dump(games, f, protocol=2)

#Our function for best fit line 
def func(x, a, b, c, d, e, f):
	return a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f

#Predict the probability using best fit curves
def pred(time, score):
	with open('pred_curves_5degree.pkl', 'rb') as f:
		curves = pickle.load(f)

	#Different to handle negatives and positives
	if score > 0:
		ceil = math.ceil(score)
		floor = math.floor(score)
		if floor == 0:
			remain = score
		else:
			remain = score % floor
	elif score < 0:
		ceil = math.floor(score)
		floor = math.ceil(score)
		if floor == 0:
			remain = score*-1
		else:
			remain = (score%floor)*-1
	else:
		ceil = floor = score

	indexHelp = 60
	pred = 0
	if ceil == floor:
		pred =  func(time, *curves[int(score)+indexHelp])
	else:
		cIndex = ceil + indexHelp
		fIndex = floor + indexHelp
		if cIndex > 120:
			cIndex = 120
		if fIndex > 120:
			fIndex = 120
		# print(cIndex)
		# print(fIndex)
		pred = (remain*func(time, *curves[cIndex]) + (1-remain)*func(time, *curves[fIndex])) 

	# If end of game, force prob to 1 or 0
	# If not end of game, don't allow prob of 1 or 0s
	if score >= 1 and time == 0:
		pred = 1
	elif score <= -1 and time==0:
		pred=0
	elif pred >= 1 and time>0 and score<10:
		pred = 0.9999
	elif pred <= 0 and time>0 and score>-10:
		pred = 0.0001
	elif pred > 1:
		pred = 1
	elif pred < 0:
		pred = 0.0001

	return pred

def addPredictions(filename):
	df = pd.read_csv("pbp.csv")

	with open('classifier_ot_2.pkl', 'rb') as f:
		classifier = pickle.load(f)

	predictions = []
	prev = 0
	print(prev)
	for i in range(0, len(df)):
		load = int(i/len(df) * 100)
		if load != prev:
			print(load)
			prev = load
		row = df.iloc[i]
		next_row = df.iloc[i+1] if (i < len(df)-1) else df.iloc[i]

		if str(row.score) != 'nan':
			home, away = classifier3.getScores(row.score) 
		else:
			pass

		if "Violation" in row.event_type or "Substitution" in row.event_type or "Ejection" in row.event_type:
			pass # Keep event the same as previous
		else:
			event = classifier3.getEvent(row, next_row)

		time = classifier3.getTime(row.play_clock)
		period = int(row.period)
		# if(period > 4):
		# 	time = time - 300

		event = event*classifier3.clutchAdj(time)
		score = home - away + event
		# prob = classifier.predict_proba([[time  /720, score /53]])
		# print(str(home) + "-" + str(away) + " -- " + str(event) + ", " + str(time) + " --- " + str(prob[0][1]))
		# predictions.append(prob[0][1])
		prob = pred(time, score)
		predictions.append(prob)

	df['win_probability'] = predictions

	df.to_csv(filename, index=False)


#Get the best fit curves
def getCurves():
	with open('classifier_ot_2.pkl', 'rb') as f:
		classifier = pickle.load(f)

	allVals = []
	#Get curves for score diff of -60 to 60
	for s in range(-60,61,1):
		print(s)
		values = []
		for t in range(0, 761, 10):
			probs = classifier.predict_proba([[t  /720, s /53]])
			prob = probs[0][1]
			if t == 0:
				if s > 0:
					prob = 1.1
				elif s < 0:
					prob = -.1
			elif t != 0:
				if prob >= 1:
					prob = 0.99
				if prob <= 0:
					prob = 0.01
			values.append([(t), prob])

		values = np.array(values)
		popt, pcov = curve_fit(func, values[:,0], values[:,1])
		
		allVals.append(popt)

	with open('pred_curves_5degree.pkl', 'wb') as f:
			pickle.dump(allVals, f, protocol=2)



# getCurves()
addPredictions("pbp_predictions.csv")		
# getGameNames()
# getTimeoutPPP()
# getExpectedPPP()
# separateGames()