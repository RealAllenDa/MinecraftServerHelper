"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module name: MCSH.init
 Module Revision: 0.0.1-18
 Module Description:
    Handles all initializing things.
"""
import os

from MCSH.config import Config
from MCSH.consts import insert_cfg_instance
from MCSH.first_time_setup import startup_guide
from MCSH.logging import initialize_logger, log

config_instance = None
MODULE_NAME = "init"


def init():
    """
    Initializes all modules.
    """
    # Logger Module
    global config_instance
    initialize_logger()
    log(MODULE_NAME, "DEBUG", "Pre-initializing...")
    # If it's first time to run this program
    if not os.path.exists("./MCSH/logs") or not os.path.exists("./MCSH/config/MCSH.json"):
        log(MODULE_NAME, "DEBUG", "Detected first time to use this program -- starting up guide...")
        config_instance = Config(flag_first_time_start=True)
        log(MODULE_NAME, "DEBUG", "Inserting CFG instance to INSTANCES...")
        insert_cfg_instance(config_instance)
        startup_guide()
    else:
        # Config Module
        log(MODULE_NAME, "DEBUG", "Initializing config module...")
        config_instance = Config()
        log(MODULE_NAME, "DEBUG", "Inserting CFG instance to INSTANCES...")
        insert_cfg_instance(config_instance)
        log(MODULE_NAME, "DEBUG", "Config initialised -- parsing arguments...")
        config_instance.parser_parse()
