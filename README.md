[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

# Log Format Collector

This script collects the last lines from readable log files in a specified folder and its subdirectories. It is designed to compare log formats by extracting the last line from each file.

## Features

- Retrieves the last lines from readable log files.
- Truncates the last lines to a maximum length.
- Stores the truncated last lines in a sorted list.
- Writes the sorted last lines to an output file.

## Purpose

The Log Collector script is mainly intended to collect the last line of log files for log format comparison purposes, but it can be used as needed. By extracting and storing the last lines from various log files, it provides a convenient way to compare and analyze the log formats used across different files in a given folder and its subdirectories.

## Usage

```shell
python3 logs_collector.py [-p FOLDER_PATH] [-o OUTPUT_FILE] [-m MAX_LENGTH]
```

## Arguments

- `-p`, `--folder-path` (optional): Path to the folder to search for files (default: "/var/log/")
- `-o`, `--output-file` (optional): Path to the output file to store the sorted last lines (default: "log_formats.txt")
- `-m`, `--max-length` (optional): Maximum length for the truncated last lines (default: 80)

**Note**: This script assumes that the log files are text files and are readable. Binary files and unreadable files will be skipped.

## Example

Suppose we have a folder named "/path/to/logs/" containing the following log files:

- `access.log`
- `error.log`
- `application.log`

We want to retrieve the last lines from these log files, truncate them to a maximum length of 70 characters, and store the sorted last lines in an output file named "output.txt".

Running the script with the following command:

```shell
python3 logs_collector.py -p /path/to/logs/ -o output.txt -m 70
```

The script will process the log files in the specified folder and generate the "output.txt" file with the sorted last lines.

## Output

The "output.txt" file will contain the following content:

```
### Logs collected from /path/to/logs/ ###
2023-06-15 23:59:59  [INFO]  This is the last line of access.log.       /path/to/logs/access.log
2023-07-09 23:59:59  [ERROR] An error occurred in error.log.            /path/to/logs/error.log
2023-10-01 23:59:59  [INFO]  Last line of application.log with some ex  /path/to/logs/application.log
```

## Author

Author: ogamingSCV

Version: 1.3

Email: fetes.05-comings@icloud.com
