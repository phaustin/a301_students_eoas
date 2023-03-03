"""
original html: https://git.earthdata.nasa.gov/projects/LPDUR/repos/daac_data_download_python/browse/EarthdataLoginSetup.py

Run this command in a terminal:  set_nasa_password

You will be prompted for your Earth Data login https://urs.earthdata.nasa.gov/

the script will store your username and encrypted password in a file called ~/.netrc
in your home directory

 Author: Cole Krehbiel
 Last Updated: 11/20/2018

"""
# Load necessary packages into Python
from netrc import netrc
from subprocess import Popen
from getpass import getpass
import os
import click
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sat_lib")
except PackageNotFoundError:
    __version__ = "unknown version"

# -----------------------------------AUTHENTICATION CONFIGURATION-------------------------------- #
@click.command()
@click.version_option(__version__)
def main():
    urs = 'urs.earthdata.nasa.gov'    # Earthdata URL to call for authentication
    prompts = ['Enter NASA Earthdata Login Username \n(or create an account at urs.earthdata.nasa.gov): ',
               'Enter NASA Earthdata Login Password: ']

    # Determine if netrc file exists, and if so, if it includes NASA Earthdata Login Credentials
    try:
        netrcDir = os.path.expanduser("~/.netrc")
        netrc(netrcDir).authenticators(urs)[0]

    # Below, create a netrc file and prompt user for NASA Earthdata Login Username and Password
    except FileNotFoundError:
        homeDir = os.path.expanduser("~")
        Popen('touch {0}.netrc | chmod og-rw {0}.netrc | echo machine {1} >> {0}.netrc'.format(homeDir + os.sep, urs), shell=True)
        Popen('echo login {} >> {}.netrc'.format(input(prompts[0]), homeDir + os.sep), shell=True)
        Popen('echo password {} >> {}.netrc'.format(input(prompts[1]), homeDir + os.sep), shell=True)

    # Determine OS and edit netrc file if it exists but is not set up for NASA Earthdata Login
    except TypeError:
        homeDir = os.path.expanduser("~")
        Popen('echo machine {1} >> {0}.netrc'.format(homeDir + os.sep, urs), shell=True)
        Popen('echo login {} >> {}.netrc'.format(input(prompts[0]), homeDir + os.sep), shell=True)
        Popen('echo password {} >> {}.netrc'.format(input(prompts[1]), homeDir + os.sep), shell=True)
