"""
Simple OS scan

Create an easy to use toolwith pythonthat lists installed linux packages (with versions)AND python libraries (with versions) in a linux environment.
Assume that the linux distribution would be centos or debian
The tool should also be able to tell whenthose software packages / libraries were installed.

"""
import os
import pandas
import subprocess

"""
Created a cmd-line cmd to get the installed packages with their installation dates as available by the logs:
  Debian: `for x in $(ls -1 /var/log/dpkg.log*); do zcat -f $x | tac | grep -e " install " -e " upgrade "; done | awk -F" " '{print $1 "\t" $2 "\t" $4 "\t" $6}'`
    - Go through all of the dpkg log files available
    - Reverse cat through them
    - Grep for install or upgrade
    - Awk for only the date, time, name, latest-version columns
  ***Note: there is a limitation to this as debian may use rolling logs and does not maintain all installation data as seen in `dpkg-query -l`
  CentOS: centOS uses rpm which maintains the installtime so the cmd is `rpm -qa --queryformat '%{installtime:date} %{installtime} %{name} %{version}\n' | sort -n`
"""
# Write the output to a csv file for easier parsing
subprocess.check_output("for x in $(ls -1 /var/log/dpkg.log*); do zcat -f $x | tac | grep -e \" install \" -e \" upgrade \"; done | awk -F\" \" '{print $1 \"\t\" $2 \"\t\" $4 \"\t\" $6}' > packages.csv", shell=True, text=True)

# Pandas has a max_rows=10 default that we need to override
pandas.set_option('display.max_rows', None)
packages = pandas.read_csv("packages.csv", sep='\t', names=["Date", "Time", "Package Name", "Version"])

# Print the pandas dataframe output
print(packages)

# Delete the csv file we created to parse the values
os.remove("packages.csv")

