#!/usr/bin/env python3.7
# Written by Dozie Enworom
# ---------------------------------------------------------------------------------------------------------------------
# Purpose:
#   Returns a list of eventId's belonging to outliers
#
# In Progess:
#   Determine which saved model to use based on file name
# ---------------------------------------------------------------------------------------------------------------------

import csv
from sklearn.ensemble import IsolationForest
from sklearn.externals import joblib as jl
from sklearn.preprocessing import OrdinalEncoder
import pickle


# local variables
rows = []
eid = []
src = "events.csv"
dest = "eid.txt"
cust_name = ['cn_01', 'cn_02', 'cn_03', 'cn_04', 'cn_05']
cust_model = ['cm_01.sav', 'cm_02.sav', 'cm_03.sav', 'cm_04.sav', 'cm_05.sav']


# prep data
def prep_data():
    with open(src, 'r') as file:
        fr = csv.reader(file)
        for i in fr:
            rows.append(i[2:])
            eid.append(i[1])
        rows.pop(0)
        eid.pop(0)
    file.close()
    # print(rows)
    return rows


# encode data
pd = prep_data()
enc = OrdinalEncoder(dtype='int64')
data = enc.fit_transform(pd)
d = enc.inverse_transform(data)
# print(pd)
# print(data)
# print(d)


# fit model, predict outlier
clf = IsolationForest(max_features=6)
pred = clf.fit_predict(data)
# print(pred)


# get data
def output_data():
    with open(dest, 'w') as file:
        n = 0
        olc = 0
        ilc = 0
        for i in pred:
            if i == -1:
                file.write(eid[n] + "\n")
                print("Outlier: %s" % eid[n])
                olc += 1
            elif i == 1:
                print("Inlier: %s" % eid[n])
                ilc += 1
            n += 1
        print("Outliers total: %s \nInliers total: %s \nOverall total: %s" % (olc, ilc, n))
        print((olc + ilc) == n)
    file.close()


# output_data()


# save model
fn = "od_model.sav"
jl.dump(clf, fn, 2)
# pickle.dump(clf, fn)

# load model
jl.load(fn)
# pickle.load(fn)

# make predictions
# jl.predict(fn)

