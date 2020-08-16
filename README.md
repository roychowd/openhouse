# OpenHouse Test

## Instructions:

In order to run the app follow the command below

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

To run the tests:
python -m pytest
```

```bash
Author: Roy Chowdhury
language: Python 3.7.4
Date created: 15 Aug, 2020
OS used: OSX
```

Note the app is also deployed on heroku which can be accessed via the url:

```bash
https://openhouse-code.herokuapp.com
```

In order to use the api use the following routes :

### Add Logs

```bash

baseurl: localhost:5000 or https://openhouse-code.herokuapp.com
endpoint: /api/log

.. example::
       $ curl -i -X POST -H  "Content-Type: application/json" -d
       '{
        "userId": "ABC123XYZ",
        "sessionId": "XYZ456ABC",
        "actions": [
            {
            "time": "2018-10-18T21:37:30-06:00",
            "type": "NAVIGATE",
            "properties": {
                "pageFrom": "communities",
                "pageTo": "inventory"
            }
            }
        ]  }'  baseUrl/api/log
```

### Get Logs

```bash
baseurl: localhost:5000 or https://openhouse-code.herokuapp.com
/api/log/get?userId=<userId>&type=<type>&start=<date>&end=<date>

Params:

    - userId = userId to query
    - type = type of log that you want to query
    Please either select date as a stand alone argument or start and end to specify a time range
            - date = used to search for exact match with date in format %Y-%m-%dT%H:%M:%S 
            - start = intial date used for range query in format %Y-%m-%dT%H:%M:%S. Need end date argument (start - end )
            - end = intial date used for range query in format %Y-%m-%dT%H:%M:%S. Need start date argument (start - end )

.. example:
    curl baseUrl\userId=ABC123XYZ&type=CLICK&start=2018-10-18T21:37:25&end=2018-10-18T21:37:29

------------------------------------------------------------------------------------
returns logs of the form:

"{
     "actions": [
        {
            "properties": {
                "locationX": 52,
                "locationY": 11
            },
            "time": "2018-10-18T21:37:28-06:00",
            "type": "CLICK"
        },
}"

```

## Additional Questions

Provide your comments on how you would make this solution cloud-scalable.

Since this is a simple app, I would refactor the code to make it follow the [flask factory pattern](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/) in order to scale and structure the flask app for more models, testing, and configruations.

In addition here some other things that I would do:

- I would use gunicorn (wsgi) in order to handle multiple requests instead of running the program through app.py
- Use celery in order to handle longer and non trivial tasks
- Use redis and postgres for faster reads
- Set up a load balancers as we scale
