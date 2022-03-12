import os




def __list_all_plugins():
	""" load plugins """
	from os.path import dirname, basename, isfile
	import glob

	mod_paths = glob.glob(dirname(__file__) + "/*.py")
	all_plugins = [
		basename(f)[:-3]
		for f in mod_paths
		if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
	]
	return all_plugins




PLUGINS = sorted(__list_all_plugins())
__all__ = PLUGINS + ["PLUGINS"]

