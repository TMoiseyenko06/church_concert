from flask import Flask
from database import db
from services.personServices import register_user, get_user, check_user
import gunicorn

app = Flask(__name__)
app.config.from_object(f'config.DevelopmentConfig')
db.init_app(app)

with app.app_context():
    db.create_all()
  

@app.route('/person',methods=['POST'])
def add_person():
    return register_user()

@app.route('/person/<int:id>', methods=['GET'])
def get_person(id):
    return get_user(id)

@app.route('/person/check', methods=['GET'])
def check():
    return check_user()


