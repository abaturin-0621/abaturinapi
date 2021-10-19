import calendar
import time
import pytest
import json
import requests

def pytest_addoption(parser):
    parser.addoption("--baseUrl", action="store", default="http://127.0.0.1:5000",help="baseUrl")



@pytest.fixture()
def get_base_url(pytestconfig):
    return pytestconfig.option.baseUrl          


@pytest.fixture()
def BASEURL(get_base_url):
    return get_base_url  

@pytest.fixture()
def UNIQ_USER():
    """Return username and password by template : user_{timestamp}"""
    unique=calendar.timegm(time.gmtime())
    return  {
              "username":f"user_{unique}", 
              "password":f"password_{unique}"
              }              

@pytest.fixture()
def SENDER_USER():
    """Return username and password by template : sender_{timestamp}"""
    unique=calendar.timegm(time.gmtime())
    return  {
              "username":f"sender_{unique}", 
              "password":f"password_{unique}"
              }        

@pytest.fixture()
def RECEIVER_USER():
    """Return username and password by template : receiver_{timestamp}"""
    unique=calendar.timegm(time.gmtime())
    return  {
              "username":f"receiver_{unique}", 
              "password":f"password_{unique}"
              }    

@pytest.fixture()
def EXISTING_USER():
    """Return existing username and password by template : receiver_{timestamp}"""
    
    return  {
              "username":"myusertest1", 
              "password":"myusertest1"
              }                

@pytest.fixture()
def NO_EXISTING_USER():
    """Return existing username and password by template : receiver_{timestamp}"""
    
    return  {
              "username":"myusertestnone", 
              "password":"myusertestnone"
              }                
@pytest.fixture(scope="function")
def EXISTING_TOKEN(BASEURL):
    """Return  existing user token and item name """
    body={ 
        "username":"myusertest1", 
        "password":"myusertest1"
    }
    headers={'Content-Type': 'application/json'}
    data=json.dumps(body)
    url=f"{BASEURL}/login"
    try:
        response = requests.request(method="POST",url=url,data=data,headers=headers)
        token=response.json()["token"]
    except Exception:
         assert 0, "Error get existing token"

    return  {
              "token":token, 
              "name":"myobject1"
        }              
@pytest.fixture()
def NO_EXISTING_TOKEN():
    """Return no existing user token and item name """
    return  {
              "token":"token_invalid", 
              "name":"myobject1"
        }            

@pytest.fixture()
def EXISTING_ITEM(BASEURL):
    """Return existing item"""
    body={ 
        "username":"myusertest1", 
        "password":"myusertest1"
    }
    headers={'Content-Type': 'application/json'}
    data=json.dumps(body)
    url=f"{BASEURL}/login"
    try:
        response = requests.request(method="POST",url=url,data=data,headers=headers)
        token=response.json()["token"]
    except Exception:
         assert 0, "Error get existing token"


    body={ 
        "token":token, 
        "name":"myobject1"
    }
    headers={'Content-Type': 'application/json'}
    data=json.dumps(body)
    url=f"{BASEURL}/items/new"
    try:
        response = requests.request(method="POST",url=url,data=data,headers=headers)
        item_id=response.json()["id"]
        
    except Exception:
         assert 0, "Error create new item"     



    return  {
              "item_id":item_id,
              "token":token 
        }      
@pytest.fixture()
def NO_EXISTING_ITEM():
    ###TODO  must be query db or get request
    """Return no existing item"""
    return  {
              "item_id":"100", 
        }            
           