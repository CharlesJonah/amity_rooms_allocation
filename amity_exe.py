"""
This uses docopt library to allow for a smooth user Interactive session.
Usage:

    rooms_app add_person <person_name> <role> <wants_accommodation>
    rooms_app create_room <room_name>...
    rooms_app reallocate_person <person_identifier> <room_name> <room_type>
    rooms_app save_state
    rooms_app load_people <file_path>
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

#This function clears the screen for fresh output
def clear_screen():
    clear = lambda: os.system('cls')
    clear()

#This class ties all the docopt calling functions
class ScreenOut (cmd.Cmd):


    #The prompt that shows the use that he or she is running form the application in the cmd
    prompt = '<rooms_app> '

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <person_name> <role> <wants_accommodation>"""
        amity.add_person(args['<person_name>'],args['<role>'],args['<wants_accommodation>'])

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
    def do_save_state(self,arg):
        """Usage: save_state """
        amity.save_state()

    @docopt_cmd
    def do_load_state(self,arg):
        """Usage: save_state """
        amity.load_state()

    @docopt_cmd
    def do_load_people(self,args):
        """Usage: load_people <file_path>"""
        amity.load_people(args['<file_path>'])




    # This cmd allows the user to quit from the app
    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        clear_screen()
        print('Successfully Exited Program')
        exit()


ScreenOut().cmdloop()

print(opt)
