from flask import Flask
from database import db
from services.personServices import register_user, get_user, check_user, confirm_email, confirm_person, get_all, remove_user
import gunicorn
from flask_cors import CORS
from utils.util import key_required

app = Flask(__name__)
app.config.from_object(f'config.DevelopmentConfig')
CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()
  
@key_required
@app.route('/person',methods=['POST'])
def add_person():
    return register_user()

@key_required
@app.route('/person/<int:id>', methods=['GET'])
def get_person(id):
    return get_user(id)

@key_required
@app.route('/person/check', methods=['POST'])
def check():
    return check_user()

@key_required
@app.route('/person/check-email',methods=['POST'])
def check_email():
    return confirm_email()

@key_required
@app.route('/person/confirm',methods=["PUT"])
def confirm():
    return confirm_person()

@key_required
@app.route('/person/get_all',methods=['GET'])
def get_all_users():
    return get_all()

@key_required
@app.route('/person/remove/<int:id>',methods=['DELETE'])
def remove_user_id(id):
    return remove_user(id)