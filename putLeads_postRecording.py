import os, sys
from pathlib import Path
from mysql.connector.errors import get_mysql_exception
import requests
import urllib3
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import time
import json
import requests
from requests.structures import CaseInsensitiveDict

while (True):
    mydb = mysql.connector.connect(host="10.0.0.101",user="root",passwd="pravit",database="calorico",)
    mycursor = mydb.cursor()
    #query to retrieve the records needed to be used in the put request
    select_stmt = """select vtiger_contactscf.contactid,vtiger_contactdetails.firstname,vtiger_contactdetails.lastname,vtiger_contactscf.cf_1181 AS Address,vtiger_contactscf.cf_1433 AS streetNumber,vtiger_contactscf.cf_1437 AS AppartmentNumber,vtiger_contactscf.cf_1175 AS City,vtiger_contactscf.cf_1179 AS ZIP,vtiger_contactscf.cf_1451 as Gender,vtiger_contactscf.cf_1431 AS OfferVariation,vtiger_contactscf.cf_1169 AS Shipper,vtiger_contactscf.cf_1461 AS ShipperNote,vtiger_contactscf.cf_1439 AS Status,vtiger_contactscf.cf_1441 AS statusComment,vtiger_contactscf.cf_1471,vtiger_contactscf.cf_1465 AS Suburb,vtiger_contactscf.cf_1467 from vtiger_contactscf INNER JOIN vtiger_contactdetails on vtiger_contactdetails.contactid=vtiger_contactscf.contactid where cf_1469 IN (0,'0','',' ') AND cf_1155='Yes' LIMIT 1"""
    mycursor.execute(select_stmt)
    myresult = mycursor.fetchall()
    for row in myresult:
        contactid = row[0]
        fName = row[1]
        lName = row[2]
        street = row[3]
        streetNumber = row[4]
        appartmentNumber = row[5]
        city = row[6]
        zip = row[7]
        gender = row[8]
        offerVariation = row[9]
        shipper = row[10]
        shipperNote = row[11]
        status = row[12]
        statusComment = row[13]
        orderId = row[14]

        #########PATCH
        url = "url for put request with the orderid/%s" %(orderId)

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        headers["X-AUTH-TOKEN"] = "authentication token value"

        data = """
        {
            "customer": {
                "first_name": "%s",
                "last_name": "%s",
                "address": "%s",
                "address_number": "%s",
                "address_entrance_number": "%s",
                "address_floor_number": "%s",
                "address_apartment_number": "%s",
                "city": "%s",
                "zip": "%s",
                "gender": "%s"
            },
            "offer_variation": %s,
            "shipper": "%s",
            "shipper_note": "%s",
            "status": "%s",
            "status_comment": "%s"
        }

        """ %(fName,lName,street,streetNumber,'','','',city,zip,gender,offerVariation,shipper,shipperNote,status,statusComment)

        resp = requests.patch(url, headers=headers, data=data)

        print(resp.status_code)
        print(resp.text)
        if (resp.status_code ==400):
            print('ERROR ON ORDERID : '+str(orderId))
            #updating the crm record with a value of 9 to indicate error 400 for easier filtering
            select_stmt = """UPDATE vtiger_contactscf set cf_1469=9 WHERE contactid='%s'""" %(contactid)
            mycursor.execute(select_stmt)
            mydb.commit()
        if (resp.status_code ==200):    
            #updating the crm record with a value of 1 to indicate success
            select_stmt = """UPDATE vtiger_contactscf set cf_1469=1 WHERE contactid='%s'""" %(contactid)
            mycursor.execute(select_stmt)
            mydb.commit()

            # Obtaining the call recording stored within a folder labeled as the orderid and then
            # submitting the call through a post request
            dirs = os.listdir( r"\\path to folder\%s" %(orderId) )
            for file in dirs:
                print(file)
                url = "url of api to post call recording to/%s/call" %(orderId)                                    
                with open(r"\\path to folder\%s\%s" %(orderId,file),'rb') as fobj:                
                    r = requests.post(url,headers=headers, files={'file': fobj})          
                    print(r.status_code)
                    print(r.text)
                    if (r.status_code == 200):
                        #updating field on crm to be set to a value of 2 to indicate entire success
                        recordingUpdate_stmt = """UPDATE vtiger_contactscf set cf_1469=2 WHERE contactid='%s'""" %(contactid)
                        mycursor.execute(recordingUpdate_stmt)
                        mydb.commit()
                        print('Uploaded Recording')
                    else:
                        #Updating field on crm to be set to a value of 8 indicating failed to upload recording
                        recordingFailed_stmt = """UPDATE vtiger_contactscf set cf_1469=8 WHERE contactid='%s'""" %(contactid)
                        mycursor.execute(recordingFailed_stmt)
                        mydb.commit()
                        print('Uploaded Recording')
    time.sleep(4)











