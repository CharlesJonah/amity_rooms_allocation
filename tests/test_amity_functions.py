import unittest
import sys
sys.path.append('./app_classes')
from amity import Amity
#Main Testing class
class AmityTest(unittest.TestCase):
	#Setup for class initializations
	def setUp(self):
		self.amity = Amity()
	
	#Tests under add_person function

	def test_add_person(self):
		"Test that person is added"
		total_people = len(self.amity.all_people)
		self.assertEqual(len(self.amity.all_people), 0)
		self.amity.create_room(['SHIRE','OFFICE'])
		self.amity.add_person('Charles','Fellow','Y')
		self.amity.add_person('Eric','Fellow','Y')
		total_people = len(self.amity.all_people)
		self.assertEqual(len(self.amity.all_people), total_people)
	
	def test_create_room(self):
		 "Test for adding offices"
		 total_rooms = len(self.amity.all_rooms_office)
		 self.assertEqual(len(self.amity.all_rooms_office), total_rooms)
		 self.amity.create_room(['SHIRE','CARMELOT','HOGWARTS','OFFICE'])
		 total_rooms = len(self.amity.all_rooms_office)
		 self.assertEqual(len(self.amity.all_rooms_office), total_rooms)

		 "Test for adding living_spaces"
		 total_rooms = len(self.amity.all_rooms_office)
		 self.assertEqual(len(self.amity.all_rooms_office), total_rooms)
		 self.amity.create_room(['R','RUBY','BLOCKCHAIN','LIVING_SPACE'])
		 total_rooms = len(self.amity.all_rooms_office)
		 self.assertEqual(len(self.amity.all_rooms_office), total_rooms)

		 "Test if a room is added more than once"
		 test_add_living_twice = self.amity.create_room(['RUBY','LIVING_SPACE'])
		 self.assertEqual(test_add_living_twice, "One of the rooms entered exits")

		 "Test if a room is added more than once"
		 test_add_office_twice = self.amity.create_room(['CARMELOT','OFFICE'])
		 self.assertEqual(test_add_office_twice, "One of the rooms entered exits")




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
