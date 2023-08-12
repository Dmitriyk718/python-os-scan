"""
Simple OS scan

Create an easy to use toolwith pythonthat lists installed linux packages (with versions)AND python libraries (with versions) in a linux environment.
Assume that the linux distribution would be centos or debian
The tool should also be able to tell whenthose software packages / libraries were installed.

"""
import os
import pandas
from pandas import DataFrame
import pkg_resources
import subprocess
import time

"""
Created a cmd-line cmd to get the installed packages with their installation dates as available by the logs:
  Debian: `for x in $(ls -1 /var/log/dpkg.log*); do zcat -f $x | tac | grep -e " install " -e " upgrade "; done | awk -F" " '{print $1 "\t" $2 "\t" $4 "\t" $6}'`
    - Go through all of the dpkg log files available
    - Reverse cat through them
    - Grep for install or upgrade
    - Awk for only the date, time, name, latest-version columns
  **Note: there is a limitation to this as debian may use rolling logs and does not maintain all installation data as seen in `dpkg-query -l`**
  
  CentOS: centOS uses rpm which maintains the installtime so the cmd is `rpm -qa --queryformat '%{installtime:date} \t %{installtime} \t %{name} \t %{version}\n' | sort -n`
"""
def get_system_packages():
  # Write the output to a csv file for easier parsing
  subprocess.check_output("for x in $(ls -1 /var/log/dpkg.log*); do zcat -f $x | tac | grep -e \" install \" -e \" upgrade \"; done | awk -F\" \" '{print $1 \"\t\" $2 \"\t\" $4 \"\t\" $6}' > sys_packages.csv", shell=True, text=True)

  # Pandas has a max_rows=10 default that we need to override
  pandas.set_option('display.max_rows', None)
  sys_packages = DataFrame(pandas.read_csv("sys_packages.csv", sep='\t', names=["Date", "Time", "Package Name", "Version"])).to_markdown() 

  # Print the pandas dataframe output
  print("#####################################################################################################################################")
  print("##################################################### SYSTEM PACKAGES ###############################################################")
  print("#####################################################################################################################################")

  print(sys_packages)

  print("#####################################################################################################################################")
  print("##################################################### SYSTEM PACKAGES ###############################################################")
  print("#####################################################################################################################################")

  # Delete the csv file we created to parse the values
  os.remove("sys_packages.csv")

"""
Loop through the system python packages to get the package names, versions and installation times
"""
def get_python_packages():
  names = []
  versions = []
  install_datetimes = []

  # TODO: Figure out how to update this deprecated import
  for package in pkg_resources.working_set:
    names.append(package.key)
    versions.append(package.version)
    install_datetimes.append(time.ctime(os.path.getctime(package.location)))

  # Create the dict definition to be used by pandas
  py_packages_data = {'Install Date': install_datetimes, 'Package Name': names, 'Version': versions }
  
  py_packages = DataFrame.from_dict(py_packages_data).to_markdown()

  # Print the pandas dataframe output
  print("#################################################################################################################")
  print("############################################ PYTHON PACKAGES ####################################################")
  print("#################################################################################################################")

  print(py_packages)

  print("#################################################################################################################")
  print("############################################ PYTHON PACKAGES ####################################################")
  print("#################################################################################################################")


get_system_packages()
print("\n")
get_python_packages()
