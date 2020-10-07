"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module Name: MCSH.config
 Module Description:
    A module that stores all the configuration needed for MCSH.
    Main argparse module for MCSH.
"""
import argparse
import json
import sys

from MCSH.logging import log

MCSH_version = "MCSH v0.0.1-InEDev"


class Config:
    def __init__(self):
        """
        Initialize for the config.
        """
        # Initialize config
        try:
            self.program_config_file = open("MCSH/config/MCSH.json")
            self.program_config = json.loads(self.program_config_file.read())
            self.program_config_file.close()
        except:
            log("initialize_config", "WARNING", "The file {file_name} ({file_path}) is missing or corrupted. "
                                                "Trying to retrieve a new one from the repo...".format(
                **{"file_name": "MCSH.json", "file_path": "MCSH/config/MCSH.json"}))
        # Initialize locales
        self.locale = self.program_config["locale"]
        try:
            self.locale_file = open("MCSH/locale/{}.json".format(self.locale), encoding="utf-8")
            self.locale_dict = json.loads(self.locale_file.read())
            self.locale_file.close()
        except:
            log("initialize_locale", "FATAL", "FATAL ERROR during pre-initialization:\n"
                                              "Unable to load locale file.\n"
                                              "This could be triggered by an improper installation and/or upgrade.\n"
                                              "Please reinstall MCSH.")
            sys.exit(2)
        # Detect the version of the locale file.
        # If it's outdated, raise a fatal error.
        if self.locale_dict["version"] != MCSH_version:
            log("initialize_locale", "FATAL", self.locale_dict["exceptions"]["fatal_lang_version_mismatch"].format(
                **{"program": MCSH_version,
                   "locale": self.locale_dict["version"]}))
            sys.exit(2)
        # Initialize parsers
        self.parser = argparse.ArgumentParser(description=self.locale_dict["parser"]["description"],
                                              epilog=self.locale_dict["parser"]["epilog"])
        self.parser_args = None
        self.operations = self.parser.add_mutually_exclusive_group(required=True)

    def parser_init(self):
        """
        Set the commands for the parser.
        """
        self.parser.add_argument("-v", "--version", action="version", version=self.version)
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
        self.operations.add_argument("--list", action="store_true", help=self.locale_dict["parser"]["helps"]["list"])
        self.operations.add_argument("--repolist", action="store_true",
                                     help=self.locale_dict["parser"]["helps"]["repolist"])
        self.operations.add_argument("--reposearch", nargs=1, metavar="ServerName",
                                     help=self.locale_dict["parser"]["helps"]["reposearch"])
        self.operations.add_argument("--reposhow", nargs=1, metavar="ServerName",
                                     help=self.locale_dict["parser"]["helps"]["reposhow"])

    def parser_parse(self):
        """
        Parse the args the user had entered.
        """
        self.parser_args = self.parser.parse_args()
        print(self.parser_args)
