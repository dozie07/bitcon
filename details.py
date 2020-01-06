#!/usr/bin/python

# This script is used to populate the portmap and portmap_dtl tables.
# To run properly the installation of python 3 is mandatory. Then pip install the mysql-connector and pandas modules.
# Written by Dozie Enworom of BITCON

import pandas as pd
import mysql.connector as ms
import argparse
import numpy as np
# import sys


# import, parse, format and read csv
def read_csv(file):
    # import csv
    doc = pd.read_csv(filepath_or_buffer=file, encoding='ISO-8859-1').to_records()
    # print(doc)
    # init variable
    index = []
    data = []
    row_total = 0

    # split the csv
    for row in doc:
        for i in row:
            # convert floats to int
            if isinstance(i, float):
                try:
                    # print(i)
                    i = int(i)
                    # print(i)
                    index.append(i)
                except ValueError:
                    i = None
                    index.append(i)
            elif isinstance(i, np.int64):
                # print(i)
                i = int(i)
                # print(i)
                index.append(i)
            else:
                index.append(i)
            # print(i)
        row_total += 1

    # print(index)
    ind = tuple(index)
    # print(ind)

    # make array of data
    a = 0
    b = 18
    x = range(0, row_total)
    for i in x:  # 288
        val = ind[a:b]
        data.append(val)
        a += 19
        b += 19
        # print(val)

    # for i in data:
    #     print(i)

    return data


# connect to database
def connect():
    cnx = ms.connect(host='database-1-instance-1.cwdomq0apf1r.us-east-1.rds.amazonaws.com', user='admin',
                     password='pA4rUTHeK?b6', port='3306', database='assessment')
    # print('Connection successful!')
    return cnx


def get_recent_id():
    conn = connect()
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT id FROM portmap ORDER BY id DESC;")
    # print(cur.fetchall())
    # grd = cur.fetchmany(2)
    grid = cur.fetchone()
    grid = grid[0]
    print(grid)
    conn.close()
    return grid


# populate table for port map
def populate_portmap(file):
    # parse file name
    fn = file[-29:]
    fn = fn.split('.csv')
    fn = fn[0].split()
    fn = fn[0].split('_')
    # print(fn)
    conn = connect()
    cur = conn.cursor(buffered=True)

    # avoid duplicates
    # query0 = "SELECT date FROM portmap WHERE date = date('%s');" % fn[2]
    # cur.execute(query0)
    # dup = cur.fetchone()
    # dup = dup[0]
    # if str(dup) == str(fn[2]):
    #     print('The date already exist in portmap. Would you like to proceed? y/n.')
    #     nxt = input()
    #     if nxt == 'n':
    #         conn.close()
    #         sys.exit()
    #     else:

    # populate portmap
    query = "INSERT INTO portmap (client_id, name, date) VALUES (%s, %s, %s);"
    cur.execute(query, (fn[0], fn[1], fn[2]))
    conn.commit()
    conn.close()


# populate table for port map dtl
def populate_portmap_dtl(file):
    doc = read_csv(file)

    conn = connect()
    cur = conn.cursor(buffered=True)

    query = "INSERT INTO portmap_dtl (" \
            "portmap_id, ip, site, revdns, port, protocol, " \
            "service, version, state, banner, http_respcode, redirect_url, " \
            "redirect_respcode, geoip_country, geoip_region, geoip_city, geoip_netowner, suspect_port) " \
            "VALUES (" \
            "%s, %s, %s, %s, %s, %s, " \
            "%s, %s, %s, %s, %s, %s, " \
            "%s, %s, %s, %s, %s, %s);"

    grid = get_recent_id()

    for row in doc:
        param = (grid, row[1], row[2], row[3], row[4], row[5],
                 row[6], row[7], row[8], row[9], row[10], row[11],
                 row[12], row[13], row[14], row[15], row[16], row[17])
        print(param)
        cur.execute(operation=query, params=param)
        conn.commit()
    conn.close()


# bundle together the populate functions
def populate(file):
    print("Populating tables...")
    populate_portmap(file)
    populate_portmap_dtl(file)
    print("...tables populated")


# parse the argument for script execution
def arg_parse():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("file", help="port-mappings", type=str)

    # Parse arguments
    arg = parser.parse_args()
    return arg


if __name__ == '__main__':
    args = arg_parse()
    populate(args.file)

