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
    # session = db.Column(db.)
    log_type = db.Column(db.String)
    log_data = db.Column(db.String)

    def __repr__(self):
        return '<Log_Type %s>' % self.log_type



@app.route('/')
def index():
    return jsonify({'hello': 'world'})
    
@app.route('/api/log', methods=['POST'])
def add_log():
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
            # print("LOG userid " ,log.userId, "\n Log time " log.time, "\n Log type" , log.log_type, "\n log data",log.log_data)
            db.session.add(log)

        db.session.commit()
        return "Success"



@app.route("/api/log/get", methods=["GET"])
def get_logs():
    if request.method == "GET":
        userId = request.args.get("userId",  default=None, type=str)
        log_type = request.args.get("type",  default=None, type=str)
        date = request.args.get("date",  default=None, type=str)
        start = request.args.get("start",  default=None, type=str)
        end = request.args.get("end",  default=None, type=str)
        isRange = start and end
        if isRange:
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        kwargs = {'userId': userId}
        if log_type:
            kwargs["log_type"] = log_type
        if date:
            kwargs["date"] = date
        logs = Log.query.filter_by(**kwargs).all()
        actions = []
        if len(logs) == 0:
            return abort(404)
        for log in logs:
            if isRange:
                if log.time <= end and log.time > start:
                    actions.append(json.loads(log.log_data))
            else:
                actions.append(json.loads(log.log_data))
        if len(actions) == 0:
            return abort(404)
        return jsonify({
            "actions": actions
        })


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
