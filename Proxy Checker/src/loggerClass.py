import time
import logging

from src.templates import*
from functools import wraps

# Everything related to Errors are here.

class Logger(object):
    '''
    
        Makes logging easier through different files and custom classes.
        Simply just creates a logging object and keeps everything centrally managed, I 
        can make changes whenever.
    
    '''
    def __init__(self, log_file_name='app.log'):
        # Set up the logger
        self.log_file_name = log_file_name
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)  # Set the logging level

        # Create a file handler
        file_handler = logging.FileHandler(self.log_file_name)
        file_handler.setLevel(logging.ERROR)  # Log only error messages to the file

        # Create a formatter and set it for the file handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)

    def log_err(self, err: str):
        # Log the error message to the file
        self.logger.error(err)


def print_err(msg: str, enter_to_continue: bool = True):
    '''
    
        Prints errors easily for me + formats + enhances user experience.

    '''
    print(f"{Cols.GREEN}[!] - {Cols.RED}[ {msg} ]")
    if enter_to_continue == True:
        time.sleep(3)
    else:
        input(f"[ Enter to Continue. ]")

# don't want to keep defining this Object in every python file
loggerObj = Logger()

def func_logger(func):
    '''
        - decorator to log exceptions from functions so I don't have to write
        1000 try/except blocks. 
        - This will mainly be thrown onto functions that are prone to breaking during 
        development and not so much for production.
        - However, if a function for some reason in production does break that was not meant ot 
            this still provides a user message.
    
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            loggerObj.log_err(f"in {func.__name__} --> {err}")
            # re-raise the exception if you want the program to crash
            print_err(f"[ For some reason an unexpected exception was thrown in function \'{func.__name__}\', please"\
                      f"contact developer on discord: {Display.DISCORD_CONTACT} ]", enter_to_continue=True)
    return wrapper




# allows me to easily differentiate between unexpected Exceptions and Exceptions that I expect
class customException(Exception):
    ...