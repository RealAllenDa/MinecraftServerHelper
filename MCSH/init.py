"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module name: MCSH.init
 Module Revision: 0.0.1-16
 Module Description:
    Handles all initializing things.
"""
import os

from MCSH.config import Config
from MCSH.first_time_setup import startup_guide
from MCSH.logging import initialize_logger

config_instance = None
computer_info_instance = None
first_time_setup = False


def init():
    """
    Initializes all modules.
    """
    global config_instance, computer_info_instance, first_time_setup
    # If it's first time to run this program
    if not os.path.exists("./MCSH/logs"):
        first_time_setup = True
    # Logger Module
    initialize_logger()
    # Config Module
    config_instance = Config()
    config_instance.parser_parse()
    # Start first-time setup routine (If first_time_setup is True)
    if first_time_setup:
        startup_guide()
