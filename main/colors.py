""" All colors """



class Colors:
    # colours
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    # decorators
    bold = "\u001b[1m"
    underline = "\u001b[0m\u001b[4m"
    block = "\u001b[0m\u001b[7m"

    # reset
    reset = "\u001b[0m"

    # move cursor
    def cursor_left(digits: int=0):
        return "\u001b[{}D".format(digits) 

    def cursor_right(digits: int=0):
        return "\u001b[{}C".format(digits) 

    def cursor_up(digits: int=0):
        return "\u001b[{}A".format(digits) 

    def cursor_down(digits: int=0):
        return "\u001b[{}B".format(digits) 


