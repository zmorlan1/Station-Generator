# Author Zach Morlan
# Creates Object to store weekly  employee schedule
import instructor
import pandas


class Schedule(object):

	timeframe = "Weekly"
	"""docstring for Schedule"""
	def __init__(self, data):
		super(Schedule, self).__init__()
		self.schedule = data
		self.weekDays = {}

	def add_day(self, week_day,data):

		new_Day = day(week_day,data)
		self.weekDays.update({len(self.weekDays)+1:new_Day})
	def createWeeklySchedule(self,data_dict):
	
		global schedule
		global days_dict
	   #global employee_list
	
		for key in data_dict:
			data_dict[key] = createLists(self.schedule,data_dict[key])
			self.add_day(key,data_dict[key])

		for key in self.weekDays:
			self.weekDays[key].createShifts()

		return	
	
	def listReturn(self,x):
		for key in self.weekDays:
			for y in self.weekDays[key].shifts:
				shift = str(self.weekDays[key].name)+" "+str(self.weekDays[key].shifts[y].time)
				if x.lower() == shift.lower(): 
					return self.weekDays[key].shifts[y].employees
class day(object):

	"""docstring for day"""
	def __init__(self, name,data):
		super(day, self).__init__()
				
		self.name = name
		self.shifts_info = data
		self.shifts = {}
			
	def add_Shift (self,time,employees):

		new_shift = shift(time,employees)
		self.shifts.update({len(self.shifts)+1:new_shift})

	# Creates and adds shift to day object
	def createShifts(self):
		shift_dic = self.splitByShift(self.shifts_info)	
		for key in shift_dic:
			self.add_Shift(key,shift_dic[key])

	# Splits list by AM and PM shift
	def splitByShift(self,list):
		shifts = {"AM":"Instructors","PM":"Instructors"}
		count = 0
		i = 0
		am_list = []
		pm_list = []
		for x in list:
			if x[0] == "Coaches":
				count+=1	
			elif count == 2:
				break
			else:
				i+=1
		i+=1		
		shifts["AM"] = list[1:i]
		shifts["PM"] = list[i+1:]
		return shifts
	

class shift(object):

	"""docstring for shift"""
	def __init__(self,time,employees):
		super(shift, self).__init__()
		self.time = time
		self.employees = createInstructorList(employees)

# Removes null values from lists	
# NOTE CHANGE: duration will not be used but Average Adventure levels
def removeNulls(list_A, list_B):
	
	list_A = [x for x in list_A if pandas.isnull(x) == False]
	list_B = [x for x in list_B if pandas.isnull(x) == False]
	results = list(zip(list_A,list_B))
	return  results

# Takes dataframe and splits into lists by day 
def createLists(df,dict_value):

	col_list = df[dict_value].values.tolist()
	return splitLists(col_list)

# Splits each list value into instructors and duration
# NOTE: Code could be added to schedule object
def splitLists(list):
	list_A = [i[0] for i in list]
	list_B = [i[1] for i in list]
	return removeNulls(list_A, list_B)

# Creates a list of instructor objects 
# NOTE CHANGE: Second attribue from hours to average_adventure_level
def createInstructorList(coachList):
	list = []
	for x in coachList:
			list.append(instructor.Instructor(x[0],x[1]))
	return list		


