from tkinter import *
from PIL import ImageTk, Image


root = Tk()
root.title("Station Generator")
root.iconbitmap('Dolphin.ico')
root.geometry("350x325")

logo = ImageTk.PhotoImage(Image.open("Little Kickers Logo.png"))
logo_label = Label(image=logo).grid(row=0,column=0,columnspan=3)

#Label For interface user options 
startLabel = Label(root, text="Pick an Option: ")
startLabel.grid(row=1,column=1)
def addInstructorSub(x):

# Open lists containing 
def openList(shift):
	shift_label = Label(root, text=shift.get()).grid(row=3,column=1)
	if shift == "Monday AM":
		subList_mondayAm = addInstructorSub(mondayAm)
	if shift == "Monday PM":
		subList_mondayPm = addInstructorSub(mondayPm)
	if shift == "Tuesday AM":
		subList_tuesdayAm = addInstructorSub(tuesdayAm)
	if shift == "Tuesday PM":
		subList_tuesdayPm = addInstructorSub(tuesdayPm)	
	if shift == "Wednesday AM":
		subList_wednesdayAm = addInstructorSub(wednesdayAm)
	if shift == "Wednesday PM":
		subList_wednesdayPm = addInstructorSub(wednesdayPm)
	if shift == "Thursday AM":
		subList_thursdayAm = addInstructorSub(thursdayAm)
	if shift == "Thursday PM":
		subList_thursdayPm = addInstructorSub(thursdayPm)
	if shift == "Friday AM":
		subList_fridayAm = addInstructorSub(fridayAm)
	if shift == "Friday PM":
		subList_fridayPm = subaddInstructorSub(fridayPm)
	if shift == "Saturday AM":
		subList_saturdayAm = addInstructorSub(saturdayAm)
	if shift == "Saturday PM":
		subList_saturdayPm = addInstructorSub(saturdayPm)
	if shift == "Sunday AM":
		subList_sundayAm = addInstructorSub(sundayAm)
	if shift == "Sunday PM":
		subList_sundayPm = addInstructorSub(sundayPm)

def pick_Shift():
	
	global subButton
	global displayButton
	global startLabel

	shift_Options = ["Monday AM","Tuesday AM","Wednesday AM","Thursday AM","Friday AM","Saturday AM","Sunday AM",\
				   "Monday PM","Tuesday PM","Wednesday PM","Thursday PM","Friday PM","Saturday PM","Sunday PM"]


	clicked = StringVar()
	clicked.set(shift_Options[0])
	
	#forget unused buttons of root
	startLabel.grid_forget()
	displayButton.grid_forget()
	subButton.grid_forget()
	pick_shift_label = Label(root, text="Pick the shift:")
	pick_shift_label.grid(row=1,column=1)
	drop = OptionMenu(root, clicked,*shift_Options)
	drop.grid(row=2,column=0)
	add_sub_button = Button(root,text="Continue",command=lambda: openList(clicked))
	add_sub_button.grid(row=2,column=1)

subButton = Button(root,text="Add Subs",command=pick_Shift)
subButton.grid(row=2,column=0)
displayButton = Button(root,text="Create Display")
displayButton.grid(row=2,column=1)
exit_Button = Button(root, text="Exit Program", command=root.quit)
exit_Button.grid(row=2,column=2)



root.mainloop()