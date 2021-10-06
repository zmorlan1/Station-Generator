# Author Zachary Morlan
# purpose to take Instructor data from Little kickers and 
# create a display for the front lobby
# Version macOS 

import numpy as np
import pandas
import instructor
import random as r 
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageFont, ImageDraw, ImageTk
from os import path

# NOT USED
# Take data frame of all employees and create list 
def createEmployeeList(df):
	emp_list = df["Name"].values.tolist()
	return emp_list

# NOT USED
# Cleans names for Employee list 
def cleanEmployeeList(list):
	for x in list:
		if '-' in x: 
			t = x.split('-')
			list[list.index(x)]=t[0]
		else:
			list[list.index(x)]=x
			
	return list

# Function that takes data from excel file and splits into lists 
# returns lists of instructers, and shifts for the whole week
def createDailyOperations():
	
	#global employee_list

	x = "Employee Schedule.xlsx"
	print("file name: " + x)
	print(path.exists(x))
	with open(x) as file:
		
		# NOTE: This Code is to create another list for a GUI drop down menu
		#employeeData = pandas.read_excel(x, skiprows = lambda x: x in [1], na_values=[''], usecols = "Q")
		#employee_list = createEmployeeList(employeeData)
		#employee_list = cleanEmployeeList(employee_list)
		
		data = pandas.read_excel(x, skiprows = 0, na_values=[''], usecols = "B:O")
		data.columns = data.columns.to_series().replace('Unnamed:\s\d+',np.nan,regex=True).ffill().values
		data = data.drop([19])
	sunday,monday,tuesday,wednesday,thursday,friday,saturday = createLists(data)
		
	monInstructors,\
	monDuration = splitLists(monday)
	tueInstructors,\
	tueDuration = splitLists(tuesday)
	wedInstructors,\
	wedDuration = splitLists(wednesday)
	thurInstructors,\
	thurDuration = splitLists(thursday)
	friInstructors,\
	friDuration = splitLists(friday)
	satInstructors,\
	satDuration = splitLists(saturday)
	sunInstructors,\
	sunDuration = splitLists(sunday)
	
	monInstructors,\
	monDuration = removeNulls(monInstructors,monDuration)
	tueInstructors,\
	tueDuration = removeNulls(tueInstructors,tueDuration)
	wedInstructors,\
	wedDuration = removeNulls(wedInstructors,wedDuration)
	thurInstructors,\
	thurDuration = removeNulls(thurInstructors,thurDuration)
	friInstructors,\
	friDuration = removeNulls(friInstructors,friDuration)
	satInstructors,\
	satDuration = removeNulls(satInstructors,satDuration)
	sunInstructors,\
	sunDuration = removeNulls(sunInstructors,sunDuration)

	mondayAm, mondayPm = splitByShift(monInstructors)
	monDurationAm, monDurationPm = splitByShift(monDuration)
	tuesdayAm, tuesdayPm = splitByShift(tueInstructors)
	tueDurationAm, tueDurationPm = splitByShift(tueDuration)
	wednesdayAm, wednesdayPm = splitByShift(wedInstructors)
	wedDurationAm, wedDurationPm = splitByShift(wedDuration)
	thursdayAm, thursdayPm = splitByShift(thurInstructors)
	thurDurationAm, thurDurationPm = splitByShift(thurDuration)
	fridayAm, fridayPm = splitByShift(friInstructors)
	friDurationAm, friDurationPm = splitByShift(friDuration)
	saturdayAm,saturdayPm = splitByShift(satInstructors)
	satDurationAm, satDurationPm = splitByShift(satDuration)
	sundayAm, sundayPm = splitByShift(sunInstructors)
	sunDurationAm, sunDurationPm = splitByShift(sunDuration)

	return mondayAm, mondayPm, monDurationPm, monDurationAm,\
		   tuesdayAm, tuesdayPm, tueDurationAm, tueDurationPm,\
		   wednesdayAm, wednesdayPm, wedDurationAm, wedDurationPm,\
		   thursdayAm, thursdayPm, thurDurationAm, thurDurationPm,\
		   fridayAm, fridayPm, friDurationAm, friDurationPm,\
		   saturdayAm, saturdayPm, satDurationAm, satDurationPm,\
		   sundayAm, sundayPm, sunDurationAm, satDurationPm 

# Removes null values from lists	
# NOTE CHANGE: duration will not be used but Average Adventure  levels
def removeNulls(instructors, duration):
	
	instructors = [x for x in instructors if pandas.isnull(x) == False]
	duration = [x for x in duration if pandas.isnull(x) == False]
	return instructors, duration

# Takes dataframe and splits into lists by day 
def createLists(df):
	sun = df["Sun AM"].values.tolist()
	mon = df["Mon AM"].values.tolist()
	tue = df["Tue AM"].values.tolist()
	wed = df["Wed AM"].values.tolist()
	thur = df["Thur AM"].values.tolist()
	fri = df["Fri AM"].values.tolist()
	sat = df["Sat AM"].values.tolist()
	return sun,mon,tue,wed,thur,fri,sat

# Splits each list value into instructors and duration
def splitLists(list):
	Instructors = [i[0] for i in list]
	Duration = [i[1] for i in list]
	return Instructors, Duration

# Splits list by AM and PM shift
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

# Prints instructor list for the shift
# NOTE NOT IN USE but could use for a view function of lists 
def printInstructors(list):
	
	global coaches
	coorX = 4
	coorY = 0
	for x in list:
		coaches = Label(root,text=x.get_name())
		coaches.grid(row=coorX,column=coorY)
		coorX+=1

# Looks for value in list matching user input
def checkValue(coach,list,sub):	 
	for x in list:
		if x.get_name() == coach: 
			index = list.index(x)
			list[index].add_sub(sub)
			return list.index(x)

# Saves all the names of employees into a list
def saveName(list):
	save_list = []
	i = 0
	for x in list:
		save_list.append(x.get_name())
		i+=1
	return save_list

# Function that allows for clearing unused widgets to create display
def displayOptions_loop():

	change_day_button.grid_forget()
	displayButton.grid_forget()
	displayOptions()

# Function that allows for clearing unused widgets for Changing day of the week
def shift_loop():

	global change_day_button

	change_day_button.grid_forget()
	user_Entry.grid_forget()
	pick_Shift()

def backButtonLoop(x):
	
	back_Button.grid_forget()
	if x == 1:
		pick_shift_label.grid_forget()
		drop.grid_forget()
		add_sub_button.grid_forget()
		home_Page()
	if x == 2: 
		shift_back_Button.grid_forget()
		sub_label.grid_forget()
		coach_list.grid_forget()
		pick_sub_button.grid_forget()
		pick_Shift()
	if x == 3:
		sub_label_2.grid_forget()
		user_Entry.grid_forget()
		coach_back_Button.grid_forget()
		openList(shift_clicked)
	if x == 4:
		sortLabel.grid_forget()
		back_Button.grid_forget()
		create_Display_button.grid_forget()
		sort_Options_Display.grid_forget()
		home_Page()

def home_Page():
	global subButton
	global displayButton
	global startLabel

	back_Button.grid_forget()
	
	#startLabel = Label(root, text="Pick an Option: ")
	startLabel.grid(row=1,column=1)

	subButton = Button(root,text="Add Subs",command=pick_Shift)
	subButton.grid(row=2,column=0)
	displayButton = Button(root,text="Create Display",command=displayOptions)
	displayButton.grid(row=2,column=1)
	
# Function to add sub entry into list
def addSub(coach,sub,list):
	
	global displayButton
	global change_day_button

	index = checkValue(coach,list,sub)
	createSublist(list,index)
	

	sub_label_2.grid_forget()
	sub = Label(root,text =sub +" is subbing for "+coach)
	sub.grid(row=1,column=0,columnspan=3)
	
	# NOTE: more drop down menu code
	#index = checkValue(coach,list,sub)
	#sub_list = createSublist(list,index)

	response = messagebox.askyesno("Add another sub?", "Add Another Sub?")
	if response == 1: 
		back_Button.grid_forget()
		coach_back_Button.grid_forget()
		shift_back_Button.grid_forget()
		user_Entry.grid_forget()
		sub.grid_forget()
		# NOTE: Drop down menu code
		#full_coach_list.destroy()
		add_sub_button.grid_forget()
		return addInstructorSub(list)
	else:
		back_Button.grid_forget()
		coach_back_Button.grid_forget()
		shift_back_Button.grid_forget()
		user_Entry.grid_forget()
		sub.grid_forget()
		#NOTE: Drop down menu code
		#full_coach_list.destroy()
		add_sub_button.grid_forget()
		change_day_button = Button(root,text="Change Day",command=shift_loop)
		change_day_button.grid(row=2,column=0)
		displayButton = Button(root,text="Create Display",command=displayOptions_loop)
		displayButton.grid(row=2,column=1)

# Changes widget from drop menu to entry
# NOTE: could also read in table from excel to include another drop down of all employees
def pickSub(x,list):
	
	global sub_label_2
	global user_Entry
	global add_sub_button
	global employee_list
	global coach_back_Button
	#NOTE: Drop down menu code
	#global full_coach_list

	shift_back_Button.grid_forget()
	coach_list.grid_forget()
	sub_label.grid_forget()
	pick_sub_button.grid_forget()
	sub_label_2 = Label(root,text="who is subbing for "+x.get())
	sub_label_2.grid(row=1,column=0,columnspan=3)

	#NOTE: Drop down menu code
	#clicked = StringVar()
	#clicked.set(employee_list[0])

	#NOTE: Drop down menu code
	#full_coach_list = OptionMenu(root,clicked,*employee_list)
	#full_coach_list.grid(row=2,column=0)
	user_Entry = Entry(root,width=10)
	user_Entry.grid(row=2,column=0)
	add_sub_button = Button(root,text="Continue",command=lambda: addSub(x.get(),user_Entry.get(),list))
	#NOTE: Drop down menu code
	#add_sub_button = Button(root,text="Continue",command=lambda: addSub(x.get(),clicked,list))
	add_sub_button.grid(row=2,column=1)

	#Back button for Coach list
	coach_back_Button = Button(root, text="Back",command=lambda: backButtonLoop(3))
	coach_back_Button.grid(row=3,column=1)

# Add the sub to the instructor object
def addInstructorSub(list):
	
	global sub_label
	global coach_list
	global pick_sub_button
	global shift_back_Button
	
	coach_names = saveName(list)
	clicked = StringVar()
	clicked.set(coach_names[0])

	sub_label = Label(root,text="Who is Out?")
	sub_label.grid(row=1,column=1)
	coach_list = OptionMenu(root,clicked,*coach_names)
	coach_list.grid(row=2,column=0)
	add_sub_button.grid_forget()
	pick_sub_button = Button(root,text="Continue",command=lambda: pickSub(clicked,list))
	pick_sub_button.grid(row=2,column=1)
	#Back Button to shift list
	shift_back_Button = Button(root, text="Back",command=lambda: backButtonLoop(2))
	shift_back_Button.grid(row=3,column=1)

# creates list with sub change
def createSublist(list, index):
	
	list[index].change_name()

# Open lists containing employees from shift
def openList(shift):
	
	# drop the drop down menu and label
	pick_shift_label.grid_forget()
	drop.grid_forget()


	if shift.get() == "Monday AM":
		subList_mondayAm = addInstructorSub(mondayAm)
	if shift.get() == "Monday PM":
		subList_mondayPm = addInstructorSub(mondayPm)
	if shift.get() == "Tuesday AM":
		subList_tuesdayAm = addInstructorSub(tuesdayAm)
	if shift.get() == "Tuesday PM":
		subList_tuesdayPm = addInstructorSub(tuesdayPm)	
	if shift.get() == "Wednesday AM":
		subList_wednesdayAm = addInstructorSub(wednesdayAm)
	if shift.get() == "Wednesday PM":
		subList_wednesdayPm = addInstructorSub(wednesdayPm)
	if shift.get() == "Thursday AM":
		subList_thursdayAm = addInstructorSub(thursdayAm)
	if shift.get() == "Thursday PM":
		subList_thursdayPm = addInstructorSub(thursdayPm)
	if shift.get() == "Friday AM":
		subList_fridayAm = addInstructorSub(fridayAm)
	if shift.get() == "Friday PM":
		subList_fridayPm = addInstructorSub(fridayPm)
	if shift.get() == "Saturday AM":
		subList_saturdayAm = addInstructorSub(saturdayAm)
	if shift.get() == "Saturday PM":
		subList_saturdayPm = addInstructorSub(saturdayPm)
	if shift.get() == "Sunday AM":
		subList_sundayAm = addInstructorSub(sundayAm)
	if shift.get() == "Sunday PM":
		subList_sundayPm = addInstructorSub(sundayPm)

# Function clears widgets and adds a drop menu and continue button
def pick_Shift():
	
	global subButton
	global displayButton
	#global startLabel
	global add_sub_button
	global pick_shift_label
	global drop
	global shift_clicked
	global back_Button

	shift_Options = ["Monday AM","Tuesday AM","Wednesday AM","Thursday AM","Friday AM","Saturday AM","Sunday AM",\
				   "Monday PM","Tuesday PM","Wednesday PM","Thursday PM","Friday PM","Saturday PM","Sunday PM"]

	shift_clicked = StringVar()
	shift_clicked.set(shift_Options[0])
	
	#forget unused buttons of root
	startLabel.grid_forget()
	displayButton.grid_forget()
	subButton.grid_forget()
	pick_shift_label = Label(root, text="Pick the shift:")
	pick_shift_label.grid(row=1,column=1)
	drop = OptionMenu(root, shift_clicked,*shift_Options)
	drop.grid(row=2,column=0)
	add_sub_button = Button(root,text="Continue",command=lambda: openList(shift_clicked))
	add_sub_button.grid(row=2,column=1)
	back_Button = Button(root, text="Back",command=lambda: backButtonLoop(1))
	back_Button.grid(row=3,column=1)

# Function that creates display for viewing gallery of instructor stations 
def createDisplays(button_click):
	
	display_font = ImageFont.truetype('Fira_Sans/FiraSans-Regular.ttf', 100)	
	display_text = ["Monday AM Instructor List","Monday PM Instructor List","Tuesday AM Instructor List",\
					"Tuesday PM Instructor List","Wednesday AM Instructor List","Wednesday PM Instructor List",\
					"Thursday AM Instructor List","Thursday PM Instructor List","Friday AM Instructor List",\
					"Friday PM Instructor List","Saturday AM Instructor List","Saturday PM Instructor List",\
					"Sunday AM Instructor List","Sunday PM Instructor List"]
	
	for x in display_text:
		display_image = Image.open("Instructor Stations.png")
		image_editable = ImageDraw.Draw(display_image)
		image_editable.text((350,250), x, (237, 230, 211), font=display_font)
		display_image.save('Station images/'+x+".png")
	for y in display_text:
		shift = listReturn(y)
		#print(shift[0].get_name())
		displayEmployeeLists(button_click,y,shift)
	back_Button.grid_forget()
	finish_Label = Label(root,text="Lobby Displays Created!")
	finish_Label.grid(row=3,column=0,columnspan=3)	

# Function that returns the instructor list for certain day
def listReturn(x):
	if x == "Monday AM Instructor List":return mondayAm	
	elif x == "Monday PM Instructor List":return mondayPm
	elif x == "Tuesday AM Instructor List":return tuesdayAm
	elif x == "Tuesday PM Instructor List":return tuesdayPm
	elif x == "Wednesday AM Instructor List":return wednesdayAm
	elif x == "Wednesday PM Instructor List":return wednesdayPm
	elif x == "Thursday AM Instructor List":return thursdayAm
	elif x == "Thursday PM Instructor List":return thursdayPm
	elif x == "Friday AM Instructor List":return fridayAm
	elif x == "Friday PM Instructor List":return fridayPm
	elif x == "Saturday AM Instructor List":return saturdayAm
	elif x == "Saturday PM Instructor List":return saturdayPm
	elif x == "Sunday AM Instructor List":return sundayAm
	elif x == "Sunday PM Instructor List":return sundayPm

# Function to change how Employee Lists are sorted 
# Can be alphabetically, by Adventure level, or Random
#NOTE could change alphabetically to by first name, last name, or reverse
def displayOptions():
	global sortLabel
	global back_Button
	global sort_Options_Display
	global create_Display_button

	displayButton.grid_forget()
	subButton.grid_forget()

	sortLabel = Label(root, text="Sort Alphabetically, by Adventure Level or Randomly")
	sortLabel.grid(row=1,column=0,columnspan=3)


	sort_Options = ["Alphabetically","Adventure Level","Random"]
	clicked = StringVar()
	clicked.set(sort_Options[0])

	sort_Options_Display = OptionMenu(root,clicked,*sort_Options) 
	sort_Options_Display.grid(row=2,column=0)
	create_Display_button = Button(root,text="Create Display",command = lambda:createDisplays(clicked))
	create_Display_button.grid(row=2,column=1)
	#back button to home
	back_Button = Button(root, text="Back",command=lambda: backButtonLoop(4))
	back_Button.grid(row=3,column=1)

# function that displays Employee lists on the pdf and saves new pdf files
# NOTES: VARIABLE NAME CHANGE to change code to reflect Average Adventure Level
def displayEmployeeLists(clicked,x,list):

	shift = list
	if clicked.get() == "Alphabetically":shift.sort(key=lambda x:x.name,reverse=False)
	# Change to Average Adventure level
	if clicked.get() == "Adventrure Level":shift.sort(key=lambda x:x.duration,reverse=False)
	if clicked.get() == "Random":r.shuffle(shift)
	display_font = ImageFont.truetype('Fira_Sans/FiraSans-Regular.ttf', 75)
	display_image = Image.open('Station images/'+x+".png")
	image_editable = ImageDraw.Draw(display_image)
	coorX = 400
	coorY = 500
	for y in shift:
		z = ""
		z = str(shift.index(y) + 1) + ".) " + str(y.get_name())
		if coorY >= 1325: 
			coorX = 1200
			coorY = 500
			image_editable.text((coorX,coorY), z , (237, 230, 211), font=display_font)
		else:
			image_editable.text((coorX,coorY), z, (237, 230, 211), font=display_font)
		coorY+=100
	display_image.save('Station images/'+x+".png")

mondayAm, mondayPm, monDurationPm, monDurationAm,\
tuesdayAm, tuesdayPm, tueDurationAm, tueDurationPm,\
wednesdayAm, wednesdayPm, wedDurationAm, wedDurationPm,\
thursdayAm, thursdayPm, thurDurationAm, thurDurationPm,\
fridayAm, fridayPm, friDurationAm, friDurationPm,\
saturdayAm, saturdayPm, satDurationAm, satDurationPm,\
sundayAm, sundayPm, sunDurationAm, sunDurationPm = createDailyOperations()

mondayAm = createInstructorList(mondayAm,monDurationAm)
mondayPm = createInstructorList(mondayPm,monDurationPm)
tuesdayAm = createInstructorList(tuesdayAm,tueDurationAm)
tuesdayPm = createInstructorList(tuesdayPm,tueDurationPm)
wednesdayAm = createInstructorList(wednesdayAm,wedDurationAm) 
wednesdayPm = createInstructorList(wednesdayPm,wedDurationPm)
thursdayAm = createInstructorList(thursdayAm,thurDurationAm)
thursdayPm = createInstructorList(thursdayPm,thurDurationPm)
fridayAm = createInstructorList(fridayAm,friDurationAm)
fridayPm = createInstructorList(fridayPm,friDurationPm)
saturdayAm = createInstructorList(saturdayAm,satDurationAm)
saturdayPm = createInstructorList(saturdayPm,satDurationPm)
sundayAm = createInstructorList(sundayAm,sunDurationAm)
sundayPm = createInstructorList(sundayPm,sunDurationPm)

root = Tk()
root.title("Station Generator")
#NOTE: Attempt to add an ico image to corner or program
#root.iconbitmap('Dolphin.ico')
root.geometry("380x380")


global displayButton
global startLabel

logo = ImageTk.PhotoImage(Image.open("Little Kickers Logo.png"))
logo_label = Label(image=logo).grid(row=0,column=0,columnspan=3)

#Label For interface user options 
startLabel = Label(root, text="Pick an Option: ")
startLabel.grid(row=1,column=1)

subButton = Button(root,text="Add Subs",command=pick_Shift)
subButton.grid(row=2,column=0)
displayButton = Button(root,text="Create Display",command=displayOptions)
displayButton.grid(row=2,column=1)
exit_Button = Button(root, text="Exit Program", command=root.quit)
exit_Button.grid(row=2,column=2)

root.mainloop()
