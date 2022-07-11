"""
Gets all the plugin names
"""

import os
import glob
from os.path import dirname, basename, isfile





def __list_all_plugins():
    """ list all plugins (assistant)"""

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_plugins = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return all_plugins




PLUGINS = sorted(__list_all_plugins())
__all__ = PLUGINS + ["PLUGINS"]
