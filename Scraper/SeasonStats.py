# Player per game stats for a season
class SeasonStats:

	def __init__(self, season, school, conference, games, gamesStarted, minutes, fieldGoalsMade,
				fieldGoalsAttempted, fieldGoalPercentage, twoPointersMade, twoPointersAttempted,
				twoPointPercentage, threePointersMade, threePointersAttempted, threePointPercentage,
				freeThrowsMade, freeThrowsAttempted, freeThrowPercentage, offensiveRebounds, defensiveRebounds,
				totalRebounds, assists, steals, blocks, turnovers, personalFouls, points, strengthOfSchedule):
		self.season 				= season 					# 0
		self.school 				= school					# 1
		self.conference 			= conference				# 2
		self.games 					= games 					# 3
		self.gamesStarted 			= gamesStarted				# 4
		self.minutes 				= minutes 					# 5
		self.fieldGoalsMade 		= fieldGoalsMade 			# 6
		self.fieldGoalsAttempted 	= fieldGoalsAttempted 		# 7
		self.fieldGoalPercentage 	= fieldGoalPercentage 		# 8
		self.twoPointersMade 		= twoPointersMade			# 9
		self.twoPointersAttempted 	= twoPointersAttempted		# 10
		self.twoPointPercentage 	= twoPointPercentage		# 11
		self.threePointersMade		= threePointersMade			# 12
		self.threePointersAttempted = threePointersAttempted	# 13
		self.threePointPercentage	= threePointPercentage		# 14
		self.freeThrowsMade			= freeThrowsMade			# 15
		self.freeThrowsAttempted	= freeThrowsAttempted		# 16
		self.freeThrowPercentage	= freeThrowPercentage		# 17
		self.offensiveRebounds		= offensiveRebounds			# 18
		self.defensiveRebounds 		= defensiveRebounds			# 19
		self.totalRebounds			= totalRebounds				# 20
		self.assists				= assists					# 21
		self.steals					= steals					# 22
		self.blocks					= blocks					# 23
		self.turnovers				= turnovers					# 24
		self.personalFouls			= personalFouls				# 25
		self.points 				= points 					# 26
		self.strengthOfSchedule		= strengthOfSchedule		# 27
