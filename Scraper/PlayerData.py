# Player per game stats for a season
class PlayerData:

	def __init__(self, player, season, school, conference, games, gamesStarted, minutes, fieldGoalsMade,
				fieldGoalsAttempted, fieldGoalPercentage, twoPointersMade, twoPointersAttempted,
				twoPointPercentage, threePointersMade, threePointersAttempted, threePointPercentage,
				freeThrowsMade, freeThrowsAttempted, freeThrowPercentage, offensiveRebounds, defensiveRebounds,
				totalRebounds, assists, steals, blocks, turnovers, personalFouls, points, strengthOfSchedule, playerNBARating, ratingsStanding):
		self.player 				= player 					# 0
		self.season 				= season 					# 1
		self.school 				= school					# 2
		self.conference 			= conference				# 3
		self.games 					= games 					# 4
		self.gamesStarted 			= gamesStarted				# 5
		self.minutes 				= minutes 					# 6
		self.fieldGoalsMade 		= fieldGoalsMade 			# 7
		self.fieldGoalsAttempted 	= fieldGoalsAttempted 		# 8
		self.fieldGoalPercentage 	= fieldGoalPercentage 		# 9
		self.twoPointersMade 		= twoPointersMade			# 10
		self.twoPointersAttempted 	= twoPointersAttempted		# 11
		self.twoPointPercentage 	= twoPointPercentage		# 12
		self.threePointersMade		= threePointersMade			# 13
		self.threePointersAttempted = threePointersAttempted	# 14
		self.threePointPercentage	= threePointPercentage		# 15
		self.freeThrowsMade			= freeThrowsMade			# 16
		self.freeThrowsAttempted	= freeThrowsAttempted		# 17
		self.freeThrowPercentage	= freeThrowPercentage		# 18
		self.offensiveRebounds		= offensiveRebounds			# 19
		self.defensiveRebounds 		= defensiveRebounds			# 20
		self.totalRebounds			= totalRebounds				# 21
		self.assists				= assists					# 22
		self.steals					= steals					# 23
		self.blocks					= blocks					# 24
		self.turnovers				= turnovers					# 25
		self.personalFouls			= personalFouls				# 26
		self.points 				= points 					# 27
		self.strengthOfSchedule		= strengthOfSchedule		# 28
		self.playerNBARating		= playerNBARating			# 29
		self.ratingsStanding		= ratingsStanding			# 30

class PlayerDataEuro:

	def __init__(self, player, season, league, conference, games, gamesStarted, minutes, fieldGoalsMade,
				fieldGoalsAttempted, fieldGoalPercentage, twoPointersMade, twoPointersAttempted,
				twoPointPercentage, threePointersMade, threePointersAttempted, threePointPercentage,
				freeThrowsMade, freeThrowsAttempted, freeThrowPercentage, offensiveRebounds, defensiveRebounds,
				totalRebounds, assists, steals, blocks, turnovers, personalFouls, points, strengthOfSchedule):
		self.player 				= player 					# 0
		self.season 				= season 					# 1
		self.league 				= league					# 2
		self.games 					= games 					# 4
		self.gamesStarted 			= gamesStarted				# 5
		self.minutes 				= minutes 					# 6
		self.fieldGoalsMade 		= fieldGoalsMade 			# 7
		self.fieldGoalsAttempted 	= fieldGoalsAttempted 		# 8
		self.fieldGoalPercentage 	= fieldGoalPercentage 		# 9
		self.twoPointersMade 		= twoPointersMade			# 10
		self.twoPointersAttempted 	= twoPointersAttempted		# 11
		self.twoPointPercentage 	= twoPointPercentage		# 12
		self.threePointersMade		= threePointersMade			# 13
		self.threePointersAttempted = threePointersAttempted	# 14
		self.threePointPercentage	= threePointPercentage		# 15
		self.freeThrowsMade			= freeThrowsMade			# 16
		self.freeThrowsAttempted	= freeThrowsAttempted		# 17
		self.freeThrowPercentage	= freeThrowPercentage		# 18
		self.offensiveRebounds		= offensiveRebounds			# 19
		self.defensiveRebounds 		= defensiveRebounds			# 20
		self.totalRebounds			= totalRebounds				# 21
		self.assists				= assists					# 22
		self.steals					= steals					# 23
		self.blocks					= blocks					# 24
		self.turnovers				= turnovers					# 25
		self.personalFouls			= personalFouls				# 26
		self.points 				= points 					# 27
		self.strengthOfSchedule		= strengthOfSchedule		# 28

