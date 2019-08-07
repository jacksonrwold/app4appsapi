from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ammdwvexmwpbne:5f2956427a0fac13f1197aca445c0acc32ea8ff44f3b6e10d8b48d6d97be5a55@ec2-174-129-226-232.compute-1.amazonaws.com:5432/d8jaih58mshekl'

# commands for remaking the database are "from app import db" and "db.create_all()"

heroku = Heroku(app)
db = SQLAlchemy(app)

class SubmissionData(db.Model):
    __tablename__ = "submissiondata"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    state = db.Column(db.String(30))
    description = db.Column(db.String(200))

    def __init__(self, name, state, description):
        self.name = name
        self.state = state
        self.description = description

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def home():
    return '<h1>Hi from the App4Apps API</h1>'

@app.route('/submissionsdata/input', methods=['POST'])
def dinosaur_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        name = post_data.get('name')    
        state = post_data.get('state')    
        description = post_data.get('description')
        reg = SubmissionData(name, state, description)
        db.session.add(reg)
        db.session.commit()
        return jsonify("Submission Data Posted")
    return jsonify("Failed to post Submission Data")    

@app.route('/submissionsdata', methods=['GET'])
def return_submissiondata():
    all_dinosaurs = db.session.query(SubmissionData.id, SubmissionData.name, SubmissionData.state, SubmissionData.description).all()
    return jsonify(all_dinosaurs)

@app.route('/submissionsdata/<slug>', methods=['GET'])
def return_single_sumbissiondata(slug):
    single_submissiondata = db.session.query(SubmissionData.id, SubmissionData.name, SubmissionData.state, SubmissionData.description).filter(SubmissionData.name == slug).first()
    return jsonify(single_relic)

@app.route('/submissionsdata/<id>', methods=['DELETE'])
def delete_submissiondata(id):
    if request.content_type == 'application/json':
        record = db.session.query(SubmissionData).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("Successfully deleted the suggestion")
    return jsonify("Failed to delete the suggestion")

@app.route('/submissionsdata/<id>', methods=['PUT'])
def update_submissiondata(id):
    if request.content_type == 'application/json':
        name = put_data.get('name')
        record = db.session.query(SubmissionData).get(id)
        record.name = name
        db.session.commit()
        return jsonify("Successfully updated the suggestion")
    return jsonify("Failed to update the suggestion")