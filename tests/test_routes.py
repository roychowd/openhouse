
import json
import os


def test_post_route(app, client):
    del app
    url = '/api/log'
    mock_request_data = {
        "userId": "ABC123XYZ",
        "sessionId": "XYZ456ABC",
        "actions": [
            {
                "time": "2018-10-18T21:37:28-06:00",
                "type": "CLICK",
                "properties": {
                    "locationX": 52,
                    "locationY": 11
                }
            },
            {
                "time": "2018-10-18T21:37:30-06:00",
                "type": "VIEW",
                "properties": {
                    "viewedId": "FDJKLHSLD"
                }
            },
            {
                "time": "2018-10-18T21:37:30-06:00",
                "type": "NAVIGATE",
                "properties": {
                    "pageFrom": "communities",
                    "pageTo": "inventory"
                }
            }
        ]
    }
    response = client.post(url, data=json.dumps(mock_request_data), headers={
                           "Content-Type": "application/json"})
    assert response.status_code == 200


def test_get_route(app, client):
    del app
    url = '/api/log/get?userId=ABC123XYZ&start=2018-10-18T21:37:25&end=2018-10-18T21:37:29'
    response = client.get(url)
    print(response)
    # if nothing returns we expect a 404
    assert response.status_code == 200

    url = '/api/log/get?userId=ABC123XYZ'
    response = client.get(url)

    assert response.status_code == 200

    url = '/api/log/get?userId=fsdf'
    response = client.get(url)
    assert response.status_code == 404

    
