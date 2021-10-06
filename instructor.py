# Author Zachary Morlan
# create the instructor object
#import dailyOperations 

class Instructor(object):

	global sub
	"""docstring for instructors"""
	def __init__(self, name, hours):
	
		self.name = name
		self.hours = hours
		self.sub = ""

	def get_name(self):
		return self.name

	def change_name(self):
		try:
			x = self.name
			self.name = self.sub
			self.sub = x
		except Exception as e:print("something went wrong,\
									 check spelling or for sub")		
			
	def get_hours(self):
		return self.hours 

	def add_sub(self,x):
		
			self.sub = x
		

	def get_sub(self):
		return self.sub

	def del_sub(self):
		del self.sub 
		return print("success")



