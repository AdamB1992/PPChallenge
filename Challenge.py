from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db '
db = SQLAlchemy(app)

#create db model
class Plates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(10), nullable=False)  #max length of plate string 10 chars
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Plates('{self.plate}', '{self.timestamp}')"

@app.route('/plate', methods=['GET','POST'])
def plate():
    if request.method == 'POST':
        try:
            json_data =  request.get_json()
            plate = json_data['plate']
            if valid_plate(plate):
                plate_entry = Plates(plate=plate)
                db.session.add(plate_entry)
                db.session.commit()
                return Response(status=200)

            #if not valid german plate
            else:
                return Response(status=422)

        #catches any errors retrieving malformed json/plate data
        except:
            return Response(status=400)

    #if GET request
    else:
        records = db.session.query(Plates).all()
        record_data = []
        for record in records:
            record_data.append({'plate': record.plate,
                                'timestamp': str(record.timestamp)})
        db_data = json.dumps(record_data, indent=4)   #encoding with set indents
        return db_data

def valid_plate(plate):
    pattern = "^[A-Z]{1,3}\-[A-Z]{1,2}[1-9][0-9]{0,3}"
    prog = re.compile(pattern)
    if prog.fullmatch(plate):    #If the whole string matches the regular expression pattern
        return True
    return False

db.create_all()
