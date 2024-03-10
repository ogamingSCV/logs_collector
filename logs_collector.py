#!/usr/bin/env python
"""
This script collects the last lines from log files in a specified folder and its subdirectories.
It is designed to compare the log formats by extracting the last line from each file.


The script follows these steps:

    1. Retrieves the last lines from readable log files.
    2. Truncates the last lines to a maximum length.
    3. Stores the truncated last lines in a sorted list.
    4. Writes the sorted last lines to an output file.


This script is mainly intended to collect the last line of log files
for log format comparison purposes (but can be used as needed).

By extracting and storing the last lines from various log files, it
provides a convenient way to compare and analyze the log formats
used across different files in a given folder and its subdirectories.


Details:
    Author: ogamingSCV
    Version: 1.3
    Email: fetes.05-comings@icloud.com
    License: GNU General Public License v3.0


Usage:
- python3 logs_collector.py [-p FOLDER_PATH] [-o OUTPUT_FILE] [-m MAX_LENGTH]


Arguments:
-p, --folder-path (optional): Path to folder to search for files (default: "/var/log/")
-o, --output-file (optional): Path to output file to store last lines (default: "log_formats.txt")
-m, --max-length (optional): Maximum length for the truncated last lines (default: 80)


Note: This script assumes that the log files are text files and are readable. 
      Binary files and unreadable files will be skipped.


Example:
    Suppose we have a folder named "/path/to/logs/" containing the following log files:

    access.log
    error.log
    app.log

    We want to retrieve the last lines from these log files, truncate them to a maximum length 
    of 70 characters and store the sorted last lines in an output file named "output.txt".

    Running the script with the following command:

        python3 logs_collector.py -p /path/to/logs/ -o output.txt -m 70

    The script will process the log files in the specified folder and generate
    the "output.txt" file with the sorted last lines.

Output:
    The "output.txt" file will contain the following content:

    ### Logs collected from /path/to/logs/ ###
    2023-06-15 23:59:59  [INFO]  This is the last line of access.log.       /path/to/logs/access.log
    2023-07-09 23:59:59  [ERROR] An error occurred in error.log.            /path/to/logs/error.log
    2023-10-01 23:59:59  [INFO]  Last line of app.log with info on login s  /path/to/logs/app.log
"""

import argparse
import os
import socket

# Get hostname
hostname = socket.gethostname()

# Create an ArgumentParser object
parser = argparse.ArgumentParser(
    description="This script collects the last lines from log files in a folder and its subdirs.")

# Add command-line arguments
parser.add_argument('-p', '--folder-path', default="/var/log/",
                    help='path to the folder to search for files')
parser.add_argument('-o', '--output-file', default="log_formats.txt",
                    help='path to the output file to store the sorted last lines')
parser.add_argument('-m', '--max-length', type=int, default=80,
                    help='maximum length for the truncated last lines')

# Parse the command-line arguments
args = parser.parse_args()

# Assign the values from the arguments to variables
folder_path_arg = args.folder_path
output_file_arg = args.output_file
max_length_arg = args.max_length


def check_rec_folder(folder_path, max_length):
    """
    Check for files within the used folder
    """
    last_lines = []
    # Check if the folder path exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        # Iterate over the files in the folder and its subdirectories
        for root, _dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Check if the file is readable and not a symbolic link
                if (os.path.isfile(file_path) and
                    not os.path.islink(file_path) and
                        os.access(file_path, os.R_OK)):
                    try:
                        # Open each file in read mode
                        with open(file_path, "r", encoding="utf-8") as infile:
                            lines = infile.readlines()
                            if lines:
                                # Get the last line from the file and truncate it if necessary
                                last_line = lines[-1].strip()
                                truncated_last_line = last_line[:max_length]
                                perfect_last_line = truncated_last_line.ljust(
                                    max_length)

                                # Create a formatted string with the last line and file path
                                path_last_line = f"{perfect_last_line}\t{file_path}"
                                last_lines.append(path_last_line)
                    except UnicodeDecodeError:
                        # Skip reading binary files
                        continue
    else:
        print("Invalid folder path.")

    return last_lines


def write_to_file(last_lines, output_file):
    """
    Write output to file.
    """
    # Sort the last lines alphabetically
    last_lines.sort()

    # Write the sorted last lines to the output file
    with open(output_file, "a", encoding="utf-8") as file:
        # Add the folder path as a comment in the output file
        file.write(
            f"\n\n### Logs collected from {folder_path_arg} on {hostname} ###\n\n\n")
        for line in last_lines:
            file.write(line + "\n")


# Start the script
folder_outut = check_rec_folder(folder_path_arg, max_length_arg)
write_to_file(folder_outut, output_file_arg)
