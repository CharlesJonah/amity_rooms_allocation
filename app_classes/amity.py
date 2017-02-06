import sys
import os
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, select
from termcolor import cprint, colored
from firebase import firebase
from time import sleep
from tqdm import tqdm
import json
import sqlite3

from person import Staff, Fellow
from rooms import Office, Living_Space
from models import OfficeModel, PersonModel, LivingSpaceModel, create_db, Base

class Amity(object):
	""" Class that holds all the application functionality and all the
	data structures that persist information to be saved in the database"""

	def __init__(self):
		self.all_people = [] # This list holds all the people objects
		self.all_rooms_office = [] #This list holds all the office room object
		self.all_rooms_living = [] #This list holds all the living space objects
		self.available_living_space = [] #This list holds all the available living space objects
		self.available_offices = [] #This list holds all the available office objects
		self.input_file = '' #This variable holds the load_people file path
		self.person_role = '' #This variable holds a persons role. e.g STAFF or FELLOW
		self.load_state()  # initializes the application with data from the database

	def clear_tables(self, session):
		""" Clears the information in database tables before populating the database
			again """
		meta = Base.metadata
		for table in reversed(meta.sorted_tables):
			session.execute(table.delete())
		session.commit()
	def sync(self):
		""" Syncs with firebase online database"""
		try:
			con = sqlite3.connect('databases/amity')
			cur = con.cursor()
			#Uploads the person table data to firebase
			cur.execute("SELECT * FROM person")
			person_data = cur.fetchall()
			fibase = firebase.FirebaseApplication('https://amity-fb5f5.firebaseio.com/')
			upload_person = fibase.post('/', json.dumps(person_data))
			#Uploads the living_space table data to firebase
			cur.execute("SELECT * FROM living_space")
			living_space_data = cur.fetchall()
			fibase = firebase.FirebaseApplication('https://amity-fb5f5.firebaseio.com/')
			upload_living_space = fibase.post('/', json.dumps(living_space_data))
			#Uploads the offices table data to firebase
			cur.execute("SELECT * FROM offices")
			office_data = cur.fetchall()
			fibase = firebase.FirebaseApplication('https://amity-fb5f5.firebaseio.com/')
			upload_office = fibase.post('/', json.dumps(office_data))
			for i in tqdm(range(200)):
				sleep(0.01)
			cprint ('*** Done! ***','cyan', attrs=['bold'])
		except Exception as e:
			print(e)

	def update_database(self):
		""" Updates local database with data from firebase online database"""
		try:

			fibase = firebase.FirebaseApplication('https://amity-fb5f5.firebaseio.com/')
			upload_person = fibase.get('/')
			for i in tqdm(range(200)):
				sleep(0.01)
			cprint ('*** Done! ***','cyan', attrs=['bold'])
			print(upload_person)
		except Exception as e:
			print(e)

	def print_room(self,room_name):
		""" This function prints a room with all its allocated members"""
		room_found = False
		for office in self.all_rooms_office:
			if office.room_name == room_name:
				if len(office.allocated_members) != 0:
					cprint('---------------------------------------','cyan', attrs=['bold'])
					cprint('ALLOCATED MEMBERS','yellow', attrs=['bold'])
					cprint('---------------------------------------','cyan', attrs=['bold'])
					room_found = True
					for person in office.allocated_members:
						cprint(person,'yellow', attrs=['bold'])
					break
				else:
					cprint('No members allocated to that room.','red', attrs=['bold'])
					room_found = True
		if room_found == False:
			for living in self.all_rooms_living:
				if living.room_name == room_name:
					if len(living.allocated_members) != 0:
						cprint('---------------------------------------','cyan', attrs=['bold'])
						cprint('ALLOCATED MEMBERS','yellow', attrs=['bold'])
						cprint('---------------------------------------','cyan', attrs=['bold'])
						room_found = True
						for person in living.allocated_members:
							cprint(person,'yellow', attrs=['bold'])
						break
					else:
						cprint('No members allocated to that room.','red', attrs=['bold'])
						room_found = True

		if room_found == False:
			cprint('Room was not found','red', attrs=['bold'])
			return 'Room was not found'


	def print_allocations(self, filename):
		""" This function prints the respective room allocations. This shows the association
			of room members  to their rooms"""
		if filename != None:
			for char in filename:
				if char in "\/:*?<>|":
					cprint('File name contains unwanted characters','red', attrs=['bold'])
					return False
		output = ''
		cprint('---------------------------------------','cyan', attrs=['bold'])
		output += '---------------------------------------\n'
		cprint('OFFICE ALLOCATIONS','yellow', attrs=['bold'])
		output += 'OFFICE ALLOCATIONS\n'
		cprint('---------------------------------------','cyan', attrs=['bold'])
		output += '---------------------------------------\n'

		all_members = ''
		if len(self.all_rooms_office) > 0:
			for office in self.all_rooms_office:

				room_name = office.room_name
				output += (room_name + '\n')
				cprint(room_name,'yellow', attrs=['bold'])
				cprint('---------------------------------------','cyan', attrs=['bold'])
				output += '---------------------------------------\n'
				for person in office.allocated_members:
					cprint(person,'yellow', attrs=['bold'])
					output += (person + '\n')
				print('\n')
				output +='\n'
		else:
			cprint('No offices in the system','red', attrs=['bold'])
			return 'No offices in the system'
			output += 'No offices in the system\n'
		cprint('---------------------------------------','cyan', attrs=['bold'])
		output += '---------------------------------------\n'
		cprint('LIVING SPACE ALLOCATIONS','yellow', attrs=['bold'])
		output += 'LIVING SPACE ALLOCATIONS\n'
		cprint('---------------------------------------','cyan', attrs=['bold'])
		output += '---------------------------------------\n'
		all_members = ''
		if len(self.all_rooms_living):
			for living in self.all_rooms_living:
				room_name = living.room_name
				cprint(room_name,'yellow', attrs=['bold'])
				output +=room_name
				cprint('---------------------------------------','cyan', attrs=['bold'])
				output += '---------------------------------------\n'
				for person in living.allocated_members:
					cprint(person,'yellow', attrs=['bold'])
					output += (person + '\n')
				print('\n')
		else:
			cprint('No living spaces in the system','red', attrs=['bold'])
			return 'No living spaces in the system'
			output += 'No living spaces in the system\n'

		if filename is  None:
			pass
		else:
			directory = 'files/'
			files = open(directory + filename + ".txt", "w")
			files.write(output)
			files.close()

	def print_unallocated(self, filename):
		""" This function lists all people registered in the system that have not
			been allocated a room"""
		if filename != None:
			for char in filename:
				if char in "\/:*?<>|":
					cprint('File name contains unwanted characters','red', attrs=['bold'])
					return False
		output = ''
		cprint('---------------------------------------','cyan', attrs=['bold'])
		output += '---------------------------------------\n'
		cprint('UNALLOCATED MEMBERS','yellow', attrs=['bold'])
		output += 'UNALLOCATED MEMBERS\n'
		cprint('---------------------------------------','cyan', attrs=['bold'])
		output += '---------------------------------------\n'
		people_found = 0
		if len(self.all_people) > 0:
			for person in self.all_people:
				if person.office_allocated == None and person.living_space_allocated == None:
					people_found += 1
					name = person.name
					role = person.role
					wants_accomodation = person.wants_accomodation
					cprint(name + ' ' + role + ' ' + wants_accomodation, 'yellow', attrs=['bold'])
					output += (name + ' ' + role + ' ' + wants_accomodation + '\n')
			if people_found == 0:
				cprint('It seems that everybody has a room','yellow', attrs=['bold'])
		else:
			cprint('No people found in the system','red', attrs=['bold'])
			return 'No people found in the system'
		if filename is None:
			pass
		else:
			directory = 'files/'
			files = open(directory + filename + ".txt", "w")
			files.write(output)
			files.close()

	def save_state(self, db_name):
		"""Persists data added during a sesion to a database file."""
		for char in db_name:
			if char in "\/:*?<>|":
				cprint('Database name contains unwanted characters', 'red', attrs=['bold'])
				return False
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
			office_record = OfficeModel(room_name = room_name, \
			allocated_members = allocated_members_string,
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
			living_record = LivingSpaceModel(room_name = room_name, \
			allocated_members = allocated_members_string,
						room_type = room_type, capacity = capacity)
			session.add(living_record)
			session.commit()
		for person in self.all_people:
			name = person.name
			role = person.role
			wants_accomodation = person.wants_accomodation
			office_allocated = person.office_allocated
			living_space_allocated = person.living_space_allocated
			person_record = PersonModel(name = name, role = role, \
			wants_accomodation = wants_accomodation,
			office_allocated = office_allocated,
			living_space_allocated = living_space_allocated)
			session.add(person_record)
			session.commit()
		cprint('Your data has been saved successfully','cyan', attrs=['bold'])

	def load_state(self, db_name='amity'):
		"""Loads data to the system from a database file. amity by default if is given"""
		for char in db_name:
			if char in "\/:*?<>|":
				cprint('Database name contains unwanted characters', 'red', attrs=['bold'])
				return False
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
		cprint('SYSTEM HAS LOADED SUCCESSFULLY!', 'cyan', attrs=['bold'])

	def check_if_person_name_is_valid(self,person_identifier,new_room):
		""" This function checks if a persons name is valid before reallocating him when doing
			room reallocation"""
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
		""" This function checks if the an office exists and 
		if it is available for realocation"""
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
		""" This function checks if the a living space 
		exists and if it is available for realocation"""
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

	def remove_person_from_initial_office(self, person_identifier, current_office):
		""" This function removes a person from his or her 
		current office before reallocating him or her"""
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
		""" This function removes a person from his or her current 
		living space before reallocating him or her """
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
		""" This function swaps a person from his current 
		living space to the new living space """
		self.func_available_living_space
		room_found = False
		for living in self.available_living_space:
			if new_room == living.room_name:
				living.allocated_members.append(person_identifier)
				self.remove_person_from_initial_living_space \
				(person_identifier,current_living_space)
				room_found = True
				break
			else:
				room_found = False
		if room_found:
			return True
		else:
			return False

	def swap_office_members(self,person_identifier,new_room,current_office):
		""" This function swaps a person from his current office to a new office """
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


	def reallocate_person(self,first_name,last_name,new_room):
		""" This function is the core function that carries out the process of reallocation.
			The function controls the reallocation process and calls all the associated functions """
		person_identifier = first_name + ' ' + last_name
		new_room = new_room
		self.check_if_person_name_is_valid(person_identifier,new_room)
		if self.person_role == 'STAFF':
			if(self.check_if_office_name_is_valid(new_room)):
				for person in self.all_people:
					if person_identifier == person.name:
						current_office = person.office_allocated
						break
				if self.swap_office_members(person_identifier,new_room,current_office):
					cprint('You have been reallocated successfully','cyan', attrs=['bold'])
				else:
					cprint('Oops!Reallocation has failed.','red', attrs=['bold'])
			else:
				cprint('The room entered is not available for you to reallocate','red', attrs=['bold'])
		elif self.person_role == 'FELLOW':
			if(self.check_if_office_name_is_valid(new_room)):
				for person in self.all_people:
					if person_identifier == person.name:
						current_office = person.office_allocated
						break
				if self.swap_office_members(person_identifier,new_room,current_office):
					cprint('You have been reallocated successfully','cyan', attrs=['bold'])
				else:
					cprint('Oops!Reallocation has failed.','red', attrs=['bold'])
			elif(self.check_if_living_space_name_is_valid(new_room)):
				for person in self.all_people:
					if person_identifier == person.name:
						current_living_space = person.living_space_allocated
						break
				if self.swap_living_space_members(person_identifier,new_room,current_living_space):
					cprint('You have been reallocated successfully','cyan', attrs=['bold'])
				else:
					cprint('Oops!Reallocation has failed.','red', attrs=['bold'])

			else:
				cprint('The room entered is not available for you to reallocate.','red', attrs=['bold'])
		else:
			cprint('System was unable to identify your role.','red', attrs=['bold'])

	def load_people(self,file_path):
		""" This function loads people from a text file and allocates them
			random offices and living spaces """
		try:
			self.input_file = file_path
			if not os.path.isfile(self.input_file):
				cprint("Invalid filepath.", 'red', attrs=['bold'])
				return "Invalid filepath."
			with open(self.input_file) as people_file:
				people = people_file.readlines()
				if len(people) == 0:
					cprint('The file has no contents', 'red', attrs=['bold'])
					return 'The file has no contents'
				else:
					for person in people:
						person = person.replace('\n','')
						person = person.split(' ')
						if len(person) < 4:
							wants_accomodation = 'N'
							fname = person[0]
							lname = person[1]
							role = person[2]
							self.add_person(fname,lname, role, wants_accomodation)
						else:
							wants_accomodation = person[3]
							fname = person[0]
							lname = person[1]
							role = person[2]
							self.add_person(fname, lname, role, wants_accomodation)

		except Exception as e:
			print(str(e))
			cprint ('Oops! The system failed to read the file', 'red', attrs=['bold'])
			return 'Oops! The system failed to read the file'

	def func_office_available(self):
		""" This returns a list of all offices that have not yet accomodated their full capacity """
		del self.available_offices[:]
		for available_off in self.all_rooms_office:
			if(available_off.check_availability()):
				self.available_offices.append(available_off)

	def func_available_living_space(self):
		""" This returns a list of all offices that have not yet accomodated their full capacity """
		del self.available_living_space[:]
		for available_liv in self.all_rooms_living:
			if(available_liv.check_availability()):
				self.available_living_space.append(available_liv)

	def add_person(self, fname,lname, role, wants_accomodation):
		""" This function creates a person and allocates 
		the a random room depending on the rooms availability
			and the person's role """
		name = fname + ' ' + lname
		role = role.upper()
		wants_accomodation = wants_accomodation.upper()
		person_exists = []
		available_offices = []
		available_living_space = []

		for p_exists in self.all_people:
			person_exists.append(p_exists.name)
		if name in person_exists:
			cprint(name + ' Another user exists with the same name','red', attrs=['bold'])
			return 'Another user exists with the same name'
		else:
			random_office = None
			random_living_space = None
			self.func_office_available()
			self.func_available_living_space()
			if role == 'STAFF':
				if wants_accomodation == 'N':
					if len(self.all_rooms_office) == 0:
							cprint("Please create offices first.", 'red', attrs=['bold'])
							return "Please create offices first."
					else:
						if len(self.available_offices) == 0:
							self.add_person_to_all_people \
							(name, role, wants_accomodation,random_office,random_living_space)
							cprint(name + ' You have been added to the system but no Office or Living Space was allocated.',\
								'yellow', attrs=['bold'])
						else:
							random_office = random.choice(self.available_offices)
							self.add_person_to_all_people \
							(name, role, wants_accomodation,random_office,random_living_space)
							cprint(name + ' You have been allocated a Office successfully.',\
								   'yellow', attrs=['bold'])
				elif wants_accomodation =='Y':
					cprint('No accomodation for staff','red', attrs=['bold'])
					return 'No accomodation for staff'
				else:
					cprint('No such option. Use either Y or N', 'red', attrs=['bold'])
					return 'No such option. Use either Y or N'
			elif role == 'FELLOW':
				if wants_accomodation == 'N':
					if len(self.all_rooms_office) == 0:
						cprint("Please create offices first.", 'yellow', attrs=['bold'])
						return "Please create offices first."
					else:
						if len(self.available_offices) == 0:
							self.add_person_to_all_people \
							(name, role, wants_accomodation,random_office,random_living_space)
							cprint(name + ' You have been added to the system but no Office or Living Space was allocated.',\
									'yellow', attrs=['bold'])
						else:
							random_office = random.choice(self.available_offices)
							self.add_person_to_all_people \
							(name, role, wants_accomodation,random_office,random_living_space)
							cprint(name + ' You have been allocated a Office successfully.', 'yellow', attrs=['bold'])
				elif wants_accomodation == 'Y':
					if len(self.all_rooms_office) == 0 or len(self.all_rooms_living) == 0:
						cprint("Please create offices and living_spaces first.", 'yellow', attrs=['bold'])
						return 'Please create offices and living_spaces first.'
					else:
						if len(self.available_offices) == 0:
							if len(self.available_living_space) == 0:
								self.add_person_to_all_people \
								(name, role, wants_accomodation,random_office,random_living_space)
								cprint(name + ' You have been added to the system but no Office or Living Space was allocated.',\
										'yellow', attrs=['bold'])
							else:
								random_living_space = random.choice(self.available_living_space)
								self.add_person_to_all_people \
								(name, role, wants_accomodation,random_office,random_living_space)
								cprint(name + ' You have been added to the system. You were allocated a Living space only.',\
										'yellow', attrs=['bold'])
						else:
							random_office = random.choice(self.available_offices)
							if len(self.available_living_space) == 0:
								self.add_person_to_all_people \
								(name, role, wants_accomodation,random_office,random_living_space)
								cprint(name + ' You have been allocated a Office successfully. Living space is still unavailable',\
										'yellow', attrs=['bold'])
							else:
								random_living_space = random.choice(self.available_living_space)
								self.add_person_to_all_people \
								(name, role, wants_accomodation,random_office,random_living_space)
								cprint(name + ' You have been allocated a Office and a Living Space successfully',\
										'yellow', attrs=['bold'])
				else:
					print('No such option. Use either Y or N')
					return 'No such option. Use either Y or N'

			else:
				print('Your role is undefined')
				return('Your role is undefined')

	def add_person_to_all_people(self, name, role, wants_accomodation,random_office,random_living_space):
		""" This functions creates a person object with the help of add_person function.
			After creating a person, the function adds the person to all_people list which
			holds all people objects"""
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

	def  create_room(self, room_name):
		""" This function creates a rooms either as offices or living spaces"""
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
					cprint('One of the rooms entered exits', 'red', attrs=['bold'])
					return 'One of the rooms entered exits'
					break
				else:
					office = Office(office,room_type)
					self.all_rooms_office.append(office)
			cprint('The following offices have been added :', 'cyan', attrs=['bold'])
			for room in self.all_rooms_office:
				cprint(room.room_name, 'yellow', attrs=['bold'])
		elif room_type == 'LIVING_SPACE':
			room_name_list_living =[]
			room_name_list_living = room_name
			room_exists_list_living = []
			del room_name_list_living[-1]
			for room in self.all_rooms_living:
				room_exists_list_living.append(room.room_name)
			for room in room_name_list_living:
				if room in room_exists_list_living:
					cprint('One of the rooms entered exits','cyan', attrs=['bold'])
					return 'One of the rooms entered exits'
					break
				else:
					living = Living_Space(room,room_type)
					self.all_rooms_living.append(living)
			cprint('The following living spaces have been added :', 'cyan', attrs=['bold'])
			for room in self.all_rooms_living:
				cprint(room.room_name, 'yellow', attrs=['bold'])
		else:
			cprint('You can only create OFFICE or a LIVING_SPACE', 'red', attrs=['bold'])
			return 'You can only create OFFICE or a LIVING_SPACE'
