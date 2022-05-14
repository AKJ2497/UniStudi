#!/usr/bin/env python3
###############################################################################
#
# UniStudi Backend
#
# Author: Moses Christopher Bollavarapu <moseschristopherb@gmail.com>
#
# TODO: Remove duplicate code
# TODO: Generalize and Modularize
#
###############################################################################

#--------------------------------------
# I M P O R T S
#--------------------------------------
import mysql.connector as mysql
from mysql.connector   import Error
from flask             import Flask,json,request
from flask_cors        import CORS
import json


#--------------------------------------
# G L O B A L   O B J E C T S
#--------------------------------------
app                  = Flask(__name__)
HOST                 = "127.0.0.1"
USER                 = "oswald"
PASSWORD             = "mysql"
DATABASE             = "unistudiDb"
LOGIN_TABLE          = "usLoginTable"
CHECKLIST_TABLE      = "usChecklistTable"
USER_CHECKLIST_TABLE = "usUserChecklistTable" 


#--------------------------------------
# C O R S
#--------------------------------------
CORS(app)


#--------------------------------------
# LOGIN  BASEURL/login
#--------------------------------------
@app.route("/login",methods=["POST"])
def login():
    uname = request.get_json()["uname"]
    password = request.get_json()["password"]
    result = "incorrect"
    try:
        conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        query = "SELECT * FROM "+LOGIN_TABLE+" where userName = '"+uname+"' AND userPass = '"+password+"'"
        print(query)
        cursor.execute(query)
        row = cursor.fetchone()
        if(row != None):
            result = "correct"
    except Error as e:
        print("SQL Error: "+str(e))
        return result
    conn.close()
    return result


#--------------------------------------
# CHECKLIST  BASEURL/checklist
#--------------------------------------
@app.route("/checklist",methods=["GET"])
def getChecklist():
    json_data=[]
    try:
        conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        query = "select * from " + CHECKLIST_TABLE
        print(query)
        cursor.execute(query)
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
    except Error as e:
        print("SQL Error: "+str(e))
        return "Failed"
    conn.close()
    print(json.dumps(json_data))
    return json.dumps(json_data)


#--------------------------------------
# R U N
#--------------------------------------
def run():
    app.run(host="0.0.0.0")
