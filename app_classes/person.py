# Main class model for person entity
class Person(object):
	def __init__(self,name,role,wants_accomodation):
		self.name = name
		self.role = role
		self.wants_accomodation = wants_accomodation
		self.office_allocated = ''
		self.living_space_allocated = ''

# Class Staff inherits from model
class Staff(Person):
	def __init__(self,name,role,wants_accomodation):
		Person.__init__(self,name,role,wants_accomodation)
		self.rooms_type = ['Office']

# Class Fellow inherits from model
class Fellow(Person):
	def __init__(self,name,role,wants_accomodation):
		Person.__init__(self,name,role,wants_accomodation)
		self.rooms_type = ['Office','Living Space']
