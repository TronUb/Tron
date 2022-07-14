from termux.setup.requirements import install_requirements  



# install dependencies
install_requirements()


# check if previous class exists or not
try:
    from termuxconfig import TermuxConfig
except (ImportError, ModuleNotFoundError):
    create_termuxconfig()
    from termuxconfig import TermuxConfig     





