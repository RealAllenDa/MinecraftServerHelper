"""
 ***************************************
 MCSH - A Minecraft Server Helper.
 Coded by AllenDa 2020.
 Licensed under MIT.
 ***************************************
 Module name: MCSH.crash_report
 Module Revision: 0.0.1-16
 Module Description:
    Generates the crash report for MCSH.
    Considering crashes during the PRE-INITIALIZATION, it will NOT use the locale file.
    Instead, it will use English as crash report's language.
"""
import os
import sys
import tarfile
import time


def generate_crash_report(crash_description, crash_detailed_exception, computer_crash_info):
    """
    Generate a crash report using English.
    """
    if len(
            [lists for lists in os.listdir("./MCSH/crash_report")
             if os.path.isfile(os.path.join("./MCSH/crash_report", lists))]
    ) >= 10:
        try:
            tar = tarfile.open("./MCSH/crash_report/pack.tar.gz", "w:gz")
            for root, directory, files in os.walk("./MCSH/crash_report"):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.splitext(file)[1] == ".log":
                        tar.add(file_path)
                        os.remove(file_path)
            tar.close()
        except Exception as e:
            print("[??-??] [crash_report/ERROR]: Failed to pack crash reports.")
    CRASH_REPORT_FORMAT = '''---- MCSH Crash Report ----
Time: {time}
Process Time: {process_time}
Description: {description}

{detailed_exception}

-- System Details --
Details:
{computer_crash_info}
'''
    formatted_crash_info = ""
    crash_report_filename = "CRASH_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".log"
    if computer_crash_info is None:
        formatted_crash_info = "??? (Crashes during pre-initialization)"
    if formatted_crash_info != "??? (Crashes during pre-initialization)":
        for key in computer_crash_info.keys():
            formatted_info = "  {key}: {content}\n".format(**{
                "key": key,
                "content": computer_crash_info[key]
            })
            formatted_crash_info += formatted_info
    FORMATTED_CRASH_REPORT = CRASH_REPORT_FORMAT.format(**{
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "process_time": time.process_time(),
        "description": crash_description,
        "detailed_exception": crash_detailed_exception,
        "computer_crash_info": formatted_crash_info
    })
    if not os.path.exists("./MCSH/crash_report"):
        try:
            os.mkdir("./MCSH/crash_report")
        except:
            print("[??-??] [crash_report/FATAL]: Failed to generate a crash report."
                  "Cannot make crash_report folder.")
            sys.exit(2)
    try:
        with open("./MCSH/crash_report/{}".format(crash_report_filename), "w+") as f:
            f.write(FORMATTED_CRASH_REPORT)
            f.close()
    except:
        print("[??-??] [crash_report/FATAL]: Failed to generate a crash report."
              "Cannot write to crash_report folder.")
        sys.exit(2)
    print("[??-??] [crash_report/FATAL]: Generated report under ./MCSH/crash_report folder.")
    sys.exit(2)
