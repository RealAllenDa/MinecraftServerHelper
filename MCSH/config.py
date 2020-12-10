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
import traceback

from MCSH.consts import MCSH_version, DEBUG
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
        self.locale = None
        self.locale_file = None
        self.locale_dict = None
        self.parser = None
        self.parser_args = None
        self.operations = None
        self.parse_sequence = None
        self.execute_command = None
        self.computer_info = None
        self.crash_info = None
        # Call functions for initializing.
        self._init_computer_info()
        if not flag_first_time_start:
            log(MODULE_NAME, "DEBUG", "Not starting the first time -- initializing other things...")
            self._init_program_config()
            self._init_locale()
            self._init_parser()
            self._config_parser()
        log(MODULE_NAME, "DEBUG", "-- Config Summary --\n"
                                  "program_config: {}\n"
                                  "locale: {} ({})\n"
                                  "computer_info: {}\n"
                                  "crash_info: {}\n"
                                  "first_time_startup: {}\n"
                                  "DEBUG: {}".format(self.program_config, self.locale, self.locale_file,
                                                                  self.computer_info, self.crash_info,
                                                                  flag_first_time_start, DEBUG))

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
        try:
            self.program_config_file = open("MCSH/config/MCSH.json")
            self.program_config = json.loads(self.program_config_file.read())
            self.program_config_file.close()
        except Exception as e:
            log("initialize_config", "WARNING", "The file {file_name} ({file_path}) is missing or corrupted. "
                                                "Trying to generate a new one...".format(
                **{"file_name": "MCSH.json", "file_path": "MCSH/config/MCSH.json"}))
            self._generate_config()
            self._init_program_config()
    def _init_locale(self):
        """
        Read program locale config.
        """
        log(MODULE_NAME, "DEBUG", "Reading locale config...")
        self.locale = self.program_config["locale"]
        try:
            self.locale_file = open("MCSH/locale/{}.json".format(self.locale), encoding="utf-8")
            self.locale_dict = json.loads(self.locale_file.read())
            self.locale_file.close()
        except Exception as e:
            log("initialize_locale", "FATAL", "Unable to load locale file.\n"
                                              "This could be triggered by an improper installation and/or upgrade.\n"
                                              "Please reinstall MCSH.")
            crash({
                "description": "Unable to load locale file.",
                "exception": "Unable to load locale file. "
                             "Locale file had been corrupted. "
                             "Please reinstall MCSH.",
                "computer_info": self.crash_info,
                "program_traceback": traceback.format_exc()
            })
        # Detect the version of the locale file.
        # If it's outdated, raise a fatal error.
        log(MODULE_NAME, "DEBUG", "Checking locale file date...")
        if self.locale_dict["version"] != MCSH_version:
            log("initialize_locale", "FATAL", self.locale_dict["exceptions"]["fatal_lang_version_mismatch"].format(
                **{"program": MCSH_version,
                   "locale": self.locale_dict["version"]}))
            crash({
                "description": "Unable to load locale file.",
                "exception": "Unable to load locale file. "
                             "Locale file is outdated. "
                             "(reported_version={}, mcsh_version={})".format(
                    self.locale_dict["version"],
                    MCSH_version
                ),
                "computer_info": self.crash_info
            })
    def _generate_config(self):
        # TODO: Update from version to version
        log(MODULE_NAME, "DEBUG", "Generating a new config file...")
        config_file_content = {
            "version": "MCSH v0.0.1-InEDev",
            "locale": "en_us"
        }
        try:
            with open("MCSH/config/MCSH.json", "w+") as f:
                f.write(json.dumps(config_file_content))
                f.close()
        except Exception as e:
            crash({
                "description": "Unable to generate config file.",
                "exception": "Unable to generate config file.",
                "computer_info": self.crash_info,
                "program_traceback": traceback.format_exc()
            })

    def _init_parser(self):
        """
        Initialize parsers.
        """
        # Initialize parsers
        log(MODULE_NAME, "DEBUG", "Initializing parsers...")
        # noinspection PyTypeChecker
        self.parser = argparse.ArgumentParser(add_help=False,
                                              description=self.locale_dict["parser"]["description"],
                                              epilog=self.locale_dict["parser"]["epilog"],
                                              formatter_class=argparse.RawTextHelpFormatter)
        self.parser_args = None
        self.operations = self.parser.add_argument_group(title=self.locale_dict["parser"]["operations_title"])
        self.parse_sequence = ["install", "remove", "reinstall", "autoupdate", "upgrade", "download",
                               "repolist", "reposearch", "reposhow"]
        self.execute_command = None

    def _config_parser(self):
        """
        Config commands for the parser.
        """
        log(MODULE_NAME, "DEBUG", "Adding parser commands...")
        self.operations.add_argument("--version", action="version", version=MCSH_version,
                                     help=self.locale_dict["parser"]["helps"]["version"])
        self.operations.add_argument("--help", action="help",
                                     help=self.locale_dict["parser"]["helps"]["help"])
        self.operations.add_argument("--list", action="store_true",
                                     help=self.locale_dict["parser"]["helps"]["list"])
        self.operations.add_argument("--install", action="store_true", default=False,
                                     help=self.locale_dict["parser"]["helps"]["install"])
        self.operations.add_argument("--remove", nargs="+", metavar="ServerName",
                                     help=self.locale_dict["parser"]["helps"]["remove"])
        self.operations.add_argument("--reinstall", nargs=1, metavar="ServerName",
                                     help=self.locale_dict["parser"]["helps"]["reinstall"])
        self.operations.add_argument("--autoupdate", action="store_true",
                                     help=self.locale_dict["parser"]["helps"]["autoupdate"])
        self.operations.add_argument("--upgrade", action="store_true",
                                     help=self.locale_dict["parser"]["helps"]["upgrade"])
        self.operations.add_argument("--download", action="store_true",
                                     help=self.locale_dict["parser"]["helps"]["download"])
        self.operations.add_argument("--repolist", action="store_true",
                                     help=self.locale_dict["parser"]["helps"]["repolist"])
        self.operations.add_argument("--reposearch", nargs=1, metavar="ServerName",
                                     help=self.locale_dict["parser"]["helps"]["reposearch"])
        self.operations.add_argument("--reposhow", nargs=1, metavar="ServerName",
                                     help=self.locale_dict["parser"]["helps"]["reposhow"])
        # Commands used JUST FOR DEBUGGING
        self.operations.add_argument("--debugging-crash", action="store_true",
                                     help=argparse.SUPPRESS)

    def parser_parse(self):
        """
        Parse the args the user had entered.
        """
        debug_args_selected = False
        log(MODULE_NAME, "DEBUG", "Parsing arguments...")
        self.parser_args = self.parser.parse_args()
        # DEBUGGING ARGUMENTS
        if self.parser_args.debugging_crash:
            debug_args_selected = True
            # TODO: Move to another debugging place
            crash({
                "description": "Manually triggered crash",
                "exception": "UNKNOWN (Manually triggered crash)",
                "computer_info": self.crash_info
            })
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
            self.parser.print_help()
        log(MODULE_NAME, "DEBUG", "-- Parser Summary --\n"
                                  "parser_args: {}\n"
                                  "execute_command: {}\n"
                                  "parse_sequence: {}".format(self.parser_args, self.execute_command, self.parse_sequence))
        print(self.execute_command)
