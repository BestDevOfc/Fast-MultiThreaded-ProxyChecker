'''
Proxy checker should have API 1 and API 2
API 1 (web): 
    - using HTTP get requests
API 2 (sockets):
    - using sockets

    reason it's different is because sockets are faster but can lead to bans + VPNs may block the socket connections.
'''


from src.templates import*
from src.ProxyChecker import ProxyChecker
from src.loggerClass import func_logger
from src.getUserInput import GetUserInput
from src.proxyConfig import ProxyType, CheckerType


# TODO: proxy identifier (auto-sorter, slower, more bandwith)
# TODO: test on windows as well.
# TODO: implement the new API (socket API)
# NOTE: use easyGUI for a nice window when choosing proxy path


@func_logger
def main():
    inputObj = GetUserInput()
    
    proxy_type: ProxyType = inputObj.get_proxy_type()
    proxies_list: list[bytes] = inputObj.get_proxies()
    num_threads: int = inputObj.get_threads()
    checker_type: CheckerType = inputObj.get_checker_type()

    CheckerObj = ProxyChecker(proxies_list, num_threads, proxy_type)
    CheckerObj.start_checker()
    
if __name__ == "__main__":
    main()