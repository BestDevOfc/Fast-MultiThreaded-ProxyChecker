import sys
import random
import requests
import time
import threading

from concurrent.futures import ThreadPoolExecutor

# simple configurations (headers, web API to test proxies on, http://httpbin.org/ip is used by default)
from src.templates import*
from src.proxyConfig import ProxyResources, ProxyType

class ProxyChecker(object):
    '''
    
        Checks proxies using 2 ways:
            1) Sockets
            2) Website URLs (safest without a VPN being used.)
    
    '''
    def __init__(self, proxies_list: list[str], threads: int, proxy_type: ProxyType, timeout: int = 5) -> None:
        self.proxies_list = proxies_list
        self.threads = threads                              # NOTE: I wonder if we can use multiple cores and throw threads on those
                                                            # for even higher speeds.

        self.proxy_type = proxy_type                        # we use an ENUM for this to keep development easier and tidy
        self.timeout = timeout                              # we're going to keep this at defaulted 5 seconds
        self.config = ProxyResources().load_cfg()           # (for dev) simple config of rotating userAgents + HTTP URL to test proxies on.
        self.results_file = open(self.create_results_file(), 'w')
        self.ThreadLocker = threading.Lock()                # used when writing to files to prevent race conditions.
        self.results_stats: dict = {
            "Valids": 0,
            "Invalids": 0,
            "Retries": 0,
            "Errors": 0,
            "Time Passed": 0
        }

    def create_results_file(self) -> None:
        '''
        
            Just creates the Results/ValidProxies.txt 
            file, keeps everything tidy and easy to change if needed 
            in the future.
        
        '''
        root_path: str = f"Results/{time.time()}"
        os.makedirs(f"{root_path}", exist_ok=True)
        return f"{root_path}/Valids_Proxies.txt"

    
    def display_results(self) -> None:
        '''
        
            Displays all the results from the checking process of the proxies.

            * It self-terminates by simply checking if all proxies have been checked,
            this is intended to run as a Daemon thread for it is IO blocking method!
        
        '''
        start = time.time()
        total_len = len(self.proxies_list)
        # see if we've checked all the proxies, and once we have stop displaying results.
        total_checked = 0
        while total_checked < total_len:
            clear_screen()

            current = time.time()
            seconds_passed = int(current-start)
            total_checked = self.results_stats['Valids']+self.results_stats['Invalids']
            print(f'''
                    {Display.TITLE}                    
                    {Display.LINE}

                    {Cols.RED} [+] - {Cols.GREEN}Made with {Cols.RED}\u2764\uFE0F {Cols.GREEN}by: {Cols.MAGENTA}{Display.DISCORD_CONTACT}

                    {Cols.RED} [+] - {Cols.GREEN}Checked: {Cols.YELLOW}{total_checked:,}/{total_len:,}
                    {Cols.RED} [+] - {Cols.GREEN}Valids: {Cols.YELLOW}{self.results_stats['Valids']:,}
                    {Cols.RED} [+] - {Cols.GREEN}Invalids: {Cols.YELLOW}{self.results_stats['Invalids']:,}
                    {Cols.RED} [+] - {Cols.GREEN}Time Passed: {Cols.YELLOW}{seconds_passed:,}
                    {Cols.RED} [+] - {Cols.GREEN}Errors: {Cols.RED}{self.results_stats['Errors']:,}

                    {Display.LINE}

                  ''')
            time.sleep(3)

        
        input(f"{Cols.GREEN}[ Done! ]")
    def check_proxy_web(self, proxy: bytes) -> bool:
        '''
        
            - checks a proxy, this is meant to be run as a threadpool.
            - Uses a website URL to check the proxy
            - For web proxies using a site to check is the most accurate. Connecting directly via 
            sockets may not always be accurate since it can lead to ISP bans or flags. 

            When I use SocketProxyChecker option I always have a VPN on, many VPNs will
            block certain socket (TCP) connections, so this one is always the safe bet for accuracy.

            However, for speed I typically just shoot for the SocketProxyChecker since it's way faster.
        
        '''
        try:
            proxy = proxy.decode().strip().rstrip()
            headers: dict = {
                "User-Agent": random.choice(self.config['UserAgents'])
            }
            proxies: dict = {
                "http": f"{self.proxy_type}://{proxy}",
                "https": f"{self.proxy_type}://{proxy}"
            }
            
            # proxy request was successful, so proxy is valid:
            req = requests.get(url=self.config['API'], headers=headers, proxies=proxies, timeout=self.timeout)
            self.results_stats['Valids'] += 1

            ''' Write into file using threadlocking to prevent race conditions. '''
            # self.ThreadLocker.acquire()
            with self.ThreadLocker:
                self.results_file.write(f"{proxy}\n")
                self.results_file.flush()
            # self.ThreadLocker.release()

            
        except Exception as err:
            # proxy is not valid since an exception was thrown, could be bcs of timeout or invalid format of that proxy
            # regardless, we'll count it as an invalid
            self.results_stats['Invalids'] += 1

    def start_checker(self):
        # Daemon thread (runs in background, when program exits thread exits, clean termination.)
        display_thread = threading.Thread(target=self.display_results, daemon=True)
        display_thread.start()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.check_proxy_web, self.proxies_list)
        
        '''
            * Had an annoying bug where the program would enter a I/O blocking state 
            after the ThreadPoolExecutor... completed, so after the display function said "DONE!", which was weird.
            
            Turns out that when when the threadpoolexecutor was finished it terminated the main thread
            because it's done. However, this created a timing synchronization issue because the display_thread()
            waits 3 seconds before exiting so it was left in an unknown state since the parent thread terminated, this is 
            why the program was thrown into a "sleep state" (IO blocking state).

            solution: display_thread.join()
        '''
        display_thread.join()
