from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'localhost:3000'


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
    return 'Hi from the App4Apps API'

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