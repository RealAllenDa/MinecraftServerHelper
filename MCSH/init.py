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
from MCSH.shared import *
def init():
    config_instance.parser_init()
    config_instance.parser_parse()