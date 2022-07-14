from termux.setup.install import install_requirements  
from termux.setup.getconfig import create_termuxconfig


# install dependencies
install_requirements()


# check if previous class exists or not
try:
    from termuxconfig import TermuxConfig
except (ImportError, ModuleNotFoundError):
    create_termuxconfig()
    from termuxconfig import TermuxConfig     





