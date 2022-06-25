from .requirements_installer import install_requirements
from .accept_details import create_termuxconfig




install_requirements()

try:
	from termuxconfig import Termuxconfig
except (ImportError, ModuleNotFoundError):
	create_termuxconfig()
	from termuxconfig import Termuxconfig





