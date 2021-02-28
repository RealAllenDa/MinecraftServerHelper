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
from MCSH.consts import MCSH_version, LOGGING_COLORS, TUI_COLORS
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
    _choose_colours()
    # Computer evaluation


def _choose_colours():
    print("Welcome to Minecraft Server Helper (MCSH) ver.{}!\n".format(MCSH_version) +
          "Now, the setup program will print a few ANSI characters.\n"
          "Choose yes and enable the console colouring "
          "if you see characters in different colours.\n"
          "Choose no and disable the console colouring "
          "if you see characters with a '\\033..m' and no colours.")
    for i in LOGGING_COLORS:
        print("Testing Logging_Colors: {}This line should be the color of {}.\033[0m".format(LOGGING_COLORS[i], i))
    for i in TUI_COLORS:
        print("Testing TUI_Colors: {}This line should be the color of {}.\033[0m".format(TUI_COLORS[i], i))
    seen_colours = input("Do you see the colours described above? [y/n]: ")
    from MCSH.consts import config_instance
    if seen_colours.lower() == "y":
        log(MODULE_NAME, "INFO", "Successfully enabled console colouring.")
        config_instance.program_config["color_enabled"] = True
        config_instance.update_config()
    else:
        log(MODULE_NAME, "INFO", "Successfully disabled console colouring.", True)
        config_instance.program_config["color_enabled"] = False
        config_instance.update_config()


def _evaluate_computer():
    log(MODULE_NAME, "DEBUG", "[Step 3/4] Evaluating computer...")
