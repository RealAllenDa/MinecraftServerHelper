"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module Name: MCSH.config
 Module Description:
    A module that stores all the configuration needed for MCSH.
"""
import argparse, json
class Config:
    def __init__(self):
        """
        Initialize for the config.
        """
        # Version of MCSH
        self.version = "MCSH v0.0.1-InEDev"
        # Initialize locales
        self.locale = "zh_cn"
        self.locale_file = open("MCSH/locale/{}.json".format(self.locale), encoding="utf-8")
        self.locale_dict = json.loads(self.locale_file.read())
        self.locale_file.close()
        # Detect the version of the locale file.
        # If it's outdated, raise an exception.
        if self.locale_dict["version"] != self.version:
            raise Exception("ERROR: Locale file version didn't match with the program version.\n"
                            "Program version is {}, but locale file version is {}.\n"
                            "This could be triggered by an improper installation. "
                            "Please reinstall MCSH.".format(self.version, self.locale_dict["version"]))
        # Initialize parsers
        self.parser = argparse.ArgumentParser(description=self.locale_dict["parser"]["description"],
                                              epilog=self.locale_dict["parser"]["epilog"])
        self.parser_args = None
        self.operations = self.parser.add_mutually_exclusive_group(required=True)
    def parser_init(self):
        self.parser.add_argument("-v", "--version", action="version", version=self.version)
        self.operations.add_argument("--install", action="store_true", default=False, help=self.locale_dict["parser"]["helps"]["install"])
        self.operations.add_argument("--remove", nargs="+", metavar="servername", help=self.locale_dict["parser"]["helps"]["remove"])
        self.operations.add_argument("--reinstall", nargs=1, metavar="servername", help=self.locale_dict["parser"]["helps"]["reinstall"])
        self.operations.add_argument("--autoupdate", action="store_true", help=self.locale_dict["parser"]["helps"]["autoupdate"])
        self.operations.add_argument("--upgrade", action="store_true", help=self.locale_dict["parser"]["helps"]["upgrade"])
        self.operations.add_argument("--download", action="store_true", help=self.locale_dict["parser"]["helps"]["download"])
        self.operations.add_argument("--list", action="store_true", help=self.locale_dict["parser"]["helps"]["list"])
        self.operations.add_argument("--repolist", action="store_true", help=self.locale_dict["parser"]["helps"]["repolist"])
        self.operations.add_argument("--reposearch", nargs=1, metavar="servername", help=self.locale_dict["parser"]["helps"]["reposearch"])
        self.operations.add_argument("--reposhow", nargs=1, metavar="servername", help=self.locale_dict["parser"]["helps"]["reposhow"])
    def parser_parse(self):
        self.parser_args = self.parser.parse_args()
        print(self.parser_args)