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
from MCSH.config import Config
from MCSH.get_computer_info import ComputerInfo
from MCSH.logging import initialize_logger

config_instance = None
computer_info_instance = None


def init():
    config_instance.parser_init()
    config_instance.parser_parse()
