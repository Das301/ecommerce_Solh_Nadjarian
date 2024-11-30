import pytest
import json
from reviews import app

def test_submit_review():
    response = app.test_client().post('/submit_review', data=json.dumps({"user": "DanySolh21",
            "password": "24h_LeM@ns",
            "good": "Lug Nuts",
            "rating": 9.5,
            "review": "Very good and reliable."}),
    content_type='application/json',)

    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200 and (data == "Review Submitted Successfully" or data=="Review already exists for this product")


def test_update_review():
    response = app.test_client().put("/update_review", data=json.dumps({"user": "DanySolh21",
            "password": "24h_LeM@ns",
            "good": "Michelin Soft Sports Tires",
            "rating": 9.8,
            "review": "Amazing tires! Great performance and reliability!"}),
    content_type='application/json',)

    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200 and data == "Review updated Successfully"

def test_delete_review():
    response = app.test_client().delete("/delete_review", data=json.dumps({"user": "DanySolh21",
            "password": "24h_LeM@ns",
            "good": "Lug Nuts"}),
    content_type='application/json',)

    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200 and (data == "Review Deleted Successfully" or data=="No reviews exists for this product")

def test_admin_delete_review():
    response = app.test_client().delete("/admin_delete_review", data=json.dumps({"user": "DanySolh21",
            "password": "24h_D@yt0n@",
            "good": "Lug Nuts",
            "admin_user": "Das35"}),
    content_type='application/json',)

    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200 and (data == "Review Deleted Successfully" or data=="No reviews exists for this product")

def test_get_review():
    response = app.test_client().get('/get_review/DanySolh21/Michelin Soft Sports Tires')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200

def test_get_product_review():
    response = app.test_client().get('/get_product_review/Michelin Soft Sports Tires')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200

def test_get_user_review():
    response = app.test_client().get('/get_user_review/DanySolh21')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200

def test_flag_review():
    response = app.test_client().put("/flag_review", data=json.dumps({"user": "DanySolh21",
            "good": "Michelin Soft Sports Tires",
            "flag": 1}),
    content_type='application/json',)

    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code==200 and data == "Flag Changed Successfully"
