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


def get_existing_token():
    ###TODO  must be query db or get request
    """Return  existing user token and item name """
    body={ 
        "username":"myusertest1", 
        "password":"myusertest1"
    }
    headers={'Content-Type': 'application/json'}
    data=json.dumps(body)
    url=f"{get_url()}/login"
    try:
        response = requests.request(method="POST",url=url,data=data,headers=headers)
    except Exception:
         assert 0, "Error get existing token"

    return  {
              "token":response.json()["token"], 
              "name":"myobject1"
        }

def get_invalid_token():
    ###TODO  must be query db or get request
    """Return no existing user token and item name """
    return  {
              "token":"token_invalid", 
              "name":"myobject1"
        }        

class TestCase:
    """TestCase method: Create item by name item and token user"""

    body={
        "token": get_existing_token()["token"],
        "name": get_existing_token()["name"],
    }
    headers={'Content-Type': 'application/json'}
    parameters=None
    response_schema={
            "message": "The user was autorised",
            "token": str

        } 
    status_code=200 #default value, must be change in  every case function

    #####################################################################################
    def case_positive_request(self):
        """positive:  valid request"""        
        self.status_code=201
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code
    #####################################################################################
    def case_negative_invalid_token(self):
        """negative :user_already_exists"""  
        self.body={
        "token": get_invalid_token()["token"],
        "name": get_invalid_token()["name"],
        }
        self.status_code=401
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code    

    #####################################################################################
    @parametrize("body",
                        [
                            
                             {},  #invalid body shema emtpy
                             
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
def test_create_item_by_name_item_and_token_user(body,headers,parameters,response_schema,status_code):
    data=json.dumps(body)
    url=f"{get_url()}/items/new"
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==status_code, "Invalid response" 
     