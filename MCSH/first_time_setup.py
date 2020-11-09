"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module name: MCSH.first_time_setup
 Module Revision: 0.0.1-17
 Module Description:
    Guides the user through first-time setup routines.
"""
from MCSH.logging import log

def startup_guide():
    """
    The entrance of the startup guide.
    Included parts:
        Check pre.req., Generate config, Evaluate computer.
    """
    log("first_time_setup", "DEBUG", "Initializing first-time setup guide...")
    print("\033[")