from .setup.requirements import install_requirements
from .setup.ask_details import create_termuxconfig, startdb   



# install dependencies
install_requirements()


# check if previous class exists or not
try:
	from termuxconfig import Termuxconfig
except (ImportError, ModuleNotFoundError):
	create_termuxconfig()
	from termuxconfig import Termuxconfig     

startdb()




