# Author Zachary Morlan
# create the dailyOperations object

class DailyOperations(object):
	limit = 20
	instructors = []
	
	def __init__(self, day, instructors):
		super(DailyOperations, self).__init__()
		self.day = day
		self.instructors = instructors
	
	def description(self):
		return print(self.instructors)


class instructors(object):
	"""docstring for instructors"""
	def __init__(self, name, hours):
		super(instructors, self).__init__()
		self.name = name
		self.hours = hours

instructors = ["Jules","Jon", "Wesley", "Zachary"]
duration = ['1','3.5','3','5']
day = "Monday"
monday = DailyOperations(day,instructors)
print(monday.instructors)