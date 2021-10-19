import calendar
import time
import pytest
import requests
import json
from pytest_cases import  parametrize_with_cases, case, get_case_id, parametrize
from pytest_schema import  schema, And, Enum, Optional, Or, Regex, SchemaError


def get_url():
    ###TODO  must be config 
    return "http://127.0.0.1:5000/api"

def get_unique_user(prefix=None):
    """Return username and password by template : user_{timestamp}"""

    unique=calendar.timegm(time.gmtime())
    return  {
              "username":f"{prefix}_user_{unique}", 
              "password":f"{prefix}_password_{unique}"
              }


def test_integration_test(BASEURL):
    ###Регистрируем пользователя получателя
    ########Registration################
    userreceiver=get_unique_user("rec")["username"]
    userreceiver_password=get_unique_user("rec")["password"]
    body={
        "username":userreceiver,
        "password":userreceiver_password

    }
    headers={'Content-Type': 'application/json'}
    data=json.dumps(body)
    url=f"{BASEURL}/registration"
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==201, "Invalid response" 

    ###Регистрируем пользователя отправителя
    ########Registration################
    username=get_unique_user("snd")["username"]
    password=get_unique_user("snd")["password"]
    body={
        "username":username,
        "password":password

    }
    
    data=json.dumps(body)
    url=f"{BASEURL}/registration"
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==201, "Invalid response" 

    ###Выполяем вход пользователем отправителем
    ########login################
    body={
        "username":username,
        "password":password

    }
    data=json.dumps(body)
    url=f"{BASEURL}/login"
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==200, "Invalid response"
    ###Создаем объект пользователя отправителя
    ########items/new################
    token=response.json()["token"]
    name="object"
    body={
        "token":token,
        "name":name

    }
    data=json.dumps(body)
    url=f"{BASEURL}/items/new"
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==201, "Invalid response"

    ###Проверяем  объект в списке объектов пользователя отправителя
    ########items################
    item_id=response.json()["id"]
    body={
        "token":token,
    }
    data=json.dumps(body)
    url=f"{BASEURL}/items"
    response = requests.request(method="GET",url=url,data=data,headers=headers)
    assert response.status_code==200, "Invalid response"
    item={'id': item_id, 'name': name}
    assert item in response.json()["result"],"No item in list item"

    ###Отправлеям объект пользователю получателю
    ########items/send################
    body={
        "token":token,
        "username":userreceiver,
        "id":item_id
    }
    print(body)
    data=json.dumps(body)
    url=f"{BASEURL}/send"
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==200, "Invalid response"

    ###Переходим по ссылке
    link=response.json()["link"]
    body={}
    print(link)
    data=json.dumps(body)
    url=f"{link}"
    response = requests.request(method="GET",url=url,data=data,headers=headers)
    assert response.status_code==200, "Invalid response"

    ### Выполняем вход под пользователем получателем 
    ########login user receiver################
    body={
        "username":userreceiver,
        "password":userreceiver_password

    }
    data=json.dumps(body)
    url=f"{BASEURL}/login"
    response = requests.request(method="POST",url=url,data=data,headers=headers)
    assert response.status_code==200, "Invalid response"
    
    ### Проверяем объект в списке объектов получателя
    ########list items receivers################
    token=response.json()["token"]
    body={
        "token":token,
    }
    data=json.dumps(body)
    url=f"{BASEURL}/items"
    response = requests.request(method="GET",url=url,data=data,headers=headers)
    assert response.status_code==200, "Invalid response"
    item={'id': item_id, 'name': name}
    assert item in response.json()["result"],"No item in list item"

    ##Удаляем объект из списка объектов получателя 
    ########delete items receivers################
    body={
        "token":token,
    }
    data=json.dumps(body)
    url=f"{BASEURL}/items/{item_id}"
    response = requests.request(method="DELETE",url=url,data=data,headers=headers)
    assert response.status_code==200, "Invalid response"

    ##Проверяем что объекта нет
    ########delete items receivers################
    body={
        "token":token,
    }
    data=json.dumps(body)
    url=f"{BASEURL}/items/{item_id}"
    response = requests.request(method="DELETE",url=url,data=data,headers=headers)
    assert response.status_code==404, "Invalid response"
 

