################################################
# Author:  alimuhammadsecured
# Linkedin: https://www.linkedin.com/in/muhammadalisecured/
# Blogs/Bug Bounty Writeups: https://medium.com/@alimuhammadsecured
################################################


from src.templates import*
from src.ProxyChecker import ProxyChecker
from src.loggerClass import func_logger
from src.getUserInput import GetUserInput
from src.proxyConfig import ProxyType, CheckerType


# TODO: proxy identifier (auto-sorter, slower, more bandwith)
# TODO: test on windows as well.


@func_logger
def main():
    inputObj = GetUserInput()
    
    proxies_list: list[bytes] = inputObj.get_proxies()
    num_threads: int = inputObj.get_threads()
    
    # NOTE: not used bcs I need to update it to support check types.
    checker_type: CheckerType = inputObj.get_checker_type()

    if checker_type == CheckerType.SOCKET:
        proxy_type: ProxyType = inputObj.get_proxy_type(can_use_sorter=True)
    else:
        proxy_type: ProxyType = inputObj.get_proxy_type(can_use_sorter=False)

    CheckerObj = ProxyChecker(proxies_list, num_threads, proxy_type, checker_type)
    CheckerObj.start_checker()
    
if __name__ == "__main__":
    main()