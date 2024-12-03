from database import db, Base
from flask import request, jsonify
from middleware.schemas.person_schema import person_schema, hash_schema, email_schema, persons_schema
from marshmallow import ValidationError
from sqlalchemy.orm import Session
from models.person import Person
import hashlib
from sqlalchemy import select, exists
import qrcode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import io
from email.mime.image import MIMEImage
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()



def register_user():
    try:
        user_data = person_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages)
    
    with Session(db.engine) as session:
        with session.begin():
            try:
                email_exists = session.query(exists().where(Person.email == user_data['email'])).scalar()
                if email_exists:
                    return jsonify({"error":"error"}), 400
                
                email = user_data['email'].encode()
                new_person = Person(
                    first_name = user_data['first_name'],
                    last_name = user_data['last_name'],
                    email = user_data['email'],
                    plus_hash = hashlib.sha1(email).hexdigest() 
                )
                session.add(new_person)
                send_email(new_person.plus_hash, new_person.email,new_person.first_name,new_person.last_name)
                session.commit()
                return jsonify({"message":"person added"}),200
            except:
                return jsonify({"error":"error"}), 400
            

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

def send_email(plus_hash, email,first,last):
    code = qrcode.make(plus_hash)
    img_io = io.BytesIO()
    code.save(img_io)
    img_io.seek(0)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    password = os.getenv('PASS_EMAIL')
    sender = 'radvestyouth@gmail.com'
    

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = f'Concert Ticket for {first}'

    msg_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Concert Ticket</title>
        <style>
            /* This is a fallback for email clients that support inline styles */
            .content-container {
                background-image: url('https://i.imgur.com/Z7D5Lvs.jpeg');
                background-size: cover;
                background-repeat: no-repeat;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }

            .overlay {
                background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black overlay */
                border-radius: 10px;
                padding: 20px;
            }

            /* Ensure the content stays on top */
            .content {
                position: relative;
                z-index: 2;
                text-align: center;
                color: #ffffff;
            }
            a:link, a:visited {
                color: #b0151e;
            }
            h1 {
                font-family: 'Brush Script MT', cursive;
                color: #fff;
                font-size: 40px;
                text-decoration: underline;
                text-decoration-color: #b0151e;
            }

            p {
                font-size: 16px;
            }

            .qr-code {
                border: 15px solid #b0151e;
                border-radius: 10px;
            }
        </style>
    </head>
    <body style="background-color: #414b43; font-family: 'Sofia'; margin: 0; padding: 0; color: #333;">

        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #414b43; padding: 20px;">
            <tr>
                <td>
                    <table role="presentation" width="100%" max-width="600px" cellspacing="0" cellpadding="0" class="content-container">
                        <tr>
                            <td class="overlay">
                                <div class="content">
                                    <div style="text-align: center;">
                                        <img src="https://i.imgur.com/ILkltII.png" width="100" alt="QR Code">
                                    </div>
                                    <h1>You're All Set for the Christmas Concert!</h1>
                                    <div style="padding: 10px;">
                                        <img src="cid:picture@example.com" width="300" height="300" alt="QR Code" class="qr-code">
                                    </div>
                                    <p><strong>Event:</strong> Radvest Youth Christmas Concert</p>
                                    <p><strong>Date:</strong> December 21, 2024</p>
                                    <p><strong>Location:</strong><a href="https://maps.app.goo.gl/3tqFyzfBB1JsK87U8">Church of Wonderful News</a></p>
                                    <p style="font-size: 12px;">If you have any questions, please contact our support team.</p>
                                    <p style="font-size: 12px;">© 2024 Radvest Youth. All rights reserved.</p>
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

    </body>
    </html>

    '''

    msg.attach(MIMEText(msg_content, 'html'))

    
    image = MIMEImage(img_io.read(), _subtype="png")
    image.add_header('Content-ID', '<picture@example.com>')
    image.add_header('Content-Disposition', 'inline', filename='image.jpg')
    msg.attach(image)
    try:
        s.login(sender, password)
        s.sendmail(sender, email, msg.as_string())
        s.close()
        return jsonify({"message":"Registered and email sent"})
    except:
        return jsonify({"error":"email not sent"})
    

def confirm_person():
    hash = hash_schema.load(request.json)['plus_hash']
    with Session(db.engine) as session:
        with session.begin():
            person = session.execute(select(Person).where(Person.plus_hash == hash)).scalars().first()
            if person.checked_in == False:
                person.checked_in = True
                session.commit()

                return jsonify({"message":"OK"}),200            
            return jsonify({"error":"already checked in"}),401
            
            

def confirm_email():
    email = email_schema.load(request.json)['email']
    with Session(db.engine) as session:
        with session.begin():
            email_exists = session.query(exists().where(Person.email == email)).scalar()
            if email_exists:
                return jsonify({"error":"email already exists"}), 400
            else:
                return jsonify({"message":"OK"}), 200
            
def get_all():
    with Session(db.engine) as session:
        with session.begin():
            people = session.execute(select(Person)).scalars().all()
            return persons_schema.jsonify(people)

def remove_user(id):
    with Session(db.engine) as session:
        with session.begin():
            try:
                person = session.get(Person,id)
                session.delete(person)
                return jsonify({"deleted":f"user {id}"})
            except:
                return jsonify({"error":"user not found"})