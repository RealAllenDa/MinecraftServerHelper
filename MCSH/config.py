"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module Name: MCSH.config
 Module Revision: 0.0.1-18
 Module Description:
    A module that stores all the configuration needed for MCSH.
    Main argparse module for MCSH.
"""
import argparse
import json
import os
import traceback

from MCSH.consts import MCSH_version
from MCSH.debug import debugging_check, debugging_parse
from MCSH.get_computer_info import ComputerInfo
from MCSH.logging import log, crash

MODULE_NAME = "config"


class Config:
    """
    The main config class for MCSH.
    """

    def __init__(self, flag_first_time_start=False):
        """
        Initialize configurations.
        """
        log(MODULE_NAME, "DEBUG", "Initializing config instance...")
        # Set all variables to none
        self.program_config_file = None
        self.program_config = None
        self.parser = None
        self.parser_args = None
        self.operations = None
        self.parse_sequence = None
        self.execute_command = None
        self.computer_info = None
        self.crash_info = None
        self.debug = False
        self.first_time_start = flag_first_time_start
        # Call functions for initializing.
        self._init_computer_info()
        self._init_debug()
        self._init_program_config()
        log(MODULE_NAME, "DEBUG", "-- Config Summary --\n"
                                  "program_config: {}\n"
                                  "computer_info: {}\n"
                                  "crash_info: {}\n"
                                  "first_time_startup: {}\n"
                                  "DEBUG: {}".format(self.program_config,
                                                     self.computer_info, self.crash_info,
                                                     self.first_time_start, self.debug))
        log(MODULE_NAME, "DEBUG", "Starting parser...")
        self._init_parser()
        self._config_parser()

    def _init_debug(self):
        if debugging_check(suppress_warning=True):
            log(MODULE_NAME, "DEBUG", "WARNING: Debugging features enabled.")
            self.debug = True
            self.crash_info["Debugging"] = True
        else:
            self.crash_info["Debugging"] = False

    def _init_computer_info(self):
        """
        Initialize computer info module.
        """
        log(MODULE_NAME, "DEBUG", "Initializing computer info instance...")
        computer_info_instance = ComputerInfo()
        computer_info_instance.get_computer_info()
        self.computer_info = computer_info_instance.computer_info
        self.crash_info = computer_info_instance.crash_report_system_info

    def _init_program_config(self):
        """
        Read program config json.
        """
        log(MODULE_NAME, "DEBUG", "Reading program config...")
        if self.first_time_start:
            self._generate_config()
        try:
            self.program_config_file = open("MCSH/config/MCSH.json")
            self.program_config = json.loads(self.program_config_file.read())
            self.program_config_file.close()
        except Exception:
            log("initialize_config", "WARNING", "The file {file_name} ({file_path}) is missing or corrupted. "
                                                "Trying to generate a new one...".format(
                **{"file_name": "MCSH.json", "file_path": "MCSH/config/MCSH.json"}))
            self._generate_config()
            self._init_program_config()

    def _generate_config(self):
        # TODO: Update from version to version
        log(MODULE_NAME, "DEBUG", "Generating a new config file...")
        if self.first_time_start:
            try:
                os.mkdir("MCSH/config")
            except Exception:
                crash({
                    "description": "Unable to create config directory.",
                    "exception": "Unable to create config directory.",
                    "computer_info": self.crash_info,
                    "program_traceback": traceback.format_exc()
                })
        config_file_content = {
            "version": "MCSH v0.0.1-InEDev",
            "color_enabled": False
        }
        try:
            with open("MCSH/config/MCSH.json", "w+") as f:
                f.write(json.dumps(config_file_content))
                f.close()
        except Exception:
            crash({
                "description": "Unable to generate config file.",
                "exception": "Unable to generate config file.",
                "computer_info": self.crash_info,
                "program_traceback": traceback.format_exc()
            })

    def update_config(self):
        try:
            with open("MCSH/config/MCSH.json", "w") as f:
                f.write(json.dumps(self.program_config))
                f.close()
        except Exception:
            print("Failed")

    def _init_parser(self):
        """
        Initialize parsers.
        """
        if self.first_time_start:
            log(MODULE_NAME, "DEBUG", "First time startup guide. Parser disabled.")
            return
        # Initialize parsers
        log(MODULE_NAME, "DEBUG", "Initializing parsers...")
        # noinspection PyTypeChecker
        self.parser = argparse.ArgumentParser(add_help=False,
                                              description="A Minecraft Server Helper.",
                                              epilog="NOTE: The MCSH will only execute command by the sequence mentioned above.\n"
                                                     "e.g. mcsh-cli.py --remove --install, MCSH will only execute --install, not --remove.\n"
                                                     "For more detailed help, see README.md in the root folder.",
                                              formatter_class=argparse.RawTextHelpFormatter)
        self.parser_args = None
        self.operations = self.parser.add_argument_group(title="All MCSH Commands")
        self.debug_operations = self.parser.add_argument_group(title="Debugging Commands")
        self.parse_sequence = ["install", "remove", "reinstall", "autoupdate", "upgrade", "download",
                               "repolist", "reposearch", "reposhow"]
        self.execute_command = None

    def _config_parser(self):
        """
        Config commands for the parser.
        """
        if self.first_time_start:
            return
        log(MODULE_NAME, "DEBUG", "Adding parser commands...")
        self.operations.add_argument("--version", action="version", version=MCSH_version,
                                     help="Display the version of MCSH.")
        self.operations.add_argument("--help", action="help",
                                     help="Show this help message.")
        self.operations.add_argument("--list", action="store_true",
                                     help="List all installed server(s).")
        self.operations.add_argument("--install", action="store_true", default=False,
                                     help="Install a server.")
        self.operations.add_argument("--remove", nargs="+", metavar="ServerName",
                                     help="Remove server(s).")
        self.operations.add_argument("--reinstall", nargs=1, metavar="ServerName",
                                     help="Reinstall a server.")
        self.operations.add_argument("--autoupdate", action="store_true",
                                     help="Update all server(s) in the list.")
        self.operations.add_argument("--upgrade", action="store_true",
                                     help="Upgrade all server(s) to current version, including MCSH.\n"
                                          "WARNING: Under very early development, strongly unrecommended.")
        self.operations.add_argument("--download", action="store_true",
                                     help="Download a specified server program.")
        self.operations.add_argument("--repolist", action="store_true",
                                     help="List all server(s) in the repository.")
        self.operations.add_argument("--reposearch", nargs=1, metavar="ServerName",
                                     help="Search for server(s) in the repository.")
        self.operations.add_argument("--reposhow", nargs=1, metavar="ServerName",
                                     help="Show the specific server detail in the repository.")
        # Commands used JUST FOR DEBUGGING
        self.debug_operations.add_argument("--debugging-crash",
                                           action="store_true",
                                           help=("Crash the program."
                                                 if self.debug
                                                 else argparse.SUPPRESS))
        self.debug_operations.add_argument("--debugging-enable",
                                           action="store_true",
                                           help=("Enable debugging features."
                                                 if self.debug
                                                 else argparse.SUPPRESS))
        self.debug_operations.add_argument("--debugging-disable",
                                           action="store_true",
                                           help=("Disable debugging features."
                                                 if self.debug
                                                 else argparse.SUPPRESS))
    def parser_parse(self):
        """
        Parse the args the user had entered.
        """
        log(MODULE_NAME, "DEBUG", "Parsing arguments...")
        self.parser_args = self.parser.parse_args()
        # DEBUGGING ARGUMENTS
        debug_args_selected = debugging_parse(self.parser_args)
        # Normal Parsing
        for i in self.parse_sequence:
            if eval("self.parser_args." + i) is True:
                self.execute_command = i
                break
            elif eval("self.parser_args." + i) is not None and eval("self.parser_args." + i) is not False:
                self.execute_command = i + "({})".format(eval("self.parser_args." + i))
                break
        if self.execute_command is None and debug_args_selected is False:
            log(MODULE_NAME, "ERROR", "No command specified.")
            self.parser.print_usage()
        log(MODULE_NAME, "DEBUG", "-- Parser Summary --\n"
                                  "parser_args: {}\n"
                                  "execute_command: {}\n"
                                  "parse_sequence: {}".format(self.parser_args, self.execute_command, self.parse_sequence))