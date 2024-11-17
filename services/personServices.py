from database import db, Base
from flask import request, jsonify
from middleware.schemas.person_schema import person_schema, hash_schema
from marshmallow import ValidationError
from sqlalchemy.orm import Session
from models.person import Person
import hashlib
from sqlalchemy import select



def register_user():
    try:
        user_data = person_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages)
    
    with Session(db.engine) as session:
        with session.begin():
            email = user_data['email'].encode()
            new_person = Person(
                first_name = user_data['first_name'],
                last_name = user_data['last_name'],
                email = user_data['email'],
                plus_hash = hashlib.sha1(email).hexdigest() 
            )
            session.add(new_person)
            session.commit()
            

def get_user(id):
    with Session(db.engine) as session:
        with session.begin():
            user = session.get(Person, id)
            return person_schema.jsonify(user)
        

def check_user():
    with Session(db.engine) as session:
        with session.begin():
            hash = hash_schema.load(request.json)['plus_hash']
            person = session.execute(select(Person).where(Person.plus_hash == hash)).scalars().first()
            if person:
                return person_schema.jsonify(person)
            else:
                 return jsonify({"error":"person_not_exist"})

