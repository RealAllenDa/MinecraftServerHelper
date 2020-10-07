"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module name: MCSH.init
 Module Description:
    Handles all initializing things.
"""
import os

from MCSH.config import Config
from MCSH.first_time_setup import startup_guide
from MCSH.get_computer_info import ComputerInfo
from MCSH.logging import initialize_logger

config_instance = None
computer_info_instance = None
first_time_setup = False


def init():
    config_instance.parser_init()
    config_instance.parser_parse()
    # Start first-time setup routine (If first_time_setup is True)
    if first_time_setup:
        startup_guide()
