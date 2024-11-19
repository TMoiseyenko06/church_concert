from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

def key_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if 'Authorization' in request.headers:
            try:
                key = request.headers['Authorization'].split(" ")[1]
                if key != API_KEY:
                    return jsonify({"error":"api key not correct"}), 401
            except:
                return jsonify({"error":"api key missing"}), 401
        else:
            return jsonify({"error","Api Key Not Found"}), 401
        return f(*args,**kwargs)
    return decorated