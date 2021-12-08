# Node.js Rest API Using MySQL and JWT Authentication Integrated with VTiger CRM
#
# This project also contains 2 python files called importLeads.py & putLeads_postRecording.py

#importLeads.py is responsible for obtaining any new leads stored in the database connected with the NodeJs API and then importing it into the VTiger CRM through the CRM's built in API service. 

# putLeads_postRecording.py is responsible for obtaining any leads that have been actioned to sale that needs to be sent back to a third party with the updated information through a patch request. Once done, it will then retrieve the call recording stored in a folder labeled as the order id and post that audio file to the partners API.



## Project setup
```
npm install
```

### Run
```
node server.js
```
