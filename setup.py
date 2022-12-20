import socket



hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
localhost_hostname = "localhost"
localhost_ip_address = "127.0.0.1"
is_localhost = (hostname==localhost_hostname) and (ip_address==localhost_ip_address) 



class TempConfig:
    pass


if not is_localhost:
    os.system("python -m main")
    exit(0)



import os
import platform
import subprocess
import pkg_resources




class Tools:
    device = platform.uname()[0].lower()
    is_linux = (device=="linux")
    is_windows = (device=="windows")

    def check_command(self, args: list):
        return (subprocess.run(
            args,
            stdout=subprocess.PIPE,
            shell=True
        )).stdout.decode()


    def requirements(self):
        with open("requirements.txt", "r") as f:
            return [x for x in f.read().split("\n") if x not in ("\n", "")]


    def check_requirements(self):
        print("Checking Packages:\n\n")
        for pkg in self.requirements():
            try:
                pkg_resources.require([pkg])
            except pkg_resources.DistributionNotFound as e:
                print(f"Since {e.req} is not Installed, Installing {e.req}")
                os.system(f"pip3 install {e.req}")


tools = Tools()

tools.check_requirements()
if tools.is_windows:
    # install ffmpeg

    # permission needed in windows
    os.system('Set-ExecutionPolicy RemoteSigned -Scope CurrentUser')
    # install scoop for installing scoop & other packages
    os.system('Invoke-Expression "& {$(Invoke-RestMethod get.scoop.sh)} -RunAsAdmin"')
    # install ffmpeg through scoop
    os.system('scoop install ffmpeg')

elif tools.is_linux:
    # install ffmpeg

    os.system('apt install ffmpeg')

else:
    print('\nUnknown device, Existing . . .')
    exit(0)


# variable counter
count = 1

# check if the user config file exists
if os.path.exists("config.text"):
    print("config.text file exists: Yes\n\n")
    with open("config.text") as f:
        content = [x for x in f.read().split("\n") if x not in ("\n", "")]

    # set text file config values
    print("Setting configuration values.\n\n")
    for x in content:
        data = x.split("=")
        file_value = data[1]
        if data[1].isdigit():
            file_value = int(data[1])

        setattr(TempConfig, data[0], file_value)
        print(f"[{count}] Added config = {data[0]} with value = {file_value}\n")
        count += 1
    os.system("python -m main")
    exit(0)
else:
    print("config.text file doesn't exist, existing. . .")
    exit(0)
