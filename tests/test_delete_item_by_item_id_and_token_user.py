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
def get_no_existing_item():
    ###TODO  must be query db or get request
    """Return no existing item"""
    return  {
              "item_id":"100", 
        }   

def get_existing_item():
    ###TODO  must be query db or get request
    """Return existing item"""
    body={ 
        "username":"myusertest1", 
        "password":"myusertest1"
    }
    headers={'Content-Type': 'application/json'}
    data=json.dumps(body)
    url=f"{get_url()}/login"
    try:
        response = requests.request(method="POST",url=url,data=data,headers=headers)
        token=response.json()["token"]
    except Exception:
         assert 0, "Error get existing token"


    body={ 
        "token":response.json()["token"], 
        "name":"myobject1"
    }
    headers={'Content-Type': 'application/json'}
    data=json.dumps(body)
    url=f"{get_url()}/items/new"
    try:
        response = requests.request(method="POST",url=url,data=data,headers=headers)
        
    except Exception:
         assert 0, "Error create new item"     



    return  {
              "item_id":response.json()["id"],
              "token":token 
        }          


class TestCase:
    """TestCase method: Delete item by item id and token user"""

    body={
        "token": get_existing_item()["token"],
        
    }
    headers={'Content-Type': 'application/json'}
    parameters={"id":get_existing_item()["item_id"]} #default value, must be change in  every case function
    response_schema={
            "message": "Item delete",
        } 
    status_code=200 #default value, must be change in  every case function

    #####################################################################################
    def case_positive_request(self):
        """positive:  valid request"""        
        self.status_code=200
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code
    #####################################################################################
    def case_negative_invalid_token(self):
        """negative :invalid token"""  
        self.body={
        "token": get_invalid_token()["token"],
        }
        self.status_code=401
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code    

    #####################################################################################
    def case_negative_invalid_item(self):
        """negative :invalid item"""  
        self.parameters["id"]=get_no_existing_item()["item_id"]
        self.status_code=404
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
def test_delete_item_by_item_id_and_token_user(body,headers,parameters,response_schema,status_code):
    data=json.dumps(body)
    id=parameters["id"]
    url=f"{get_url()}/items/{id}"
    response = requests.request(method="DELETE",url=url,data=data,headers=headers)
    assert response.status_code==status_code, "Invalid response" 
     