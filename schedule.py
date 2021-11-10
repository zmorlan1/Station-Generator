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

	def add_day(self, week_day,data):

		new_Day = day(week_day,data)
		self.weekDays.update({len(self.weekDays)+1:new_Day})
		


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
		shifts["AM"] = list[1:i-1]
		shifts["PM"] = list[i+1:]
		return shifts
	

class shift(object):

	"""docstring for shift"""
	def __init__(self,time,employees):
		super(shift, self).__init__()
		self.time = time
		self.employees = createInstructorList(employees)

# Function that takes data from excel file and splits into lists 
# returns lists of instructers, and shifts for the whole week
# WORK NEEDED: Work on redusing repetition by creating a schedule object  
def createWeeklySchedule():
	
	global schedule
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
	for key in days_dict:
		days_dict[key] = createLists(data,days_dict[key])
		schedule.add_day(key,days_dict[key])
		print(key)

	for key in schedule.weekDays:
		schedule.weekDays[key].createShifts()
		for x in schedule.weekDays[key].shifts:
			print(schedule.weekDays[key].name)
			print(schedule.weekDays[key].shifts[x].time)
			for y in range(len(schedule.weekDays[key].shifts[x].employees)):
				print(schedule.weekDays[key].shifts[x].employees[y].name)

	return schedule

# Removes null values from lists	
# NOTE CHANGE: duration will not be used but Average Adventure  levels
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

createWeeklySchedule()
print(" ")
print(schedule.weekDays[2].shifts[1].employees[3].name)

