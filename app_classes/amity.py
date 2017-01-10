import sys
# sys.path.append('./app_classes')
from person import Staff, Fellow
from rooms import Office, Living_Space
import random

#Main class Amity
class Amity(object):
	
	def __init__(self):
		self.all_people = []
		self.all_rooms_office = []
		self.all_rooms_living = []
		self.available_living_space = []
		self.available_offices = []
	def func_office_available(self):
		for available_off in self.all_rooms_office:
			if(available_off.check_availability):
				self.available_offices.append(available_off)
			else:
				print('No available offices')
				return('No available offices')
				break
	def func_available_living_space(self):
		for available_liv in self.all_rooms_living:
			if(available_liv.check_availability):
				self.available_living_space.append(available_liv)
			else:
				print('No available living spaces')
				return 'No available living spaces'
				break
		
	def add_person(self, name, role, wants_accomodation):
		name = name
		role = role.upper()
		wants_accomodation = wants_accomodation
		person_exists = []
		available_offices = []
		available_living_space = []

		for p_exists in self.all_people:
					person_exists.append(p_exists.name)
		if name in person_exists:
			print('Another user exists with the same name')
			return 'Another user exists with the same name'
		else:
			if role == 'STAFF':
				if wants_accomodation == 'N':
					if len(self.all_rooms_office) == 0:
							print("Please create offices first.")
					else:
						self.func_office_available()
						random_office = random.choice(self.available_offices)
						self.add_person_office(name, role, wants_accomodation,random_office)
				elif wants_accomodation =='Y':
					print('No accomodation for staff')
					return 'No accomodation for staff'
				else:
					print('No such option. Use either Y or N')
					return 'No such option. Use either Y or N'
			elif role == 'FELLOW':
				if wants_accomodation == 'N':
					if len(self.all_rooms_office) == 0:
						print("Please create offices first.")
					else:
						self.func_office_available()
						random_office = random.choice(self.available_offices)
						self.add_person_office(name, role, wants_accomodation,random_office)
				elif wants_accomodation == 'Y':
					if len(self.all_rooms_office) == 0 or len(self.all_rooms_living) == 0:
						print("Please create offices and living_spaces first.")
					else:
						self.func_available_living_space()
						self.func_office_available()
						random_office = random.choice(self.available_offices)
						random_living_space = random.choice(self.available_living_space)
						self.add_person_office_wants_accomodation(name, role, wants_accomodation,random_office,random_living_space)
				else:
					print('No such option. Use either Y or N')
					return 'No such option. Use either Y or N'
				
			else:
				print('Your role is undefined')
				return('Your role is undefined')
	def add_person_office_wants_accomodation(self, name, role, wants_accomodation,random_office,random_living_space):
		fellow = Fellow(name,role,wants_accomodation)
		self.all_people.append(fellow)
		random_office.allocated_members.append(name)
		fellow.rooms_allocated.append(random_office.room_name)
		fellow.rooms_allocated.append(random_living_space.room_name)
		print(fellow.name)
		print(random_office.room_name)
		print(random_office.allocated_members)
		print(fellow.rooms_allocated)
							
	def add_person_office(self, name, role, wants_accomodation,random_office):
		if role == 'STAFF':
			staff = Staff(name,role,wants_accomodation)
			self.all_people.append(staff)
			random_office.allocated_members.append(name)
			staff.rooms_allocated.append(random_office.room_name)
			print(staff.name)
			print(random_office.room_name)
			print(random_office.allocated_members)
			print(staff.rooms_allocated)
		else:
			fellow = Fellow(name,role,wants_accomodation)
			self.all_people.append(fellow)
			random_office.allocated_members.append(name)
			fellow.rooms_allocated.append(random_office.room_name)
			print(fellow.name)
			print(random_office.room_name)
			print(random_office.allocated_members)
			print(fellow.rooms_allocated)
				
	#Fuction for creating rooms
	def  create_room(self, room_name):
		room_type = room_name[-1]
		room_type = room_type.upper()
		if room_type == 'OFFICE':
			room_name_list_office =[]
			room_name_list_office = room_name
			del room_name_list_office[-1]
			room_exists_list_office = []
			for i in self.all_rooms_office:
				room_exists_list_office.append(i.room_name)
			for i in room_name_list_office:
				if i in room_exists_list_office:
					return 'One of the rooms entered exits'
					break
				else:	
					office = Office(i,room_type)
					self.all_rooms_office.append(office)
			for room in self.all_rooms_office:
				print(room.room_name)
		elif room_type == 'LIVING_SPACE':
			room_name_list_living =[]
			room_name_list_living = room_name
			room_exists_list_living = []
			del room_name_list_living[-1]
			for i in self.all_rooms_living:
				room_exists_list_living.append(i.room_name)
			for i in room_name_list_living:
				if i in room_exists_list_living:
					return 'One of the rooms entered exits'
					break
				else:
					living = Living_Space(i,room_type)
					self.all_rooms_living.append(living)
			for room in self.all_rooms_living:
				print(room.room_name)
		else:
			print('You can only create OFFICE or a LIVING_SPACE')
	
	