"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module name: MCSH.first_time_setup
 Module Revision: 0.0.1-18
 Module Description:
    Guides the user through first-time setup routines.
"""
from MCSH.logging import log

MODULE_NAME = "first_time_setup"


def startup_guide():
    """
    The entrance of the startup guide.
    Included parts:
        Language, Check pre.req., Generate config, Evaluate computer.
    """
    log(MODULE_NAME, "DEBUG", "Initializing first-time setup guide...")
    # Pre-requirements check
    _check_pre_requirements()
    # Computer evaluation


def _check_pre_requirements():
    log(MODULE_NAME, "DEBUG", "[Step 1/4] Checking pre-requirements...")


def _evaluate_computer():
    log(MODULE_NAME, "DEBUG", "[Step 3/4] Evaluating computer...")
