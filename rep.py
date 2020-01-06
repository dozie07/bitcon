#!/usr/bin/env python3
# Author: Chiedozie Enworom
# Owner: Burke IT Consulting

import requests
from requests.auth import HTTPBasicAuth
import argparse
import mysql.connector as mysql


# a function for inserting calls into the database
# @params: cid=client_id, pn=phone_num
# def add_calls(cid, pn):
def add_calls(tk, pn):
    num = 0
    conn = mysql.connect(host='database-1-instance-1.cwdomq0apf1r.us-east-1.rds.amazonaws.com',
                         user='admin',
                         password='pA4rUTHeK?b6',
                         port='3306',
                         database='identicaller')
    curs = conn.cursor()

    try:
        curs.execute("SELECT id FROM clients WHERE client_token = '%s';" % tk)
        rows = curs.fetchall()
        cid = rows[0]
        curs.execute('INSERT INTO identicaller.calls (client_id, phone_num) VALUES(%s, %s);' % (cid[0], pn))
        curs.execute("SELECT phone_num FROM calls ORDER BY client_id DESC;")
        conn.close()
        # print("Database Updated")
        num += 1
        return num
    except IndexError:
        print("Token Not Found")
        return num


# @param: phone number
# @return: raw phone reputation pt1
def request1(pn):
    url = 'https://lookups.twilio.com/v1/PhoneNumbers/%2B1' + str(pn) \
          + '?CountryCode=United%20States&Type=carrier&AddOns=whitepages_pro_phone_intel'
    req = requests.get(url, auth=HTTPBasicAuth(username='ACb0c2da5eb91f902a52a277133e4dda4b',
                                               password='98e191ca52cb49ca35c60a092ec64363')).text.split(",")
    # print(req)
    return req


# @param: phone number
# @return: raw phone reputation pt2
def request2(pn):
    url = 'https://lookups.twilio.com/v1/PhoneNumbers/+1%s/?AddOns=nomorobo_spamscore&' \
          'AddOns.nomorobo_spamscore.secondary_address=+1' % str(pn)
    req = requests.get(url, auth=HTTPBasicAuth(username='ACb0c2da5eb91f902a52a277133e4dda4b',
                                               password='98e191ca52cb49ca35c60a092ec64363')).text.split(",")
    # print(req)
    return req


# @param: phone number
# @return: parsed and formatted phone reputation for pt1
def parser1(pn):
    pair = []
    for i in request1(pn):
        if i.__contains__("is_valid") or i.__contains__("line_type") or i.__contains__("country_name") \
                or i.__contains__("is_prepaid"):
            pair.append(i)
        elif i.__contains__("country_code") and not i.__contains__("mobile_"):
            pair.append(i)
        elif i.__contains__("name") and not i.__contains__("caller_"):
            pair.append(i)

    counter = 0

    for j in pair:

        if j.__contains__('}}}}'):
            temp = j.split('}}}}')
            pair[counter] = temp[0]
        counter = counter + 1

    return pair


# @param: phone number
# @return: parsed and formatted phone reputation for pt2
def parser2(pn):
    sc = []
    for i in request2(pn):
        if i.__contains__("score") and not i.__contains__("spamscore"):
            n = i.split('"')
            sc.append(n[1])
            if n[2].__contains__('0'):
                sc.append('False')
            elif n[2].__contains__('1'):
                sc.append('True')
    sc[0] = 'robo_caller'
    return sc


# @param: phone number
# @return: final form for the phone reputation
# def get_rep(phone):
def get_rep(token, phone, bin):
    pars = parser1(phone)
    k = []
    v = []
    key = []
    val = []

    for i in pars:
        x = i.split(':')
        k.append(x[0])
        v.append(x[1])

    for i in k:
        j = i.split('"')
        if i.__contains__('"'):
            key.append(j[1])
        else:
            key.append(j[0])

    for i in v:
        j = i.split('"')
        if i.__contains__('"'):
            val.append(j[1])
        else:
            val.append(j[0])

    try:
        key[1] = 'carrier'
        sc = parser2(phone)
        key.pop(4)
        val.pop(4)
        key.append(sc[0])
        val.append(sc[1])
        dt = {key[0]: val[0], key[1]: val[1], key[2]: val[2], key[3]: val[3], key[4]: val[4], key[5]: val[5], key[6]: val[6]}
        print(dt)
        return dt

    except IndexError:
        print("This number is either, unavailable or out of service.")
        return "Please make sure you are using the recommended format."


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("token", help="client_token", type=str)
    parser.add_argument("phone", help="phone_num", type=str)
    parser.add_argument("bin", help="string_num", type=str)

    # Parse arguments
    arg = parser.parse_args()
    return arg


if __name__ == '__main__':
    args = parse_arguments()
    get_rep(args.token, args.phone, args.bin)
