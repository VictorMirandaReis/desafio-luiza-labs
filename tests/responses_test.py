import pytest
from fastapi.responses import JSONResponse
from src.api.utils.responses import success_response

def test_success_response_only_message():
    message = "Operation successful"
    response = success_response(message)
    
    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    
    content = response.body.decode("utf-8")
    assert f'"message":"{message}"' in content
    
    assert content.count(":") == 1

def test_success_response_with_data():
    message = "Data fetched"
    data = {"user_id": 42, "name": "Victor"}
    
    response = success_response(message, data)
    
    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    
    content = response.body.decode("utf-8")
    
    assert f'"message":"{message}"' in content
    assert '"user_id":42' in content
    assert '"name":"Victor"' in content

def test_success_response_with_empty_data():
    message = "Empty data test"
    data = {}
    
    response = success_response(message, data)
    
    content = response.body.decode("utf-8")
    
    assert f'"message":"{message}"' in content
    assert content.count(":") == 1
