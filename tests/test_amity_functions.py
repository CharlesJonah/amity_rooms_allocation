import unittest
import sys
sys.path.append('./app_classes')
from amity import Amity
#Tests under add_person functions
class AmityTestAddPerson(unittest.TestCase):
	""" This class tests all cases associated with add_person function """

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()

	def test_add_person(self):
		"Test that person is added"
		add_person = self.amity.add_person('Charles','Mac','Fellow','Y')
		self.assertEqual(add_person, 'Please create offices and living_spaces first.')
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		self.amity.add_person('Charles','Mac','STAFF','N')
		self.assertEqual(len(self.amity.all_people), 1)

	def test_if_person_exists(self):
		"Test if the person exists"
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_person = self.amity.add_person('Charles','Mac','Fellow','Y')
		add_person = self.amity.add_person('Charles','Mac','Fellow','Y')
		self.assertEqual(add_person, 'Another user exists with the same name')

	def test_add_person_with_accomodation_when_no_rooms_have_been_created(self):
		"Tests if there are living rooms and offices before adding a fellow who wants accomodation"
		add_person = self.amity.add_person('Charles','Mac','Fellow','Y')
		self.assertEqual(add_person, 'Please create offices and living_spaces first.')

	def test_add_person_with_accomodation_when_no_rooms_have_been_created(self):
		"Tests if there are offices before adding a fellow without accomodation"
		add_person = self.amity.add_person('Charles','Mac','Fellow','N')
		self.assertEqual(add_person, 'Please create offices first.')

	def test_rejects_when_staff_wants_accomodation(self):
		"Tests if the system denies staff accomodation."
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_person = self.amity.add_person('Charles','Mac','STAFF','Y')
		self.assertEqual(add_person, 'No accomodation for staff')

	def test_if_optional_args_for_wants_accomodation_is_valid(self):
		"Tests if optional argument for add_person is Y or N"
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_person = self.amity.add_person('Charles','Mac','STAFF','R')
		self.assertEqual(add_person, 'No such option. Use either Y or N')

	def test_if_person_role_is_valid(self):
		"Tests if the role is either staff or fellow "
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_person = self.amity.add_person('Charles','Mac','STAF','N')
		self.assertEqual(add_person, 'Your role is undefined')

class AmityTestCreateRoom(unittest.TestCase):
	""" This class tests all cases associated with create_room function """

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()

	def test_if_room_is_office_or_living_space(self):
		"Tests if the type of room given is either a living space or an office"
		add_room = self.amity.create_room(['SHIRE','OFFIC'])
		self.assertEqual(add_room, 'You can only create OFFICE or a LIVING_SPACE')

	def tests_if_office_roomname_exists(self):
		"Tests that if office room name exists"
		add_room = self.amity.create_room(['SHIRE','OFFICE'])
		add_room = self.amity.create_room(['SHIRE','OFFICE'])
		self.assertEqual(add_room, 'One of the rooms entered exits')

	def tests_if_living_space_exists(self):
		"Tests if living space name does not exist"
		add_room = self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_room = self.amity.create_room(['RUBY','LIVING_SPACE'])
		self.assertEqual(add_room, 'One of the rooms entered exits')

class AmityTestLoadPeople(unittest.TestCase):
	""" This class tests all cases associated with load_people function """

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()

	def test_load_people_handles_invalid_path(self):
		"Tests if a file path is valid"
		wrong_path = '/wrongfilepath.txt'
		status = self.amity.load_people(wrong_path)
		self.assertEqual('Invalid filepath.', status)

	def test_if_load_people_filepath_loads_file(self):
		"Tests if file is loaded"
		empty_filepath = 'files/empty_file.txt'
		status = self.amity.load_people(empty_filepath)
		self.assertEqual('The file has no contents', status)

class AmityTestReallocatePerson(unittest.TestCase):
	"""This class contains tests for the reallocate_person function"""

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()

	def test_if_person_name_exists_before_reallocation(self):
		"Tests if the person name exists so as to reallocate the person"
		people_list = []
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		self.amity.add_person('Charles','Mac','Fellow','Y')
		self.amity.reallocate_person('Charles','Mac','SHIRE')
		for person in self.amity.all_people:
			person_name = person.name
			people_list.append(person_name)
		self.assertTrue('Charles Mac' in people_list)

	def test_if_office_exists_before_reallocation(self):
		office_list = []
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.add_person('Charles','Mac','Fellow','Y')
		self.amity.reallocate_person('Charles','Mac','SHIRE')
		for office in self.amity.all_rooms_office:
			room_name = office.room_name
			office_list.append(room_name)
		self.assertTrue('SHIRE' in office_list)

class AmityTestPrintAllocations(unittest.TestCase):
	"""This class contains tests for the print_allocations function"""

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()
	
	def test_if_office_exists_before_its_printing_members(self):
		""" Tests if there are existing offices before printing the office
			members """
		self.assertEqual(self.amity.print_allocations('test_file'),'No offices in the system')
	
	def test_if_filename_contains_unwanted_characters(self):
		""" Tests if the filename contains unwanted characters """
		self.assertEqual(self.amity.print_allocations('test/<>file'), False)

class AmityTestPrintUnallocated(unittest.TestCase):
	"""This class contains tests for the print_unallocated function """

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()
	
	def test_if_system_has_people_before_printing(self):
		""" Tests if the system has people before printing them
			members """
		self.assertEqual(self.amity.print_unallocated('test_file'),'No people found in the system')
	
	def test_if_filename_contains_unwanted_characters(self):
		""" Tests if the filename contains unwanted characters """
		self.assertEqual(self.amity.print_unallocated('test/<>file'), False)

class AmityTestPrintRoom(unittest.TestCase):
	""" This class contains tests for the print_room function """

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()
	
	def test_if_room_name_is_valid(self):
		""" Tests if room name is a valid name in the system """
		self.assertEqual(self.amity.print_room('test_room'), 'Room was not found')

class AmityTestLoadState(unittest.TestCase):
	""" This class contains tests for the load_state function """

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()
	
	def test_if_database_name_contains_unwanted_characters(self):
		""" Tests if the database name contains unwanted characters """
		self.assertEqual(self.amity.load_state('db/<>name'), False)

class AmityTestSaveState(unittest.TestCase):
	""" This class contains tests for the save_state function """

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()
	
	def test_if_database_name_contains_unwanted_characters(self):
		""" Tests if the database name contains unwanted characters """
		self.assertEqual(self.amity.save_state('db/<>name'), False)

if __name__ == '__main__':

	unittest.main()
