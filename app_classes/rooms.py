#Main class model for Rooms entity
class Rooms(object):

	def __init__(self,room_name,room_type):
		self.room_name = room_name
		self.allocated_members = []
		self.room_type = room_type
#Class living_space inherits from Rooms
class Living_Space(Rooms):
	def __init__(self, room_name,room_type):
		Rooms.__init__(self,room_name,room_type)
		self.capacity = 4
	def check_availability(self):
		if len(self.allocated_members) < 2:
			return True
		else:
			return False
			
#Class living_space inherits from Rooms
class Office(Rooms):
	def __init__(self, room_name,room_type):
		Rooms.__init__(self,room_name,room_type)
		self.capacity = 6
	def check_availability(self):
		if len(self.allocated_members) < 2:
			return True
		else:
			return False