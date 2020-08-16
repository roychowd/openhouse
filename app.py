from flask import Flask, render_template, request, jsonify, abort
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_migrate import Migrate
import uuid
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Log(db.Model):
    id = db.Column(db.String, primary_key=True)
    userId = db.Column(db.String)
    time = db.Column(db.DateTime)
    log_type = db.Column(db.String)
    log_data = db.Column(db.String)

    def __repr__(self):
        return '<Log_Type %s>' % self.log_type


@app.route('/api/log', methods=['POST'])
def add_log():
    """
    Adds Logs to database
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
        ]  }'  http://localhost:5000/api/log
    """
    if request.method == "POST":
        # extract json from post request
        req_data = request.get_json()
        # get data and put in database
        user_id = req_data["userId"]
        actions = req_data["actions"]
        for item in actions:
            time = item["time"]
            log_type = item["type"]
            log = Log(id=str(uuid.uuid1()), userId=user_id, time=datetime.strptime(time[:-6], "%Y-%m-%dT%H:%M:%S"), log_type=log_type,
                      log_data=json.dumps(item))
            db.session.add(log)

        db.session.commit()
        return "Success"


@app.route("/api/log/get", methods=["GET"])
def get_logs():
    """
    An endpoint that retreives logs from one of the following patameters (or a combination):
        - userId = userId to query
        - type = type of log that you want to query
    Please either select date as a stand alone argument or start and end to specify a time range
        - date = used to search for exact match with date in format %Y-%m-%dT%H:%M:%S (optional)
        - start = intial date used for range query in format %Y-%m-%dT%H:%M:%S. Need end date argument (start - end ) 
        - end = intial date used for range query in format %Y-%m-%dT%H:%M:%S. Need start date argument (start - end ) 
    .. example::
       $ curl http://localhost:5000/api/log/get?userId=<userId>&type=<type>&start=<date>&end=<date> -X GET \
    """
    if request.method == "GET":
        # get all params from query string
        userId = request.args.get("userId",  default=None, type=str)
        log_type = request.args.get("type",  default=None, type=str)
        date = request.args.get("date",  default=None, type=str)
        start = request.args.get("start",  default=None, type=str)
        end = request.args.get("end",  default=None, type=str)
        isRange = start and end
        if isRange:
            # format start and end
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        # add kwargs for sqlalcehmy db lookup
        kwargs = {'userId': userId}
        if log_type:
            kwargs["log_type"] = log_type
        if date:
            kwargs["date"] = date
        # get all logs with conditions
        logs = Log.query.filter_by(**kwargs).all()
        actions = []
        if len(logs) == 0:
            # no logs found
            return abort(404)
        for log in logs:
            if isRange:
                # check for time range
                if log.time <= end and log.time >= start:
                    actions.append(json.loads(log.log_data))
            else:
                # no range query so just add to response
                actions.append(json.loads(log.log_data))
        if len(actions) == 0:
            return abort(404)
        return jsonify({
            "actions": actions
        })


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
