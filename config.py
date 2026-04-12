import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fridgechef.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'fridgechef-super-secret-key-2024'