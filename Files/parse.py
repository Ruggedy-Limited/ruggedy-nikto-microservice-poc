#!/usr/bin/python

##########################################################################
# Ruggedy Nikto MicroService Docker Container                            #
# Author: Ruggedy.io                                                     #
# Version 0.1 Beta                                                       #
##########################################################################
import os
import csv
import json
import flask
import psutil
import sqlite3
import pycurl
import datetime
import sqlalchemy
import flask_restful
import flask_jsonpify

##########################################################################
# Commands                                                               #
##########################################################################
if os.path.exists('temp.csv'):
    os.remove('temp.csv')
if os.path.exists('nikto.csv'):
    os.remove('nikto.csv')
if os.path.exists('niktoReport.csv'):
    os.remove('niktoReport.csv')
if os.path.exists('data.db'):
    os.remove('data.db')
os.system('nikto -h targets.txt -o /usr/bin/temp.csv')
csvFile = open('temp.csv').readlines()
open('nikto.csv', 'w').writelines(csvFile[1: ])
open('niktoReport.csv', 'w').write(
    "site,ip,port,vdb,method,uri,description\n" + open('nikto.csv').read())
date = datetime.date.today()

##########################################################################
# Sqlite Import                                                          #
##########################################################################
open('data.db', 'w')
dbconnect = sqlite3.connect("data.db")
cur = dbconnect.cursor()
cur.execute(
    "DROP TABLE IF EXISTS report;")
cur.execute(
    "CREATE TABLE report (site, ip, port, vdb, method, uri, description);")
with open('niktoReport.csv', 'rb') as csvdb:
    datarow = csv.DictReader(csvdb)# comma is default delimiter
    to_db = [(i['site'], i['ip'], i['port'], i['vdb'], i['method'], i['uri'], i['description']) for i in datarow]
    cur.executemany("INSERT INTO report (site, ip, port, vdb, method, uri, description) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
    dbconnect.commit()

##########################################################################
# JIRA Parser                                                            #
##########################################################################
jiraParse = {
    'issueUpdates': []
}
with open('niktoReport.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      jiraParse['issueUpdates'].append({
        'update': {},
        'fields': {
            'project': {
                'key': 'addProject'
            },
            'summary': "Website " + row['site'] + " with IP " + row['ip'] + " and port " + row['port'] + " was scanned on " + str(date) + ".",
            'issuetype': {
                'id': '10004'
            },
            'description': "Website " + row['site'] + " with IP " + row['ip'] + " and port " + row['port'] + " was scanned on " + str(date) + "."
            "\n"
            "\n"
            "Description: "
            "\n"
            "\n" + row['description']
        }
    })
jiraJson = json.dumps(jiraParse)

##########################################################################
# JIRA API                                                               #
##########################################################################
jira_url = 'https://addURL/rest/api/2/issue/bulk'
c = pycurl.Curl()
c.setopt(pycurl.URL, jira_url)
c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
c.setopt(c.USERPWD, "addUser:addPasswd")
# c.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer addToken', 'Content-Type: application/json'])
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, jiraJson)
c.perform()

##########################################################################
# Container API                                                          #
##########################################################################
class Reports(flask_restful.Resource):
    def get(self):
      connect = sqlalchemy.create_engine('sqlite:///data.db')
      apiConnect = connect.connect()
      query = apiConnect.execute("select site, ip, port, vdb, method, uri, description from report;")
      result = {'report': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
      return flask_jsonpify.jsonify(result)

app = flask.Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(Reports, '/report')

if __name__ == '__main__':
    app.run(port='5000',host='0.0.0.0')
