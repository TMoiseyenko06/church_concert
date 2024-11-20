from dotenv import load_dotenv
import os

load_dotenv()
URI = os.getenv('URI')

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = URI
    DEBUG = True