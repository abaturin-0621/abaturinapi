import calendar
import time
import pytest
import requests
import json
from pytest_cases import  parametrize_with_cases, case, get_case_id, parametrize
from pytest_schema import  schema, And, Enum, Optional, Or, Regex, SchemaError


def get_url():
    ###TODO  must be config 
    return "http://127.0.0.1:5000"

def get_unique_user():
    """Return username and password by template : user_{timestamp}"""

    unique=calendar.timegm(time.gmtime())
    return  {
              "username":f"user_{unique}", 
              "password":f"password_{unique}"
              }

def get_existing_user():
    ###TODO  must be query db or get request
    """Return  existing username and password """
    
    return  {
              "username":"myusertest1", 
              "password":"myusertest1"
              }

class TestCase:
    """TestCase method: Registration user by username"""

    body={
        "username": get_unique_user()["username"],
        "password": get_unique_user()["password"]
        }
    headers={'Content-Type': 'application/json'}
    parameters=None
    response_schema={
        "message": "The user was created"
        }
    status_code=200 #default value, must be change in  every case function

    #####################################################################################
    def case_positive_request(self):
        """positive:  valid request"""        
        self.status_code=201
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code
    #####################################################################################
    def case_negative_user_already_exists (self):
        """negative :user_already_exists"""  
        self.body={
        "username": get_existing_user()["username"],
        "password": get_existing_user()["password"],
        }
        self.status_code=409
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code    

    #####################################################################################
    @parametrize("body",
                        [
                             {"login": get_unique_user()["username"],"pass": get_unique_user()["password"]}, #invalid body shema parameters
                             {},  #invalid body shema emtpy
                             {"username":"","password": get_existing_user()["password"]}, #invalid body shema no username
                             {"username":get_existing_user()["username"],"password": ""}, #invalid body shema no password
                             {"username":"s","password": get_existing_user()["password"]}, #invalid body shema short username
                             {"username":get_unique_user()["username"],"password": "s"}, #invalid body shema short password
                        ]
                )    
    def case_negative_invalid_body_request(self,body):
        """negative :invalid body""" 
        self.body=body
        self.status_code=400
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code    


    #####################################################################################
    @parametrize("headers",
                        [
                            {},  #invalid headers emtpy
                            
                        ]
                )        
    def case_negative_invalid_headers(self,headers):
        """negative :invalid headers""" 
        self.headers=headers
        self.status_code=400
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code     


#####################################################################################
@parametrize_with_cases("body,headers,parameters,response_schema,status_code", cases=TestCase)
def test_registration_user_by_username(body,headers,parameters,response_schema,status_code,BASEURL):
    data=json.dumps(body)
    url=f"{BASEURL}/registration"
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==status_code, "Invalid response" 
     