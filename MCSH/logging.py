"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module Name: MCSH.logging
 Module Revision: 0.0.1-16
 Module Description:
    A module for all the shared functions.
    Including Logging, Downloading, etc.
"""
import os
import tarfile
import time

from MCSH.crash_report import generate_crash_report

logging_file_name = ""


# The logger in-program.
def log(log_module, log_severity, log_text):
    """
    The logging function for MCSH.
    log_severity: FATAL, ERROR, WARNING, INFO, DEBUG
    """
    COLORS = {
        "FATAL": "\033[1;37;41m",
        "ERROR": "\033[31m",
        "WARNING": "\033[33m",
        "INFO": "",
        "DEBUG": "\033[32m"
    }
    try:
        log_color = COLORS[log_severity]
    except:
        log_color = ""
    log_text_lines = log_text.split("\n")
    for log_text in log_text_lines:
        log_formatted_text = "[{time}-{process_time}] [{log_module}/{log_severity}]: {log}".format(**{
            "time": time.strftime("%H:%M:%S", time.localtime()),
            "process_time": time.process_time(),
            "log_module": log_module,
            "log_severity": log_severity,
            "log": log_text
        })
        log_formatted_output = "{color}{log}\033[0m".format(**{
            "color": log_color,
            "log": log_formatted_text
        })
        if logging_file_name != "":
            try:
                with open(logging_file_name, "a+") as f:
                    f.write(log_formatted_text + "\n")
                f.close()
            except:
                pass
        print(log_formatted_output)


def crash(crash_info):
    log("crash_watchdog", "FATAL", "MCSH had crashed!\n"
                                   "For detailed information, "
                                   "see crash reports under ./MCSH/crash_report folder.")
    generate_crash_report(crash_info["description"],
                          crash_info["exception"],
                          crash_info["computer_info"])

def initialize_logger():
    """
    Initialize the logging file handler.
    Default log output directory: ./MCSH/logs
    Default log threshold: 10 logs
    """
    path = "./MCSH/logs"
    # First-time initialization
    if not os.path.exists(path):
        os.mkdir(path)
    # Auto-packing logs
    if len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))]) >= 2:
        try:
            tar = tarfile.open("./MCSH/logs/pack.tar.gz", "w:gz")
            for root, directory, files in os.walk("./MCSH/logs"):
                print(root, directory, files)
                for file in files:
                    if file != "pack.tar.gz":
                        file_path = os.path.join(root, file)
                        print(file_path)
                        tar.add(file_path, arcname=file)
                        os.remove(file_path)
            tar.close()
        except:
            print("Failed to pack logs. Please delete logs manually under ./MCSH/logs.")
    # Set the logging file name
    global logging_file_name
    logging_file_name = "{}/{}.log".format(path, time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    try:
        with open(logging_file_name, "w+") as f:
            f.write("Logger initialized -- Start logging...\n")
            f.close()
    except:
        print("WARNING: Can't write a log to the file. Logging function will be disabled.")
        logging_file_name = ""
