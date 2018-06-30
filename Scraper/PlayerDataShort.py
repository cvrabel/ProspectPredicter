# Player per game stats for a season
class PlayerDataShort:

	def __init__(self, player, season, school, conference, games, minutes, fieldGoalsMade,
				fieldGoalsAttempted, fieldGoalPercentage, twoPointersMade, twoPointersAttempted,
				twoPointPercentage, threePointersMade, threePointersAttempted, threePointPercentage,
				freeThrowsMade, freeThrowsAttempted, freeThrowPercentage,
				totalRebounds, assists, steals, blocks, turnovers, personalFouls, points, strengthOfSchedule):
		self.player 				= player 					# 0
		self.season 				= season 					# 1
		self.school 				= school					# 2
		self.conference 			= conference				# 3
		self.games 					= games 					# 4
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
		self.totalRebounds			= totalRebounds				# 18
		self.assists				= assists					# 19
		self.steals					= steals					# 20
		self.blocks					= blocks					# 21
		self.turnovers				= turnovers					# 22
		self.personalFouls			= personalFouls				# 23
		self.points 				= points 					# 24
		self.strengthOfSchedule		= strengthOfSchedule		# 25
