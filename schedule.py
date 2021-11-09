# Author Zach Morlan
# Creates Object to store weekly  employee schedule
import instructor
import numpy as np
import pandas
import instructor
import random as r 
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageFont, ImageDraw, ImageTk
from os import path


class Schedule(object):

	timeframe = "Weekly"
	"""docstring for Schedule"""
	def __init__(self, data):
		super(Schedule, self).__init__()
		self.schedule = data
		self.weekDays = {}

	def add_day(self, week_day ):

		new_Day = day(week_day)
		self.weekDays.update({len(self.weekDays)+1:new_Day})
		


class day(object):

	"""docstring for day"""
	def __init__(self, name):
		super(day, self).__init__()
				
		self.name = name
		self.shifts = {}
			
	def add_Shift (self,time,employees):

		new_shift = shift(time,employees)
		self.shifts.update({len(self.shifts)+1:new_shift})
		

class shift(object):

	"""docstring for shift"""
	def __init__(self,time,employees):
		super(shift, self).__init__()
		self.time = time
		self.employees = employees		

# Function that takes data from excel file and splits into lists 
# returns lists of instructers, and shifts for the whole week
# WORK NEEDED: Work on redusing repetition by creating a schedule object  
def createDailyOperations():
	
	#global employee_list

	days_dict = {"monday":"Mon AM","tuesday":"Tue AM", "wednesday":"Wed AM", "thursday":"Thur AM",\
				 "friday":"Fri AM", "saturday":"Sat AM","sunday":"Sun AM"}
	x = "Employee Schedule.xlsx"
	print("file name: " + x)
	print(path.exists(x))
	with open(x) as file:
		
		data = pandas.read_excel(x, skiprows = 0, na_values=[''], usecols = "B:O")
		data.columns = data.columns.to_series().replace('Unnamed:\s\d+',np.nan,regex=True).ffill().values
		data = data.drop([19])

	schedule = Schedule(data)
	# Minimize items created
	# This splits the data frame into 7 lists 
	monday = createLists(data,days_dict['monday'])
	for key in days_dict:
		schedule.add_day(key)
		days_dict[key] = createLists(data,days_dict[key])
		print(key)
		print(days_dict[key])

	for key in schedule.weekDays:
		print(schedule.weekDays[key].name)
	# This splits list into Instructor and Duration for each day
	#monInstructors,\
	#monDuration = splitLists(monday)

	
	# Removes all nulls from each list
	#monInstructors,\
	#monDuration = removeNulls(monInstructors,monDuration)


	#mondayAm, mondayPm = splitByShift(monInstructors)
	#monDurationAm, monDurationPm = splitByShift(monDuration)

	return print("titties...Um I mean Success!")
	#return mondayAm, mondayPm, monDurationPm, monDurationAm,\

# Removes null values from lists	
# NOTE CHANGE: duration will not be used but Average Adventure  levels
# NOTE: Maybe after clearing nulls combine lists
def removeNulls(list_A, list_B):
	
	list_A = [x for x in list_A if pandas.isnull(x) == False]
	list_B = [x for x in list_B if pandas.isnull(x) == False]
	results = list(zip(list_A,list_B))
	return  splitByShift(results)

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

# Splits list by AM and PM shift
# NOTE: Code could be added to schedule object
# NOTE: incase I forget maybe instead of splitting maybe
# 		just writing code to clear duration and coaches from list
# NOTE: Create new function that takes the split shifts and adds 
#		them to the day object with add_shifts
def splitByShift(list):
	count = 0
	i = 0
	am_list = []
	pm_list = []
	for x in list:
		if x == "Duration" or x == "Coaches":
			count+=1	
		elif count == 2:
			break
		else:
			i+=1
	i+=1		
	am_list = list[1:i]
	pm_list = list[i+1:]
	return am_list,pm_list

# Creates a list of instructor objects 
# NOTE CHANGE: Second attribue from hours to average_adventure_level
def createInstructorList(shift,hours):
	list = []
	for x, y in zip(shift,hours):
			list.append(instructor.Instructor(x,y))
	return list		


days_dict = {1:"monday",2:"tuesday", 3:"wednesday", 4:"thursday", 5:"friday", 6:"saturday",7:"sunday"}
#mondayAm, mondayPm, monDurationPm, monDurationAm = createDailyOperations()
createDailyOperations()
#mondayTest = createInstructorList(mondayAm,monDurationAm)

#monday = day("Monday")
#monday.add_Shift('AM',mondayTest)
#print(monday.shift.employees[0].name)
