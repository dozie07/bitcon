#!/usr/bin/env python3
import mysql.connector as mysql


# connects to or creates a database
def open_conn():
    conn = mysql.connect(host='***************rds.amazonaws.com',
                         user='admin',
                         password='************',
                         port='******',
                         database='**********')
    print('Connection Successful')
    return conn


# an accessor for client table
def get_client():
    conn = open_conn()
    curs = conn.cursor()
    # curs.execute('SELECT client_token FROM clients')
    curs.execute('SELECT id, client_token FROM clients')
    rows = curs.fetchall()
    print(curs.column_names)

    for i in rows:
        print(i)

    conn.close()
    return rows


def get_calls():
    conn = open_conn()
    curs = conn.cursor()
    # curs.execute('SELECT client_token FROM clients')
    curs.execute('SELECT * FROM calls')
    rows = curs.fetchall()
    for i in rows:
        print(i)
    print(curs.column_names)
    conn.close()
    # return rows


# a function for inserting calls into the calls table
def add_calls(cid, pn):
    conn = open_conn()
    curs = conn.cursor()
    curs.execute('INSERT INTO identicaller.calls (client_id, phone_num) VALUES(%s, %s);' % (cid, pn))
    conn.close()


print(get_calls())
# add_calls(2, '6783142228')
