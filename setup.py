import socket



hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
localhost_hostname = "localhost"
localhost_ip_address = "127.0.0.1"
is_localhost = (hostname==localhost_hostname) and (ip_address==localhost_ip_address) 

if not is_localhost:
    os.system("python -m main")
    exit(0)



import os
import platform


class tools:
    device = platform.uname()[0].lower()
    is_linux = (device=="linux")
    is_windows = (device=="windows")
    

    


