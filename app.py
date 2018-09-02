from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# initialize
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppp.db'
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)


# views
@app.route("/")
def index():
    return render_template('index.html', title='Accounting')


@app.route("/record", methods=['POST'])
def add_record():
    req_data = request.form
    name = req_data['name']
    record = Record(name=name)
    db.session.add(record)
    db.session.commit()
    return 'Create Succeeded', 200


@app.route("/record", methods=['GET'])
def get_records():
    records = Record.query.all()
    records_data = [
        {
            'id': record.id,
            'name': record.name,
        }
        for record in records
    ]
    return jsonify(records_data), 200


@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = Record.query.filter_by(id=record_id).first()
    record_data = {
        'id': record.id,
        'name': record.name,
    }
    return jsonify(record_data), 200


@app.route('/record/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    req_data = request.form
    record = Record.query.filter_by(id=record_id).first()
    record.name = req_data['name']
    db.session.add(record)
    db.session.commit()
    return 'Update Succeeded', 200


@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    record = Record.query.filter_by(id=record_id).first()
    db.session.delete(record)
    db.session.commit()
    return 'Delete Succeeded', 200
