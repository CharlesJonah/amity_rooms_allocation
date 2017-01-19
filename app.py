"""
This uses docopt library to allow for a smooth user Interactive session.
Usage:

    rooms_app add_person <person_name> <role> [--wants_accommodation=N]
    rooms_app create_room <room_name>...
    rooms_app reallocate_person <person_identifier> <room_name> <room_type>
    rooms_app save_state [--db=sqlite_database]
    rooms_app load_state <database>
    rooms_app print_allocations [--o=filename]
    rooms_app print_allocated [--o=filename]
    rooms_app load_people <file_path>
    rooms_app print_room <room_name>
    reallocate_person <person_identifier> <new_room_name>



Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
import os
sys.path.append('./app_classes')
from amity import Amity
from docopt import docopt, DocoptExit
amity = Amity()

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('\n')
            print('Invalid Command! Use the below syntax:')
            print(e)
            print('\n')
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            return

        return func(self,opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

#This class ties all the docopt calling functions
class ScreenOut (cmd.Cmd):
    #The prompt that shows the use that he or she is running form the application in the cmd
    prompt = '<rooms_app>'

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <person_name> <role> [--wants_accommodation=N]"""
        person_name = args['<person_name>']
        role = args['<role>']
        if args['--wants_accommodation'] is None:
            args['--wants_accommodation'] = 'N'
        wants_accommodation = args['--wants_accommodation'] 
        amity.add_person(person_name, role, wants_accommodation)

    # This cmd links to the search() method
    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_name>..."""
        amity.create_room(args['<room_name>'])

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        amity.reallocate_person(args['<person_identifier>'],args['<new_room_name>'])

    @docopt_cmd
    def do_save_state(self,args):
        """Usage: save_state [--db=sqlite_database]"""
        if args['--db'] is None:
            db_name = 'amity'
            amity.save_state(db_name)
        else:
            db_name = args['--db']
            amity.save_state(db_name)

    @docopt_cmd
    def do_load_state(self,args):
        """Usage: load_state <database>"""
        amity.load_state(args['<database>'])

    @docopt_cmd
    def do_print_allocations(self,args):
        """Usage: print_allocations [--o=filename]"""
        if args['--o'] is None:
            filename = None
            amity.print_allocations(filename)
        else:
            filename = args['--o']
            amity.print_allocations(filename)

    @docopt_cmd
    def do_print_unallocated(self,args):
        """Usage: print_unallocations [--o=filename]"""
        if args['--o'] is None:
            filename = None
            amity.print_unallocated(filename)
        else:
            filename = args['--o']
            amity.print_unallocated(filename)

    @docopt_cmd
    def do_load_people(self,args):
        """Usage: load_people <file_path>"""
        amity.load_people(args['<file_path>'])
    @docopt_cmd
    def do_print_room(self,args):
        """Usage: print_room <room_name>"""
        amity.print_room(args['<room_name>'])




    # This cmd allows the user to quit from the app
    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('Successfully Exited Program')
        exit()


ScreenOut().cmdloop()

print(opt)
