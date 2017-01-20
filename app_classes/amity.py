import sys
import os
from person import Staff, Fellow
from rooms import Office, Living_Space
from models import OfficeModel, PersonModel, LivingSpaceModel, create_db, Base
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, select

#Main class Amity
class Amity(object):

	def __init__(self):
		self.all_people = []
		self.all_rooms_office = []
		self.all_rooms_living = []
		self.available_living_space = []
		self.available_offices = []
		self.input_file = ''
		self.person_role = ''
		self.load_state()
	
	def clear_tables(self, session):
		meta = Base.metadata
		for table in reversed(meta.sorted_tables):
			session.execute(table.delete())
		session.commit()
	def print_room(self,room_name):
		room_found = False
		for office in self.all_rooms_office:
			if office.room_name == room_name:
				if len(office.allocated_members) != 0:
					all_members = ', '.join(office.allocated_members)
					room_found = True
					print(all_members)
					break
				else:
					print('No members allocated to that room.')
					room_found = True
			else:
				for living in self.all_rooms_living:
					if living.room_name == room_name:
						if len(living.all_members) != 0:
							all_members = ', '.join(living.allocated_members)
							room_found = True
							print(all_members)
							break
						else:
							print('No members allocated to that room.')
							room_found = True

		if room_found == False:
			print('Room was not found')


	def print_allocations(self, filename):
		output = ''
		print('---------------------------------------')
		output += '---------------------------------------\n'
		print('OFFICE ALLOCATIONS')
		output += 'OFFICE ALLOCATIONS\n'
		print('---------------------------------------')
		output += '---------------------------------------\n'

		all_members = ''
		for office in self.all_rooms_office:

			room_name = office.room_name
			output += (room_name + '\n')
			print(room_name)
			print('---------------------------------------')
			output += '---------------------------------------\n'
			all_members = ', '.join(office.allocated_members)
			print(all_members)
			output += (all_members + '\n')
			print('\n')
			output +='\n'
		print('---------------------------------------')
		output += '---------------------------------------\n'
		print('LIVING SPACE ALLOCATIONS')
		output += 'LIVING SPACE ALLOCATIONS\n'
		print('---------------------------------------')
		output += '---------------------------------------\n'
		all_members = ''
		for living in self.all_rooms_living:
			room_name = living.room_name
			print(room_name)
			output +=room_name
			print('---------------------------------------')
			output += '---------------------------------------\n'
			all_members = ', '.join(living.allocated_members)
			print(all_members)
			output += (all_members + '\n')
			print('\n')
		if filename is  None:
			pass
		else:
			directory = 'files/'
			files = open(directory + filename + ".txt", "w")
			files.write(output)
			files.close()

	def print_unallocated(self, filename):
		output = ''
		print('---------------------------------------')
		output += '---------------------------------------\n'
		print('UNALLOCATED MEMBERS')
		output += 'UNALLOCATED MEMBERS\n'
		print('---------------------------------------')
		output += '---------------------------------------\n'
		for person in self.all_people:
			if person.office_allocated == None and person.living_space_allocated == None:
				name = person.name
				role = person.role
				wants_accomodation = person.wants_accomodation
				print(name + ' ' + role + ' ' + wants_accomodation)
				output += (name + ' ' + role + ' ' + wants_accomodation + '\n')
			else:
				print('It seems that everybody has a room.')
				output += 'It seems that everybody has a room.\n'
		if filename is None:
			pass
		else:
			directory = 'files/' 
			files = open(directory + filename + ".txt", "w")
			files.write(output)
			files.close()

	def save_state(self, db_name):
		'''Persists data added during a sesion to a database file. Amity by default if none is given'''
		engine = create_db(db_name)
		Base.metadata.bind = engine
		Session = sessionmaker()
		session = Session()
		self.clear_tables(session)
		for office in self.all_rooms_office:
			allocated_members_string = ''
			room_name = office.room_name
			allocated_members = office.allocated_members
			for member in allocated_members:
				member = ',' + member
				allocated_members_string += member
			room_type = office.room_type
			capacity = office.capacity
			office_record = OfficeModel(room_name = room_name, allocated_members = allocated_members_string,
						 room_type = room_type, capacity = capacity)
			session.add(office_record)
			session.commit()
		for living in self.all_rooms_living:
			allocated_members_string = ''
			room_name = living.room_name
			allocated_members = living.allocated_members
			for member in allocated_members:
				member = ',' + member
				allocated_members_string += member
			room_type = living.room_type
			capacity = living.capacity
			living_record = LivingSpaceModel(room_name = room_name, allocated_members = allocated_members_string,
						 room_type = room_type, capacity = capacity)
			session.add(living_record)
			session.commit()
		for person in self.all_people:
			name = person.name
			role = person.role
			wants_accomodation = person.wants_accomodation
			office_allocated = person.office_allocated
			living_space_allocated = person.living_space_allocated
			person_record = PersonModel(name = name, role = role, wants_accomodation = wants_accomodation,
										office_allocated = office_allocated,
										living_space_allocated = living_space_allocated)
			session.add(person_record)
			session.commit()
	def load_state(self, db_name='amity'):
		'''Persists data added during a sesion to a database file. Amity by default if none is given'''
		engine = create_db(db_name)
		Base.metadata.bind = engine
		Session = sessionmaker()
		session = Session()
		del self.all_rooms_office[:]
		del self.all_rooms_living[:]
		del self.all_people[:]
		for office in session.query(OfficeModel):
			office_allocated_members_string = ''
			room_name = office.room_name
			office_allocated_members_string = office.allocated_members
			allocated_members = office_allocated_members_string.split(',')
			del allocated_members[0]
			room_type = office.room_type
			capacity = office.capacity
			office = Office(room_name,room_type)
			office.allocated_members = allocated_members
			office.capacity = capacity
			self.all_rooms_office.append(office)
		for living in session.query(LivingSpaceModel):
			living_allocated_members_string = ''
			room_name = living.room_name
			living_allocated_members_string = living.allocated_members
			allocated_members = living_allocated_members_string.split(',')
			del allocated_members[0]
			room_type = living.room_type
			capacity = living.capacity
			living =  Living_Space(room_name,room_type)
			living.allocated_members = allocated_members
			living.capacity = capacity
			self.all_rooms_living.append(living)
		for person in session.query(PersonModel):
			self.all_people.append(person)
	
	def check_if_person_name_is_valid(self,person_identifier,new_room):
		name_found = False
		for person in self.all_people:
			if person_identifier == person.name:
				self.person_role =person.role
				name_found = True	
				break
			else:
				name_found = False
		if name_found:
			return True
		else:
			print('Your name has not been found in system')
			return False

	def check_if_office_name_is_valid(self,room):
		self.func_office_available()
		room_found = False
		for office in self.available_offices:
			office = office.room_name
			if room == office:
				room_found = True
				break
			else:
				room_found = False
		if room_found:
			return True
		return False

	def check_if_living_space_name_is_valid(self,room):
		self.func_available_living_space()
		room_found = False
		for living in self.available_living_space:
			living = living.room_name
			if room == living:
				room_found = True
				break
			else:
				room_found = False
		if room_found:
			return True
		return False

		# for living in self.available_living_space:
		# 	if new_room == living.room_name:
		# 		return True
		# 	else:
		# 		return False
	def remove_person_from_initial_office(self, person_identifier, current_office):
		room_found = False
		for office in self.all_rooms_office:
			if current_office == office.room_name:
				office.allocated_members.remove(person_identifier)
				room_found = True
				break
			else:
				room_found = False
		if room_found:
			return True
		else:
			return False

	def remove_person_from_initial_living_space(self, person_identifier, current_living_space):
		room_found = False
		for living in self.all_rooms_living:
			if current_living_space == living.room_name:
				living.allocated_members.remove(person_identifier)
				room_found = True
				break
			else:
				room_found = False
		if room_found:
			return True
		else:
			return False

	def swap_living_space_members(self,person_identifier,new_room,current_living_space):
		self.func_available_living_space
		room_found = False
		for living in self.available_living_space:
			if new_room == living.room_name:
				living.allocated_members.append(person_identifier)
				self.remove_person_from_initial_living_space(person_identifier,current_living_space)
				room_found = True
				break
			else:
				room_found = False
		if room_found:
			return True
		else:
			return False

	def swap_office_members(self,person_identifier,new_room,current_office):
		self.func_office_available()
		room_found = False
		for office in self.available_offices:
			if new_room == office.room_name:
				office.allocated_members.append(person_identifier)
				self.remove_person_from_initial_office(person_identifier,current_office)
				room_found = True
				break
			else:
				room_found = False
		if room_found:
			return True
		else:
			return False

			
	def reallocate_person(self,person_identifier,new_room):
		person_identifier = person_identifier
		new_room = new_room
		self.check_if_person_name_is_valid(person_identifier,new_room)
		if self.person_role == 'STAFF':
			if(self.check_if_office_name_is_valid(new_room)):
				for person in self.all_people:
					if person_identifier == person.name:
						current_office = person.office_allocated
						break
				if self.swap_office_members(person_identifier,new_room,current_office):
					print('You have been reallocated successfully')
				else:
					print('Oops!Reallocation has failed.')
			else:
				print('The room entered is not a valid room.')
		elif self.person_role == 'FELLOW':
			if(self.check_if_office_name_is_valid(new_room)):
				for person in self.all_people:
					if person_identifier == person.name:
						current_office = person.office_allocated
						break
				if self.swap_office_members(person_identifier,new_room,current_office):
					print('You have been reallocated successfully')
				else:
					print('Oops!Reallocation has failed.')
			elif(self.check_if_living_space_name_is_valid(new_room)):
				#code
				for person in self.all_people:
					if person_identifier == person.name:
						current_living_space = person.living_space_allocated
						break
				if self.swap_living_space_members(person_identifier,new_room,current_living_space):
					print('You have been reallocated successfully')
				else:
					print('Oops!Reallocation has failed.')

			else:
				print('The room entered is not a valid room.')
		else:
			print('System was unable to identify your role.')

	def load_people(self,file_path):
		try:
			self.input_file = file_path
			if not os.path.isfile(self.input_file):
				print("Invalid filepath.")
				return "Invalid filepath."
			with open(self.input_file) as people_file:
				people = people_file.readlines()
				if len(people) == 0:
					print('The file has no contents')
					return 'The file has no contents'
				else:
					for line in people:
						line = line.replace('\n','')
						person = line.split(' ')
						if len(person) < 4:
							wants_accomodation = 'N'
							name = person[0] + " " + person[1]
							role = person[2]
							self.add_person(name, role, wants_accomodation)
						else:
							wants_accomodation = person[3]
							name = person[0] + " " + person[1]
							role = person[2]
							self.add_person(name, role, wants_accomodation)

		except Exception as e:
			print ('Oops! The system failed to read the file')
			return 'Oops! The system failed to read the file'

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
		wants_accomodation = wants_accomodation.upper()
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
						return "Please create offices first."
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
						return "Please create offices and living_spaces first."
					else:
						if len(self.available_offices) == 0:
							if len(self.available_living_space) == 0:
								self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
								print('You have been added to the system but no Office or Living Space was allocated.')
							else:
								random_living_space = random.choice(self.available_living_space)
								self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
								print('You have been added to the system. You were allocated a Living space only.')
						else:
							random_office = random.choice(self.available_offices)
							if len(self.available_living_space) == 0:
								self.add_person_all_people(name, role, wants_accomodation,random_office,random_living_space)
								print('You have been allocated a Office successfully. Living space is still unavailable')
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
				print(staff.office_allocated)

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
			for office in self.all_rooms_office:
				room_exists_list_office.append(office.room_name)
			for office in room_name_list_office:
				if office in room_exists_list_office:
					print('One of the rooms entered exits')
					return 'One of the rooms entered exits'
					break
				else:
					office = Office(office,room_type)
					self.all_rooms_office.append(office)
			for room in self.all_rooms_office:
				print(room.room_name)
		elif room_type == 'LIVING_SPACE':
			room_name_list_living =[]
			room_name_list_living = room_name
			room_exists_list_living = []
			del room_name_list_living[-1]
			for room in self.all_rooms_living:
				room_exists_list_living.append(room.room_name)
			for room in room_name_list_living:
				if room in room_exists_list_living:
					print('One of the rooms entered exits')
					return 'One of the rooms entered exits'
					break
				else:
					living = Living_Space(room,room_type)
					self.all_rooms_living.append(living)
			for room in self.all_rooms_living:
				print(room.room_name)
		else:
			print('You can only create OFFICE or a LIVING_SPACE')
			return 'You can only create OFFICE or a LIVING_SPACE'
