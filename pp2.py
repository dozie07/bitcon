#!/usr/bin/env python3.7
# Written by Dozie Enworom
# ---------------------------------------------------------------------------------------------------------------------
# Purpose:
#   This file pre-processes the data from the cef files and then converts it into a csv file.
#   Returns the attributes needed to detect anomalies within the data.
# ---------------------------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import os


# returns "CategoryBehaviour="
def getBehaviour(x):
    lists = x.split(" ")
    val = "NULL"
    for l in lists:
        if l.__contains__("categoryBehavior="):
            val = l.split("=")
            val = val[1]
#         # print(val)
    return val


# returns "CategoryObject="
def getObject(x):
    lists = x.split(" ")
    val = "NULL"
    for l in lists:
        if l.__contains__("categoryObject="):
            val = l.split("=")
            val = val[1]
        # print(val)
    return val


# returns the device "CategoryOutcome=" as "Success" or "Failure"
def getOutcome(x):
    lists = x.split(" ")
    val = "NULL"
    for l in lists:
        if l.__contains__("categoryOutcome="):
            val = l.split("=")
            val = val[1]
            if val.__eq__("/Success"):
                val = "/Success"
            if val.__eq__("/Failure"):
                val = "/Failure"
        # print(val)
    return val


# returns "CategorySignificance="
def getSignificance(x):
    lists = x.split(" ")
    val = "NULL"
    for l in lists:
        if l.__contains__("categorySignificance="):
            val = l.split("=")
            val = val[1]
    # print(val)
    return val


# returns the "externalId="
def getExternalId(x):
    lists = x.split(" ")
    val = "NULL"
    for l in lists:
        if l.__contains__("externalId="):
            val = l.split("=")
            val = val[1]
    # print(val)
    # return int(val)
    return val


# returns the "eventId="
def getEventId(x):
    lists = x.split(" ")
    val = "NULL"
    for l in lists:
        if l.__contains__("eventId="):
            val = l.split("=")
            val = val[1]
    # print(val)
    # return int(val)
    return val


# returns the potential threat level
def getThreatLevel(x):
    lists = x.split("|")
    val = "NULL"
    for l in lists:
        if l.__contains__("Low"):
            # val = 0
            val = "Low"
        elif l.__contains__("Medium"):
            # val = 1
            val = "Medium"
        elif l.__contains__("Very-high"):
            # val = 2
            val = "Very-high"
    # print(val)
    return val


# returns a line of data in a row
def getDataRow(x):
    _a = getEventId(x)
    _b = getBehaviour(x)
    _c = getObject(x)
    _d = getOutcome(x)
    _e = getSignificance(x)
    _f = getExternalId(x)
    _g = getThreatLevel(x)
    _row = [_a, _b, _c, _d, _e, _f, _g]
    # print(_row)
    return _row


# returns the features: EventId, Behaviour, Object, Outcome, Significance, ExternalId, Risk
def getDataRowFeatures(x):
    _a = getEventId(x)
    _b = getBehaviour(x)
    _c = getObject(x)
    _d = getOutcome(x)
    _e = getSignificance(x)
    _f = getExternalId(x)
    _g = getThreatLevel(x)
    _row = [_a, _b, _c, _d, _e, _f, _g]
    # print(_row)
    return _row


# returns the whole data set
def getDataSet(x):
    files = open(x, encoding="utf8").readlines()
    data = list()
    for foo in files:
        data.append(getDataRow(foo))
    print(data)
    return data


# returns the data set features
def getDataSetFeatures(x):
    files = open(x, encoding="utf8").readlines()
    data = list()
    for foo in files:
        data.append(getDataRowFeatures(foo))
    # print(data)
    return data


# returns a list of data set features from the training data
def getTrainFeatures():
    x = r'C:\Users\dozie\PycharmProjects\BitCon\ML\train_data'
    data = []
    for n in os.listdir(x):
        dirs = os.path.join(x, n)
        data.append(getDataSetFeatures(dirs))
    # print(data)
    return data


# returns data frame of train data features XXXX
def getTrainDataFeatures(x):
    df = pd.DataFrame(x, columns=["EventId", "Behaviour", "Object", "Outcome", "Significance", "ExternalId", "Threat"])
    return df


# returns the train data features in a aggregated format
def getAggregator(x, y):
    n = ""
    if y is "d":
        n = "EventId"
    if y is "b":
        n = "Behaviour"
    if y is "ob":
        n = "Object"
    if y is "s":
        n = "Significance"
    if y is "o":
        n = "Outcome"
    if y is "ex":
        n = "ExternalId"
    if y is "t":
        n = "Threat"

    df = pd.DataFrame(x, columns=["EventId", "Behaviour", "Object", "Outcome", "Significance", "ExternalId", "Threat"])
    grouped = df.groupby(n)
    for name, group in grouped:
        print("\n -----------------------------------------------")
        print(name)
        print(group)
    return df


# get data set training features and place into dataframe
tf = getDataSetFeatures(r"events.cef")
trainFeats = getTrainDataFeatures(tf)
print(trainFeats.to_csv())
# print(trainFeats.to_csv(path_or_buf=r"C:\Users\SOC-WKSTN-02\PycharmProjects\OutlierDetection\events.csv"))
