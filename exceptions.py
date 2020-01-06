#!/usr/bin/python

# This script is used to generate data for the portmap_exception.
# To run properly the installation of python 3 is mandatory. Then pip install the mysql-connector and pandas modules.
# Written by Dozie Enworom of BITCON

import mysql.connector as ms
import argparse


# connect to database
def connect():
    cnx = ms.connect(host='database-1-instance-1.cwdomq0apf1r.us-east-1.rds.amazonaws.com', user='admin', password='pA4rUTHeK?b6', port='3306', database='assessment')
    # print('Connection successful!')
    return cnx


# get recent date
def get_date(dt):
    conn = connect()
    cur = conn.cursor(buffered=True)
    cur.execute("SELECT date FROM portmap WHERE date <= date('%s') ORDER BY date DESC;" % dt)
    gd = cur.fetchmany(2)
    conn.close()
    return gd


# get the portmap_ids
def get_portmap_id(dt):
    conn = connect()
    cur = conn.cursor(buffered=True)
    cur.execute("SELECT id FROM portmap WHERE date <= date('%s') ORDER BY date DESC;" % dt)
    gp = cur.fetchone()
    conn.close()
    return gp


# populate table for port map exception
def portmap_exception(dt):
    conn = connect()
    cur = conn.cursor(buffered=True)

    # get dates
    gd = get_date(dt)
    previous = gd[1][0]
    current = gd[0][0]

    # get id
    gp = get_portmap_id(dt)
    gp = gp[0]

    # get data using the dates
    query1 = "SELECT portmap_dtl.ip, portmap_dtl.site, portmap_dtl.revdns, portmap_dtl.port, portmap_dtl.protocol, portmap_dtl.service FROM assessment.portmap_dtl INNER JOIN assessment.portmap ON portmap_dtl.portmap_id = portmap.id WHERE portmap.date = date('%s');" % previous
    cur.execute(query1)
    previous_data = cur.fetchall()
    query2 = "SELECT portmap_dtl.ip, portmap_dtl.site, portmap_dtl.revdns, portmap_dtl.port, portmap_dtl.protocol, portmap_dtl.service FROM assessment.portmap_dtl INNER JOIN assessment.portmap ON portmap_dtl.portmap_id = portmap.id WHERE portmap.date = date('%s');" % current
    cur.execute(query2, current)
    current_data = cur.fetchall()

    # get comparative data using the dates
    q1 = "SELECT portmap_dtl.ip, portmap_dtl.port, portmap_dtl.protocol FROM assessment.portmap_dtl INNER JOIN assessment.portmap ON portmap_dtl.portmap_id = portmap.id WHERE portmap.date = date('%s');" % previous
    cur.execute(q1)
    pd = cur.fetchall()
    q2 = "SELECT portmap_dtl.ip, portmap_dtl.port, portmap_dtl.protocol FROM assessment.portmap_dtl INNER JOIN assessment.portmap ON portmap_dtl.portmap_id = portmap.id WHERE portmap.date = date('%s');" % current
    cur.execute(q2, current)
    cd = cur.fetchall()

    # search for portmap exceptions
    query3 = "INSERT INTO assessment.portmap_exception (" \
             "portmap_id, ip, site, revdns, port, protocol, service, new, dropped) " \
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

    # find the dropped data
    n = 0
    for i in pd:
        if i not in cd:
            val = (gp, previous_data[n][0], previous_data[n][1], previous_data[n][2], previous_data[n][3], previous_data[n][4], previous_data[n][5], '1', '0')
            # print(str(i) + " --- Previous")
            print(str(val) + " --- Previous")
            cur.execute(operation=query3, params=val)
            # conn.commit()
            n += 1
        else:
            n += 1

    # find the new data
    m = 0
    for i in cd:
        if i not in pd:
            val = (gp, current_data[m][0], current_data[m][1], current_data[m][2], current_data[m][3], current_data[m][4], current_data[m][5], '0', '1')
            print(str(val) + " --- Current")
            cur.execute(operation=query3, params=val)
            conn.commit()
            m += 1
        else:
            m += 1

    conn.close()


# parse the argument for script execution
def arg_parse():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("date", help="port-mappings", type=str)

    # Parse arguments
    arg = parser.parse_args()
    return arg


# bundle together the populate functions
def populate(date):
    print("Populating tables...")
    portmap_exception(date)
    print("...tables populated")


if __name__ == '__main__':
    args = arg_parse()
    populate(args.date)

