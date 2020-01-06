#!/usr/bin/python

# This script is used to execute other scripts for portmapping.
# To run properly the installation of python 3 is mandatory. Then pip install the mysql-connector and pandas modules.
# Written by Dozie Enworom of BITCON

import details
import exceptions
import argparse
import subprocess

scripts_loc = ''
csv_loc = ''


def schedule():
    return 0


# extracts the info needed from the file source
def filename(file):  # r'C:\Users\SOC-WKSTN-02\Projects\Hosts-and-Ports\Archive\64_EVO-Portmap_2019-11-14.csv'
    name = file.split('\\')
    n = len(name) - 1
    fn = name[n]
    # print(fn)
    name = name[n].split('_')
    n = len(name) - 1
    name = name[n].split('.')
    dt = name[0]
    doc = (fn, dt)
    # print(doc)
    return doc


# runs the other scripts
def cmd(file):
    doc = filename(file)
    print(doc[0])
    print(doc[1])
    subprocess.run('python details.py %s' % doc[0])
    subprocess.run('python exceptions.py %s' % doc[1])


# assigns the values for the arguments
def args():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("file", help="port-mappings", type=str)

    # Parse arguments
    arg = parser.parse_args()
    return arg


if __name__ == '__main__':
    args = args()
    cmd(args.file)
