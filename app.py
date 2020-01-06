#!/usr/bin/env python3
# Author: Chiedozie Enworom
# Owner: Burke IT Consulting

from flask import Flask, jsonify, request
import database
import reputation

# creates the app
app = Flask(__name__)

# @return: a home page
@app.route('/', methods=['GET'])  # **************************************
def index():
    return jsonify("IdentiCaller")


# @param: a phone number
# @return: the reputation for the phone number
@app.route('/reputation/<phone>', methods=['GET'])
def get_reputation(phone):  # **************************************
    hdr = get_headers()

    if header_check() and is_phone(phone):
        print('Header Check is GOOOOOOD')
        database.add_calls(cid=hdr.get('Client-Id'), pn=phone)
        return jsonify(reputation.get_rep(phone))

    return "Please check your headers."


# @params: the url of the request
# @return: the headers for client id and api token
def get_headers():  # **************************************
    arr = []

    for i in request.headers:
        if 'Client-Id' in i or 'Api-Token' in i:
            arr.append(i)

    hdr = dict(arr)

    return hdr


# @params: a phone number
# @return: true or false for the number format
def is_phone(pn):
    # print(str(pn))
    spn = str(pn)
    if len(spn) == 10:
        for i in spn:
            if int(i) <= 9:
                # print(True)
                return True
    elif len(spn) == 11 or len(spn) == 12:
        if spn[0] == '1' or spn[:2] == '+1':
            # print(True)
            return True
    # print(False)
    return False


# @return: if headers are correct, true
def header_check():  # **************************************
    hdr = get_headers()

    conn = database.open_conn()
    curs = conn.cursor()
    curs.execute("SELECT user_id, client_token FROM clients")
    row = curs.fetchall()

    for i in row:
        if int(i[0]) == int(hdr.get('Client-Id')) and i[1] == hdr.get('Api-Token'):
            conn.close()
            print('header true')
            return True

    print('header false')
    conn.close()
    return False


# @return: the api token, client id and number of remaining calls
@app.route('/license', methods=['GET'])
def get_license():  # **************************************
    hdr = get_headers()

    if header_check():
        conn = database.open_conn()
        curs = conn.cursor()
        rows = curs.execute("SELECT * FROM license WHERE user_id = %s" % hdr.get('Client-Id'))
        conn.close()
        return rows

    return "Please check that your Client-Id and Api-Token are correct"


# @return: data records
@app.route('/records', methods=['GET'])
def get_records():  # **************************************
    hdr = get_headers()

    conn = database.open_conn()
    curs = conn.cursor()
    curs.execute("SELECT * FROM client")
    rows = curs.fetchall()
    if header_check():
        for i in rows:
            if i[0] == hdr.get('Client-Id'):
                conn.close()
                return jsonify(i)

    conn.close()
    return "Please check that your Client-Id and Api-Token are correct"


# @return: warnings regarding their api call usage
def warning():  # **************************************
    hdr = get_headers()

    conn = database.open_conn()
    curs = conn.cursor()
    curs.execute("SELECT id FROM client")
    rows = curs.fetchall()

    for i in rows:
        if i == hdr.get('Client-Id'):
            curs.execute("SELECT calls FROM calls WHERE id = %s" % i)
            num = curs.fetchone()
            if num >= 0:
                conn.close()
                return "CALL LIMIT EXCEEDED"
            elif num >= 5:
                conn.close()
                return "APPROACHING CALL LIMIT"

    return "OK"


if __name__ == '__main__':
    # app.debug = True
    app.run()
