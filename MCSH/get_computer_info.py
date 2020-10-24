"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module name: MCSH.get_computer_info
 Module Revision: 0.0.1-16
 Module Description:
    To get some essential information in order to run 'Performance Tester'.
    Also, when MCSH crashed, can be used for 'System Information' section.
    Because Linux and Windows handles information in very different ways,
    I had to split the way of getting information for different platforms.
    That means you can't run it on other platforms except for Windows and Linux.
 -------------------- MODULE CAUTION --------------------
 WARNING:   This module contains some registry operations in Windows.
            Any improper modifying, corrupting, changing a specific value in this module
            may cause serious errors, probably fatal ones, not allowing the system to boot.
            Please, don't change anything UNLESS you know what you're doing!

 WARNING:   This module, if not used properly, CAN cause damage to the computer.
"""
import fileinput
import platform
import sys

try:
    import winreg
except:
    pass
import psutil

from MCSH.consts import MCSH_version
from MCSH.logging import log, crash


class ComputerInfo:
    def __init__(self):
        """
        computer_info: A detailed computer information.
        crash_report_system_info: To be used in 'System Detailed' in crash reports.
        """
        self.crash_report_system_info = {}
        self.computer_info = {}

    def _pre_check_req_python(self):
        """
        Check if the Python version meets requirements. (3.7+)
        If not, raise an Exception.
        """
        if sys.version_info.major >= 3 and sys.version_info.minor >= 7:
            return
        else:
            log("computer_pre_check", "FATAL", "Python version doesn't meet requirements. Requires 3.7 or higher.")
            crash({
                "description": "Computer didn't pass pre-check.",
                "exception": "Python version mismatch "
                             "(Current={}.{}, Required=3.7+)".format(
                    sys.version_info.major,
                    sys.version_info.minor
                ),
                "computer_info": None
            })

    def _pre_check_req_system(self):
        """
        Pre-check the system if it meets requirements in the README.md.
        Required: Linux or Windows or Mac.
        """
        if platform.system() == "Linux":
            self.computer_info["platform"] = "Linux"
        elif platform.system() == "Windows":
            self.computer_info["platform"] = "Windows"
        elif platform.system() == "Mac":
            self.computer_info["platform"] = "Mac"
        else:
            log("computer_pre_check", "FATAL", "The computer's platform doesn't met the requirements.\n"
                                               "MCSH requires Windows, Mac or Linux to run.")
            crash({
                "description": "Computer didn't pass pre-check.",
                "exception": "Platform mismatch "
                             "(Current={}, Required=Linux,Windows,Mac)".format(
                    platform.system()
                ),
                "computer_info": None
            })

    def _get_MCSH_version(self):
        """
        Get the MCSH version.
        """
        self.crash_report_system_info["MCSH Version"] = MCSH_version

    def _get_operating_system(self):
        """
        Get the detailed operating system.
        """
        self.crash_report_system_info["Operating System"] = platform.platform()

    def _get_python_version(self):
        """
        Get the Python version.
        """
        self.crash_report_system_info["Python version"] = sys.version

    def _get_memory(self):
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

    def _get_cpu_count(self):
        """
        Get the CPU counts.
        """
        self.crash_report_system_info["CPU Count"] = psutil.cpu_count()
        self.computer_info["cpu"] = psutil.cpu_count()

    def _get_argv(self):
        """
        Get the arguments (argv).
        """
        try:
            self.crash_report_system_info["Startup Arguments"] = sys.argv[1:]
        except:
            self.crash_report_system_info["Startup Arguments"] = "Unknown"

    def _get_cpu_speed(self):
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
        self._pre_check_req_python()
        self._pre_check_req_system()
        self._get_MCSH_version()
        self._get_operating_system()
        self._get_python_version()
        self._get_memory()
        self._get_cpu_count()
        self._get_argv()
        getCPUSpeed = self._get_cpu_speed()
        if not getCPUSpeed or self.crash_report_system_info["CPU Speed (Ghz)"] == "Unable to read":
            log("get_computer_info", "WARNING", "Can't determine CPU speed "
                                                "(Probably using platforms except Linux and Windows). "
                                                "'Performance Tester' will be unavailable.")
