import sys
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
		self.input_file = 'files/people.txt'

	def load_state(self):
		try:
			with open(self.input_file) as people_file:
				people = people_file.readlines()
				if len(people) == 0:
					print('The file has no contents')
				else:
					for line in people:
						line.replace(r'\n',' ')
						person = line.split(' ')
						if len(person) < 4:
							wants_accomodation = 'N'
							name = person[0] + " " + person[1]
							role = 'STAFF'
							self.add_person(name, role, wants_accomodation)
						else:
							wants_accomodation = 'Y'
							name = person[0] + " " + person[1]
							role = 'FELLOW'
							self.add_person(name, role, wants_accomodation)
							
		except Exception as e:
			e = str(e)
			print ('Oops! The system failed to read the file' + e)
							
	def func_office_available(self):
		del self.available_offices[:]
		for available_off in self.all_rooms_office:
			if(available_off.check_availability()):
				self.available_offices.append(available_off)
				

	def func_available_living_space(self):
		del self.available_living_space[:]
		for available_liv in self.all_rooms_living:
			if(available_liv.check_availability()):
				self.available_living_space.append(available_liv)
				
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
			random_office = None
			random_living_space = None
			self.func_office_available()
			self.func_available_living_space()
			if role == 'STAFF':
				if wants_accomodation == 'N':
					if len(self.all_rooms_office) == 0:
							print("Please create offices first.")
					else:
						if len(self.available_offices) == 0:
							self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
							print('You have been added to the system but no Office or Living Space was allocated.')	
						else:
							random_office = random.choice(self.available_offices)
							self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
							print('You have been allocated a Office successfully.')
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
						if len(self.available_offices) == 0:
							self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
							print('You have been added to the system but no Office or Living Space was allocated.')
						else:
							random_office = random.choice(self.available_offices)
							self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
							print('You have been allocated a Office successfully.')
				elif wants_accomodation == 'Y':
					if len(self.all_rooms_office) == 0 or len(self.all_rooms_living) == 0:
						print("Please create offices and living_spaces first.")
					else:
						if len(self.available_offices) == 0:
							if len(self.available_living_space) == 0:
								self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
								print('You have been added to the system but no Office or Living Space was allocated.')
							else:
								random_living_space = random.choice(self.available_living_space)
								self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
								print('You have been added to the system. You were only booked for accomodation.')
						else:
							random_office = random.choice(self.available_offices)
							if len(self.available_living_space) == 0:
								self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
								print('You have been allocated a Office successfully. Accomodation is still unavailable')
							else:
								random_living_space = random.choice(self.available_living_space)
								self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
								print('You have been allocated a Office and a Living Space successfully')
				else:
					print('No such option. Use either Y or N')
					return 'No such option. Use either Y or N'
				
			else:
				print('Your role is undefined')
				return('Your role is undefined')
						
	def add_person_all_people(self, name, role, wants_accomodation,random_office,random_living_space):
		if role == 'STAFF':
			staff = Staff(name,role,wants_accomodation)
			self.all_people.append(staff)
			staff.living_space_allocated = None
			if random_office == None:
				staff.office_allocated = None
			else:
				random_office.allocated_members.append(name)
				staff.office_allocated = random_office.room_name
		
		else:
			fellow = Fellow(name,role,wants_accomodation)
			self.all_people.append(fellow)
			if random_office == None:
				if random_living_space == None:
					fellow.office_allocated = None
					fellow.living_space_allocated = None
				else:
					fellow.living_space_allocated = random_living_space.room_name
					random_living_space.allocated_members.append(name)
			else:
				if random_living_space == None:
					random_office.allocated_members.append(name)
					fellow.office_allocated = random_office.room_name
					fellow.living_space_allocated = None
				else:
					random_office.allocated_members.append(name)
					random_living_space.allocated_members.append(name)
					fellow.living_space_allocated = random_living_space.room_name
					fellow.office_allocated = random_office.room_name
						
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
	
	