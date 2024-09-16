import tkinter as tk
from tkinter.filedialog import askopenfilename

from src.proxyConfig import*
from src.loggerClass import*


class GetUserInput(object):
    '''
    
         - Simply just asks questions that are needed to check the proxies 
            1) Proxy Type
            2) Proxy File Path
            3) # of threads you want
        - Runs it in a while loop to catch any mistakes made by the user,
            this just enhances user experience.
    
    '''
    def __init__(self):
        ...
    def get_file_path(self) -> str:
        '''
        
            Gets a file path using a window for better user experience.
            Moreover, this follows the 
            while-loop shenanigans as well.
        
        '''
        # we don't want a full GUI, so keep the root window from appearing
        root = tk.Tk()
        root.withdraw()

        while True:
            try:
                # Open a file selection dialog
                file_path = askopenfilename(title = "Select A File")
                
                # Check if the user selected a file
                if not file_path:
                    raise customException(f"No file selected, please select one")
                break
            except Exception as err:
                loggerObj.log_err(f"in \'get_file_path()\' --> {err}")
                print_err(f"{err}", False)
            except customException as err:
                loggerObj.log_err(f"in \'get_file_path()\' --> {err}")
                print_err(f"{err}", True)
        
        '''
        
            * Another bug, you have to ensure to to keep the below line, because
            if we do not root.destroy() the window there will be a "Tcl_WaitForEvent: Notifier not initialized"
            exception because Tkinter works in a single thread. When the main thread is destroyed 
            the root thread for tkinter is still running, which was the same issue we had with the 
            I/O sleep state of "display_thread", .join() was the solution.

        '''
        root.destroy()
        return file_path

    
    def get_proxy_type(self) -> ProxyType:
        number_to_enum = {
            1: ProxyType.HTTP_HTTPS,
            2: ProxyType.SOCKS4,
            3: ProxyType.SOCKS5
        }
        while True:
            try:
                clear_screen()
                print(f'''
                        {Display.TITLE}                    
                        {Display.LINE}

                        {Cols.RED} [+] - {Cols.GREEN} [ What Proxies are you checking? ]
                        
                        {Cols.RED} [1] - {Cols.YELLOW} [ HTTP/HTTPS ]
                        {Cols.RED} [2] - {Cols.YELLOW} [ SOCKS4 ]
                        {Cols.RED} [3] - {Cols.YELLOW} [ SOCKS5 ]
                        {Cols.RED} [TODO] - {Cols.MAGENTA} [ Unknown (auto-identifier) ]

                        {Display.LINE}
                    ''') 
                proxy_type = int(input("[+] - ").strip().rstrip())
                if proxy_type not in number_to_enum.keys():
                    raise customException(f"[ Invalid Proxy Type! ]")
                else:
                    return number_to_enum[proxy_type]

            except Exception as err:
                loggerObj.log_err(f"in \'get_proxy_type()\' --> {err}")
                print_err(f"Something went wrong, please try again", False)
            except customException as err:
                loggerObj.log_err(f"in \'get_proxy_type()\' --> {err}")
                print_err(f"{err}", True)
    def get_proxies(self) -> list[bytes]:
        while True:
            try:
                clear_screen()
                print(f'''
                        {Display.TITLE}                    
                        {Display.LINE}

                        {Cols.RED} [+] - {Cols.GREEN} [ Specify proxy path ]

                        {Display.LINE}
                    ''') 
                time.sleep(2)
                proxies_path: str = self.get_file_path()
                if os.path.isfile(proxies_path) != True:
                    raise customException(f"[ Proxies File Path Does not Exist or is not a File ! ]")\
                
                proxies_list = list(set(open(f"{proxies_path}", 'rb').readlines()))
                return proxies_list
                    

            except Exception as err:
                loggerObj.log_err(f"in \'get_proxies()\' --> {err}")
                print_err(f"Something went wrong, please try again", False)
            except customException as err:
                loggerObj.log_err(f"in \'get_proxies()\' --> {err}")
                print_err(f"{err}", True)
    def get_threads(self) -> int:
        while True:
            try:
                clear_screen()
                print(f'''
                        {Display.TITLE}                    
                        {Display.LINE}

                        {Cols.RED} [+] - {Cols.GREEN} [ Enter the number of threads ]
                        {Cols.RED} [*] - {Cols.YELLOW} [ Reccommended: 100-150 ]

                        {Display.LINE}
                    ''') 
                num_threads = int(input('[+] ').strip().rstrip())
                if num_threads <= 0:
                    raise customException(f"Please enter thread amount that is above 0!")
                return num_threads

            except Exception as err:
                loggerObj.log_err(f"in \'get_threads()\' --> {err}")
                print_err(f"Please enter a valid integer for threads", True)
            except customException as err:
                # I know why exception was thrown, that's why we're using the customException
                # because we want the user to see the message
                loggerObj.log_err(f"in \'get_threads()\' --> {err}")
                print_err(f"{err}", False)
    def get_checker_type(self) -> ProxyType:
        number_to_enum = {
            1: CheckerType.WEBSITE,
            2: CheckerType.SOCKET,
        }
        while True:
            try:
                clear_screen()
                print(f'''
                        {Display.TITLE}                    
                        {Display.LINE}

                        {Cols.RED} [+] - {Cols.GREEN} [ What method do you want to check the proxies against? ]
                        {Cols.RED} [*] - {Cols.MAGENTA} [ Website is {Cols.GREEN}safer {Cols.MAGENTA}without a VPN + more reliable ]
                        {Cols.RED} [*] - {Cols.MAGENTA} [ Sockets are more {Cols.RED}dangerous {Cols.MAGENTA}without a VPN + faster ]

                        {Cols.RED} [1] - {Cols.YELLOW} [ Website ]
                        {Cols.RED} [2] - {Cols.YELLOW} [ Sockets ]

                        {Display.LINE}
                    ''') 
                checker_type = int(input("[+] - ").strip().rstrip())
                if checker_type not in number_to_enum.keys():
                    raise customException(f"[ Invalid Checker Type! ]")
                else:
                    return number_to_enum[checker_type]

            except Exception as err:
                loggerObj.log_err(f"in \'get_checker_type()\' --> {err}")
                print_err(f"Something went wrong, please try again", False)
            except customException as err:
                loggerObj.log_err(f"in \'get_checker_type()\' --> {err}")
                print_err(f"{err}", True)