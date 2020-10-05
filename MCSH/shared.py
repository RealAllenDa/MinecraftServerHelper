"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module Name: MCSH.shared -> from MCSH.shared import *
 Module Description:
    A module for all the shared functions.
    Including Logging, Downloading, etc.
"""
import MCSH.config
class Logger:
    def __init__(self):
        pass
    def log(self, logModule, logSeverity, logText):
        """
        The logging function for MCSH.
        The color varies depending on the severity of the log:
            CRITICAL - White, on a red background
            ERROR - Red, on the default background
            WARNING - Yellow, on the default background
            INFO - Default, on the default background
            DEBUG - Green, on the default background
        Also, the severity of the log represents the required operations:
            CRITICAL - It indicates the program encountered
                        severe AND unrecoverable programs (e.g. Exceptions uncaught).
                       After this error being thrown,
                        the program will exit or crash.
            ERROR - It indicates that the program encountered
                     severe but recoverable or normal errors.
                    After this error being thrown,
                     the program will ask for user operations AND attention.
            WARNING - It indicates that a specific part of the program
                       can't be properly done or couldn't load.
                      After this warning,
                       the program will ask for user attention.
            INFO - It is an info about what the program is currently doing.
            DEBUG - It is usually the verbose version of the INFO.
                    It contains a lot of useful information that
                     a programmer or debugger would like.
                    Normal users are NOT advised to enable debugging mode.
        """

    def throw(self):
        pass
config_instance = MCSH.config.Config()