"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module Name: MCSH.consts
 Module Revision: 0.0.1-18
 Module Description:
    A module that stores all globally used variables.
"""
DEBUG = True
MCSH_version = "MCSH v0.0.1-InEDev"
CRASH_REPORT_FORMAT = '''---- MCSH Crash Report ----
Time: {time}
Process Time: {process_time}
Description: {description}

{detailed_exception}

Program Traceback:
{program_traceback}

-- System Details --
Details:
{computer_crash_info}
'''
LOGGING_COLORS = {
    "FATAL": "\033[1;37;41m",
    "ERROR": "\033[31m",
    "WARNING": "\033[33m",
    "INFO": "",
    "DEBUG": "\033[32m"
}
LOCALES_AVAIL = [
    "中文（zh-cn）",
    "English (en-us)"
]
config_instance = None


def insert_cfg_instance(instance_object):
    global config_instance
    try:
        config_instance = instance_object
    except:
        print("/// [CONSTS] ERROR: Failed to assign instance to the dictionary.")
