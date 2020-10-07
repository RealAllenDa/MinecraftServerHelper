"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module name: MCSH.get_computer_info
 Module Description:
    To get some essential information in order to run 'Performance Tester'.
    Also, when MCSH crashed, can be used for 'System Information' section.
    Because Linux and Windows handles information in very different ways,
    I had to split the way of getting information for different platforms.
 -------------------- MODULE CAUTION --------------------
 WARNING:   This module contains some registry operations in Windows.
            Any improper modifying, corrupting, changing a specific value in this module
            may cause serious errors, probably fatal ones, and not allowing the system to boot.
            Please, don't change anything UNLESS you know what you're doing!

 WARNING:   This module, if not used properly, CAN cause damage to the computer.
"""
# Imports & Pre-check
import fileinput
import hashlib
import platform
import sys
import winreg

import psutil

from MCSH.config import MCSH_version
from MCSH.logging import log


class ComputerInfo:
    def __init__(self):
        """
        computer_info: A detailed computer information.
        files_to_md5: See get_MCSH_checksum function.
        """
        self.crash_report_system_info = {}
        self.computer_info = {}
        self.files_to_md5 = ["MCSH/config.py", "MCSH/get_computer_info.py", "MCSH/init.py", "MCSH/logging.py"]

    def _pre_check_req_python(self):
        """
        Check if the Python version meets requirements. (3.7+)
        If not, raise an Exception.
        """
        if sys.version_info.major >= 3 and sys.version_info.minor >= 7:
            return True
        else:
            return False

    def get_MCSH_version(self):
        """
        Get the MCSH version.
        """
        self.crash_report_system_info["MCSH Version"] = MCSH_version

    def get_MCSH_checksum(self):
        """
        Get the checksum of important files.
        File list:
            - config.py
            - get_computer_info.py
            - init.py
            - logging.py
        """
        self.crash_report_system_info["MCSH File Checksums"] = {}
        try:
            for i in self.files_to_md5:
                with open(i, 'rb') as f:
                    data = f.read()
                    self.crash_report_system_info["MCSH File Checksums"][i] = hashlib.md5(data).hexdigest()
                    f.close()
        except:
            self.crash_report_system_info["MCSH File Checksums"] = "Failed to get checksums for files."

    def get_operating_system(self):
        """
        Get the detailed operating system.
        """
        self.crash_report_system_info["Operating System"] = platform.platform()

    def get_python_version(self):
        """
        Get the Python version.
        """
        self.crash_report_system_info["Python version"] = sys.version

    def get_memory(self):
        """
        Get the memory size.
        """
        mem = psutil.virtual_memory()
        self.crash_report_system_info["Memory"] = "{mem_used} bytes ({mem_used_mb} MB) / " \
                                                  "{mem_total} bytes ({mem_total_mb} MB)".format(**{
            "mem_used": mem.used,
            "mem_used_mb": round(mem.used / 1024 / 1024),
            "mem_total": mem.total,
            "mem_total_mb": round(mem.total / 1024 / 1024)
        })
        self.computer_info["memory_total"] = round(mem.total / 1024 / 1024 / 1024)

    def get_cpu_count(self):
        """
        Get the CPU count.
        """
        self.crash_report_system_info["CPU Count"] = psutil.cpu_count()
        self.computer_info["cpu"] = psutil.cpu_count()

    def get_argv(self):
        """
        Get the arguments (argv).
        """
        try:
            self.crash_report_system_info["Startup Arguments"] = sys.argv[1:]
        except:
            self.crash_report_system_info["Startup Arguments"] = "Unknown"

    def get_cpu_speed(self):
        """
        WARNING: This function contains registry operation in Windows.
        Please, don't change anything unless you know what you're doing!

        Linux: Read speed from /proc/cpuinfo.
        Windows: Read speed from HKLM/HARDWARE/DESCRIPTION/System/CentralProcessor/0
        """
        try:
            if platform.system() in ["Linux"]:
                for line in fileinput.input("/proc/cpuinfo"):
                    if 'Mhz' in line:
                        value = float(line.split(":")[1].strip())
                        speed = round(value / 1024, 1)
                        self.crash_report_system_info["CPU Speed (Ghz)"] = speed
                        self.computer_info["cpu_freq"] = speed
                return True
            elif platform.system() in ["Windows", "Win32"]:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                speed, typeOfElement = winreg.QueryValueEx(key, "~MHz")
                speed = round(float(speed) / 1024, 1)
                self.crash_report_system_info["CPU Speed (Ghz)"] = speed
                self.computer_info["cpu_freq"] = speed
                return True
            else:
                self.crash_report_system_info["CPU Speed (Ghz)"] = "Unable to read"
                self.computer_info["cpu_freq"] = None
                return False
        except:
            self.crash_report_system_info["CPU Speed (Ghz)"] = "Unable to read"
            self.computer_info["cpu_freq"] = None
            return False

    def get_computer_info(self):
        """
        The main function of this module.
        Gets all the information.
        """
        if not self._pre_check_req_python():
            raise Exception("Python version doesn't meet requirements. Requires 3.7 or higher.")
        self.get_MCSH_version()
        self.get_MCSH_checksum()
        self.get_operating_system()
        self.get_python_version()
        self.get_memory()
        self.get_cpu_count()
        self.get_argv()
        getCPUSpeed = self.get_cpu_speed()
        if not getCPUSpeed or self.crash_report_system_info["CPU Speed (Ghz)"] == "Unable to read":
            log("get_computer_info", "WARNING", "Can't determine CPU speed "
                                                "(Probably using platforms except Linux and Windows). "
                                                "'Performance Tester' will be unavailable.")
