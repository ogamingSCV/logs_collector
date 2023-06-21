#!/usr/bin/env python
"""
This script collects the last lines from readable log files in a specified folder and its subdirectories.
It is designed to compare the log formats by extracting the last line from each file.


The script follows these steps:

    1. Retrieves the last lines from readable log files.
    2. Truncates the last lines to a maximum length.
    3. Stores the truncated last lines in a sorted list.
    4. Writes the sorted last lines to an output file.


This script is mainly intended to collect the last line of log files for log format comparison purposes (but can be used as needed). 
By extracting and storing the last lines from various log files, it provides a convenient way to compare and analyze the log formats 
used across different files in a given folder and its subdirectories.


Details:
    Author: ogamingSCV
    Version: 1.1
    Email: fetes.05-comings@icloud.com


Usage:
    - python3 logs_collector.py [folder_path] [output_file] [max_length]


Arguments:
    - folder_path (optional): Path to the folder to search for files (default: "/var/log/")
    - output_file (optional): Path to the output file to store the sorted last lines (default: "log_formats.txt")
    - max_length (optional): Maximum length for the truncated last lines (default: 80)


Note: This script assumes that the log files are text files and are readable. Binary files and unreadable files will be skipped.


Example:
    Suppose we have a folder named "/path/to/logs/" containing the following log files:

    access.log
    error.log
    application.log

    We want to retrieve the last lines from these log files, truncate them to a maximum length of 70 characters, and store the sorted 
    last lines in an output file named "output.txt".

    Running the script with the following command:

        python3 logs_collector.py /path/to/logs/ output.txt 70

    The script will process the log files in the specified folder and generate the "output.txt" file with the sorted last lines.

Output:
    The "output.txt" file will contain the following content:

    ### Logs collected from /path/to/logs/ ###
    2023-06-15 23:59:59  [INFO]  This is the last line of access.log.       /path/to/logs/access.log
    2023-07-09 23:59:59  [ERROR] An error occurred in error.log.            /path/to/logs/error.log
    2023-10-01 23:59:59  [INFO]  Last line of application.log with some ex  /path/to/logs/application.log
"""

import argparse
import os
import sys

# List to store the last lines from files
last_lines = []

# Set default values
folder_path = "/var/log/"
output_file = "log_formats.txt"
max_length = 80

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="This script collects the last lines from readable log files in a specified folder and its subdirectories. It is designed to compare the log formats by extracting the last line from each file.")

# Add command-line arguments
parser.add_argument('folder_path', nargs='?', default=folder_path, help='path to the folder to search for files')
parser.add_argument('output_file', nargs='?', default=output_file, help='path to the output file to store the sorted last lines')
parser.add_argument('max_length', nargs='?', type=int, default=max_length, help='maximum length for the truncated last lines')

# Parse the command-line arguments
args = parser.parse_args()

# Assign the values from the arguments to variables
folder_path = args.folder_path
output_file = args.output_file
max_length = args.max_length

# Open the output file in append mode
with open(output_file, "a") as outfile:

    # Check if the folder path exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        # Add the folder path as a comment in the output file
        outfile.write(f"### Logs collected from {folder_path} ###\n")

        # Iterate over the files in the folder and its subdirectories
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Check if the file is readable and not a symbolic link
                if os.path.isfile(file_path) and not os.path.islink(file_path) and os.access(file_path, os.R_OK):
                    try:

                        # Open each file in read mode
                        with open(file_path, "r") as infile:
                            lines = infile.readlines()
                            if lines:

                                # Get the last line from the file and truncate it if necessary
                                last_line = lines[-1].strip()
                                truncated_last_line = last_line[:max_length]

                                if len(truncated_last_line) < max_length:
                                    # Fill the remaining space with spaces
                                    perfect_last_line = truncated_last_line + ' ' * (max_length - len(truncated_last_line))
                                else:
                                    perfect_last_line = truncated_last_line

                                # Create a formatted string with the last line and file path
                                path_last_line = perfect_last_line + "\t" + file_path
                                last_lines.append(path_last_line)

                    except UnicodeDecodeError:
                        # Skip reading binary files
                        continue

        # Sort the last lines alphabetically
        last_lines.sort()

        # Write the sorted last lines to the output file
        for line in last_lines:
            outfile.write(line + "\n")

    else:
        print("Invalid folder path.")
