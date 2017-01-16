import unittest
import sys
sys.path.append('./app_classes')
from amity import Amity
#Tests under add_person functions
class AmityTest_AddPerson(unittest.TestCase):

	"Setup for class initializations"
	def setUp(self):
		self.amity = Amity()

	def test_add_person(self):
		"Test that person is added"
		add_person = self.amity.add_person('Charles','Fellow','Y')
		self.assertEqual(add_person, 'Please create offices and living_spaces first.')
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		self.amity.add_person('Charles','STAFF','N')
		self.assertEqual(len(self.amity.all_people), 1)

	def test_person_exists(self):
		"Test if the person exists"
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_person = self.amity.add_person('Charles','Fellow','Y')
		add_person = self.amity.add_person('Charles','Fellow','Y')
		self.assertEqual(add_person, 'Another user exists with the same name')

	def test_rooms_adding_fellow_with_accomodation(self):
		"Tests if there are living rooms and offices before adding a fellow who wants accomodation"
		add_person = self.amity.add_person('Charles','Fellow','Y')
		self.assertEqual(add_person, 'Please create offices and living_spaces first.')

	def test_rooms_adding_fellow_without_accomodation(self):
		"Tests if there are office before adding fellow without accomodation"
		add_person = self.amity.add_person('Charles','Fellow','N')
		self.assertEqual(add_person, 'Please create offices first.')

	def test_fellow_added_without_office_and_living_space(self):
		"Tests if fellow is added without office and living space"

	def test_staff_wants_accomodation(self):
		"Tests if the system denies staff accomodation."
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_person = self.amity.add_person('Charles','STAFF','Y')
		self.assertEqual(add_person, 'No accomodation for staff')

	def test_if_optional_wants_accomodation_is_valid(self):
		"Tests if optional argument for add_person is Y or N"
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_person = self.amity.add_person('Charles','STAFF','R')
		self.assertEqual(add_person, 'No such option. Use either Y or N')

	def test_if_role_is_valid(self):
		"Tests if the role is either staff or fellow "
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		add_person = self.amity.add_person('Charles','STAF','N')
		self.assertEqual(add_person, 'Your role is undefined')

class AmityTest_CreateRoom(unittest.TestCase):

	"Setup for class initializations"
	def setUp(self):
		self.amity = Amity()

	"Test for create_room room fuctions"
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

class AmityTest_LoadPeople(unittest.TestCase):

	"Setup for class initializations"
	def setUp(self):
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

class AmityTest_ReallocatePerson(unittest.TestCase):
	"This class contains tests for the reallocate_person function"

	def setUp(self):
		"Setup for class initializations"
		self.amity = Amity()

	def test_if_person_name_exists_before_reallocation(self):
		"Tests if the person name exists so as to reallocate the person"
		people_list = []
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.create_room(['RUBY','LIVING_SPACE'])
		self.amity.add_person('Charles','Fellow','Y')
		self.amity.reallocate_person('Charles','SHIRE')
		for person in self.amity.all_people:
			person_name = person.name
			people_list.append(person_name)
		self.assertTrue('Charles' in people_list)

	def test_if_office_exists_before_reallocation(self):
		office_list = []
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.add_person('Charles','Fellow','Y')
		self.amity.reallocate_person('Charles','SHIRE')
		for office in self.amity.all_rooms_office:
			room_name = office.room_name
			office_list.append(room_name)
		self.assertTrue('SHIRE' in office_list)






	def test_reallocate_person(self):

		pass



	def test_load_people(self):

		pass



	def test_print_allocations(self):

		pass



	def test_print_unallocated(self):

		pass



	def test_print_room(self):

		pass



	def test_save_state(self):

		pass



	def test_load_state(self):

		pass







if __name__ == '__main__':

	unittest.main()
