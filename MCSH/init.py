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


def init():
    """
    Initializes all modules.
    """
    global config_instance, computer_info_instance, first_time_setup
    # Logger Module
    initialize_logger()
    # If it's first time to run this program
    if not os.path.exists("./MCSH/logs") or not os.path.exists("./MCSH/config/MCSH.json"):
        config_instance = Config(flag_first_time_start=True)
        startup_guide()
    else:
        # Config Module
        config_instance = Config()
        config_instance.parser_parse()
