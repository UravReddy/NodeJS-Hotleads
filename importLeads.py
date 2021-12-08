import requests
from hashlib import md5
import urllib3
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import time
a = 1
b = 100
urllib3.disable_warnings()

encoding = 'ascii'
userName = 'username'
userToken = 'vtiger_generated_token'
APIURL='VTigerURL/webservice.php'

session = requests.Session()


def getNewLeads():
    mydb = mysql.connector.connect(host="host",user="username",passwd="password",database="database",)
    mycursor = mydb.cursor()
    select_stmt = """SELECT * FROM hotleads2 where imported='0' LIMIT 1"""
    mycursor.execute(select_stmt)
    myresult = mycursor.fetchall()
    for row in myresult:
        if row[5] == '0':
            update_stmt = """UPDATE hotleads2 SET imported=1 WHERE id='%s' """ %(row[0])
            mycursor.execute(update_stmt)
            mydb.commit()
            return row
        else:
            return 'SLEEP'

def getSession(session, name, token):
    response = session.get(APIURL, params={'operation':'getchallenge', 'username':userName}, verify=False)
    token_key = response.json()['result']['token']
    combined = token_key + userToken
    accessKey = md5(combined.encode(encoding)).hexdigest()
    response1 = session.post(APIURL,
            data={'operation':'login', 'username':userName, 'accessKey':accessKey},  
            verify=False)
    print(response1.json())
    return response1.json()['result']['sessionName']

def addLead(session, name, token,fn,ln,em,mb,pd):
    response = session.get(APIURL, params={'operation':'getchallenge', 'username':userName}, verify=False)
    token_key = response.json()['result']['token']
    combined = token_key + userToken
    accessKey = md5(combined.encode(encoding)).hexdigest()
    response1 = session.post(APIURL,data={'operation':'login', 'username':userName, 'accessKey':accessKey},verify=False)
    print(response1.json())

    sName= response1.json()['result']['sessionName']
    data={'operation':'create','sessionName':sName,'format':'json','elementType':'Leads','element':'{"firstname":"'+fn+'","lastname":"'+ln+'","email":"'+em+'","cf_1027":"'+pd+'","mobile":"'+mb+'","assigned_user_id":"19x6"}' }
    print(data)
    response2 = session.post(APIURL,data,verify=False)
    print(response2)
    return response2.json()

while (True):
    lead = (getNewLeads())
    if lead != None:
        print(lead)
        firstName = lead[1]
        lastName = lead[1]
        email = lead[3]
        mobile = lead[2]
        product = lead[6]
        sessionToken = addLead(session, userName, userToken,firstName,lastName,email,mobile,product)
        print(sessionToken)
    time.sleep(5)
