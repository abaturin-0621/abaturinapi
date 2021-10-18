import calendar
import time
import pytest
from pytest_cases.fixture_core2 import fixture
import requests
import json
from pytest_cases import  parametrize_with_cases, case, get_case_id, parametrize,fixture_ref
from pytest_schema import  schema, And, Enum, Optional, Or, Regex, SchemaError
from utils.utils import *

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


class TestCase():
    """TestCase method: Registration user by username"""
      
    body={
        "username": "username",
        "password": "password"
        }
    headers={'Content-Type': 'application/json'}
    parameters=None
    response_schema={
        "message": "The user was created"
        }
    status_code=200 #default value, must be change in  every case function

  


    #####################################################################################
    def case_positive_request(self,UNIQ_USER): ##UNIQ_USER fixture ,  see  conftest.py
        """positive:  valid request"""   
        self.body={
        "username": UNIQ_USER["username"],
        "password": UNIQ_USER["password"]
        }     
        self.status_code=201
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code
    #####################################################################################
    def case_negative_user_already_exists (self,EXISTING_USER):##EXISTING_USER fixture ,  see  conftest.py
        """negative :user_already_exists"""  
        self.body={
        "username": EXISTING_USER["username"],
        "password": EXISTING_USER["password"],
        }
        self.status_code=409
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code    

    #####################################################################################
    @parametrize("body",
                        [
                           {},  #invalid body shema emtpy
                            
                        ]
                )    
    def case_negative_empty_body_request(self,body):
        """negative :empty body""" 
        self.body=body
        self.status_code=400
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code   
    
    ######################################################################################
    @parametrize("username",[VALID_NONE,VALID_BOOLEAN,VALID_NUMBER_INT,VALID_NUMBER_FLOAT,VALID_SLASH,VALID_SHORT_STRING,VALID_LONG_STRING,VALID_QUOTE])    
    @parametrize("password",[VALID_NONE,VALID_BOOLEAN,VALID_NUMBER_INT,VALID_NUMBER_FLOAT,VALID_SLASH,VALID_SHORT_STRING,VALID_LONG_STRING,VALID_QUOTE])   
    def case_negative_invalid_body_request(self,username,password):
        """negative :invalid body""" 
        self.body["username"]=username
        self.body["password"]=password
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
    print(data)
    print(headers)
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==status_code, "Invalid response" 
    
     