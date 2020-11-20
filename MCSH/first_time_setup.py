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
from MCSH.consts import config_instance

def startup_guide():
    """
    The entrance of the startup guide.
    Included parts:
        Language, Check pre.req., Generate config, Evaluate computer.
    """
    log("first_time_setup", "DEBUG", "Initializing first-time setup guide...")
    log("first_time_setup", "DEBUG", "[Step 1/4] Generating general config file...")
    print(config_instance)
    # Pre-requirements check
    pass
    # Computer evaluation
def _check_pre_requirements():
    log("first_time_setup", "DEBUG", "[Step 2/4] Checking pre-requirements...")
def _evaluate_computer():
    log("first_time_setup", "DEBUG", "[Step 3/4] Evaluating computer...")