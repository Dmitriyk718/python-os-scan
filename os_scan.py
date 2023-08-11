"""
Simple OS scan

Create an easy to use toolwith pythonthat lists installed linux packages (with versions)AND python libraries (with versions) in a linux environment.
Assume that the linux distribution would be centos or debian
The tool should also be able to tell whenthose software packages / libraries were installed.
The solution should be completed and submitted for review within 48 hours.

"""
import os
import pandas
import subprocess

output = subprocess.check_output("dpkg-query -f '${Package}\t${Version}\n' -W > packages.csv", shell=True, text=True)

pandas.set_option('display.max_rows', None)
my_data = pandas.read_csv("packages.csv", sep='\t', names=["Package Name", "Version"])
print(my_data)

os.remove("packages.csv")

