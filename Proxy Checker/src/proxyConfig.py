import json

class ProxyType:
    SOCKS5: str = "socks5"
    SOCKS4: str = "socks4"
    HTTP_HTTPS: str = "http"
    

class CheckerType:
    WEBSITE: str = "website"
    SOCKET: str = "socket"

class ProxyResources(object):
    '''
        Loads the config file, the config file will probably be tweaked
        in the future.
    
    '''
    def __init__(self) -> None:
        self.cfg_name = "ProgramResources/generic.json"
    def load_cfg(self):
        return json.load(open(self.cfg_name))