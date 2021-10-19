import calendar
import time
import pytest
import requests
import json
from pytest_cases import  parametrize_with_cases, case, get_case_id, parametrize
from pytest_schema import  schema, And, Enum, Optional, Or, Regex, SchemaError

       


class TestCase:
    """TestCase method: Delete item by item id and token user"""

    body={"token":  "token"}
    headers={'Content-Type': 'application/json'}
    parameters={"id":"item_id"} #default value, must be change in  every case function
    response_schema={
            "message": "Item delete",
        } 
    status_code=200 #default value, must be change in  every case function

    #####################################################################################
    def case_positive_request(self,EXISTING_ITEM):
        """positive:  valid request"""    
        self.body={
        "token": EXISTING_ITEM["token"],
        
        }    
        self.parameters={"id":EXISTING_ITEM["item_id"]}
        self.status_code=200
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code
    #####################################################################################
    def case_negative_invalid_token(self,NO_EXISTING_TOKEN,EXISTING_ITEM):
        """negative :invalid token"""  
        self.body={
        "token": NO_EXISTING_TOKEN["token"],
        }
        self.parameters={"id":EXISTING_ITEM["item_id"]}
        self.status_code=401
        return self.body,self.headers,self.parameters,self.response_schema,self.status_code    

    #####################################################################################
    def case_negative_invalid_item(self,NO_EXISTING_ITEM,EXISTING_ITEM):
        """negative :invalid item"""  
        self.body={
            "token": EXISTING_ITEM["token"],
            }      
        self.parameters["id"]=NO_EXISTING_ITEM["item_id"]
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
def test_delete_item_by_item_id_and_token_user(body,headers,parameters,response_schema,status_code,BASEURL):
    data=json.dumps(body)
    id=parameters["id"]
    url=f"{BASEURL}/items/{id}"
    response = requests.request(method="DELETE",url=url,data=data,headers=headers)
    assert response.status_code==status_code, "Invalid response" 
     