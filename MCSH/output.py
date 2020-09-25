"""
 *********************************
 MCSH - A Minecraft Server Helper.
 Coded & tested by Allen Da 2020.
 Licensed under MIT.
 *********************************
 File Description:
    This is the shared function for output.
    It handles the logging also.
 File functions:
    log - logging function for the program.
"""
import time
def log(logModules, logLevel, logDetails):
    """
    A function to handle logs.
    The color varies depending on the level of the log:
        CRITICAL - White, on a red background
        ERROR - Red, on the default background
        WARNING - Yellow, on the default background
        INFO - Default, on the default background
        DEBUG - Green, on the default background
    Also, it indicates the severity of the log:
        CRITICAL - It indicates that the program encountered
                    severe AND unrecoverable problems (e.g. Exceptions in code).
                   Usually after this error being thrown,
                    the program will exit / crash.

        ERROR - It indicates that the program encountered
                 severe but recoverable or normal errors.
                Usually after this error being thrown,
                 the program will ask for user operations AND user attention.

        WARNING - It indicates that a specific part of the program
                   can't be properly complete and/or the program
                   encountered a very low level error.
                  Usually after this warning,
                   the program will ask for user attention.

        INFO - It's just a log about what the program is doing.
               There's nothing bad about it.

        DEBUG - It's usually the verbose version of the INFO.
                It contains a lot of useful information that
                 a programmer / debugger would like to watch.
                Normal users are not advised to open debugging mode.
    """
    pass