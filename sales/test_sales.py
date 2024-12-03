import pytest
import json
from sales import app

def test_get_available_goods():
    response = app.test_client().get('/get_available_goods')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200

def test_get_good_details():
    response = app.test_client().get('/get_good_details/1')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200

def test_record_sales():
    response = app.test_client().post('/record_sales', data=json.dumps({"user": "DanySolh21",
            "good": "Michelin Soft Sports Tires",
            "quantity": 1}),
    content_type='application/json',)
    
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200 and data == "Purchase Successful"
