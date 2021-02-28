"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module Name: MCSH.consts
 Module Revision: 0.0.1-18
 Module Description:
    A module that handles all the debugging things.
"""
import os

from MCSH.logging import log, crash

MODULE_NAME = "debug"


def debugging_parse(parser_arguments):
    log(MODULE_NAME, "DEBUG", "Parsing debug arguments...")
    from MCSH.consts import config_instance
    if parser_arguments.debugging_crash:
        debugging_crash(config_instance.crash_info)
    elif parser_arguments.debugging_enable:
        debugging_enable()
    elif parser_arguments.debugging_disable:
        debugging_disable()
    else:
        return False


def debugging_enable():
    if debugging_check(suppress_warning=True):
        log(MODULE_NAME, "ERROR", "Debugging already enabled!")
    else:
        with open("MCSH/config/debug.enabled", "w+") as f:
            f.write("enabled")
            f.close()
        log(MODULE_NAME, "INFO", "Successfully enabled debugging!")


def debugging_check(suppress_warning=False):
    if os.path.exists("MCSH/config/debug.enabled"):
        log(MODULE_NAME, "DEBUG", "Debugging file exists. Continuing...")
        return True
    else:
        if not suppress_warning:
            log(MODULE_NAME, "WARNING", "You're trying to execute a command that could cause bad things "
                                        "(including crashing, deleting all the files, etc.)\n"
                                        "This command is meant for debugging only, and it should NOT be executed "
                                        "by an end user.\n"
                                        "If you insist on executing this command, enable the debugging features by "
                                        "typing 'mcsh-cli.py --debugging-enable' before continuing.")
        return False


def debugging_crash(crash_info):
    if not debugging_check():
        return
    else:
        log(MODULE_NAME + "_crash", "DEBUG", "Crashing...")
        crash({
            "description": "Manually triggered crash",
            "exception": "UNKNOWN (Manually triggered crash)",
            "computer_info": crash_info
        })


def debugging_disable():
    try:
        os.remove("MCSH/config/debug.enabled")
        log(MODULE_NAME, "INFO", "Successfully removed debugging file!")
    except:
        log(MODULE_NAME, "FATAL", "Failed to remove debugging file. (Is the file already removed?)\n"
                                  "Please go to MCSH/config and remove the debug.enabled file "
                                  "by yourself.")
