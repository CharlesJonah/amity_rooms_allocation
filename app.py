"""
Welcome to Amity Rooms allocation System.
Usage:

    rooms_app add_person <first_name> <last_name> <role> [--wants_accommodation=N]
    rooms_app create_room <room_name>...
    rooms_app reallocate_person <person_identifier> <room_name> <room_type>
    rooms_app save_state [--db=sqlite_database]
    rooms_app load_state <database>
    rooms_app print_allocations [--o=filename]
    rooms_app print_allocated [--o=filename]
    rooms_app load_people <file_path>
    rooms_app print_room <room_name>
    rooms_app upload_database
    reallocate_person <first_name> <last_name> <new_room_name>



Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
import os
sys.path.append('./app_classes')

from docopt import docopt, DocoptExit
from termcolor import cprint, colored

from amity import Amity
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

     #The below statements print a menu to act as a directive to the user
    cprint("* * * * * * * * * * * * * * * * * * * * * * * * *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("*           AMITY ROOMS ALLOCATION              *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* * * * * * * * * * * * * * * * * * * * * * * * *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* USE THE LISTED COMMAND TO EXECUTE TASKS       *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 1. create_room                                *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 2. add_person                                 *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 3. reallocate_person                          *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 4. save_state                                 *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 5. load_state                                 *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 6. print_room                                 *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 7. load_people                                *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 7. print_allocations                          *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 7. print_unallocated                          *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 8. sync                                       *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 9. help                                       *",'cyan', attrs=['bold'])
    cprint("*                                               *",'cyan', attrs=['bold'])
    cprint("* 9. quit                                       *",'cyan', attrs=['bold'])
    cprint("* * * * * * * * * * * * * * * * * * * * * * * * *",'cyan', attrs=['bold'])
    print("                                                 ")

    #The prompt that shows the user that he or she is running form the application in the cmd
    prompt = '<rooms_app>'

    #This cmd allows the user to parse arguments for calling the add_person function
    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <first_name> <last_name> <role> [--wants_accommodation=N]"""
        first_name = args['<first_name>']
        last_name = args['<last_name>']
        role = args['<role>']
        if args['--wants_accommodation'] is None:
            args['--wants_accommodation'] = 'N'
        wants_accommodation = args['--wants_accommodation']
        amity.add_person(first_name, last_name, role, wants_accommodation)

    # This cmd allows the user to parse arguments for calling create_room function
    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_name>..."""
        amity.create_room(args['<room_name>'])

    #This cmd syncs the local sqlite database with online firebase database
    def do_sync(self, args):
        """Usage: sync"""
        amity.sync()

    # This cmd allows the user to parse arguments for calling the reallocate_person function
    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <first_name> <last_name> <new_room_name>"""
        amity.reallocate_person(args['<first_name>'],args['<last_name>'],args['<new_room_name>'])

    # This cmd allows the user to call the save_state function
    @docopt_cmd
    def do_save_state(self,args):
        """Usage: save_state [--db=sqlite_database]"""
        if args['--db'] is None:
            db_name = 'amity'
            amity.save_state(db_name)
        else:
            db_name = args['--db']
            amity.save_state(db_name)

    # This cmd allows the user the load_state function
    @docopt_cmd
    def do_load_state(self,args):
        """Usage: load_state <database>"""
        amity.load_state(args['<database>'])

    # This cmd allows the user the load_state function
    @docopt_cmd
    def do_update_database(self,args):
        """Usage: upload_database """
        amity.update_database()

    # This cmd allows the user to call the print_allocations function
    @docopt_cmd
    def do_print_allocations(self,args):
        """Usage: print_allocations [--o=filename]"""
        if args['--o'] is None:
            filename = None
            amity.print_allocations(filename)
        else:
            filename = args['--o']
            amity.print_allocations(filename)

    # This cmd allows the user to call the print_unallocated function
    @docopt_cmd
    def do_print_unallocated(self,args):
        """Usage: print_unallocations [--o=filename]"""
        if args['--o'] is None:
            filename = None
            amity.print_unallocated(filename)
        else:
            filename = args['--o']
            amity.print_unallocated(filename)

    #This cmd allows the user to call the load_people function
    @docopt_cmd
    def do_load_people(self,args):
        """Usage: load_people <file_path>"""
        amity.load_people(args['<file_path>'])

    #This cmd allows the user to call print_room function
    @docopt_cmd
    def do_print_room(self,args):
        """Usage: print_room <room_name>"""
        amity.print_room(args['<room_name>'])

    # This cmd allows the user to quit from the application
    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        cprint('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *','cyan', attrs=['bold'])
        cprint('*                  AMITY ROOMS ALLOCATIONS                  *','cyan', attrs=['bold'])
        cprint('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *','cyan', attrs=['bold'])
        cprint('*                                                           *','cyan', attrs=['bold'])
        cprint('*       BYE! YOU HAVE SUCCESSFULLY EXITED THE PROGRAM       *','cyan', attrs=['bold'])
        cprint('*                                                           *','cyan', attrs=['bold'])
        cprint('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *','cyan', attrs=['bold'])
        exit()


ScreenOut().cmdloop()

print(opt)
