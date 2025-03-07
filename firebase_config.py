import json
import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
from dotenv import load_dotenv
import os
import io
load_dotenv(override=True)
# Load Firebase credentials (use a service account for admin actions)
firebase_config = {
    "apiKey": os.environ.get("apiKey"),
    "authDomain": os.environ.get("authDomain"),
    "databaseURL": os.environ.get("databaseURL"),
    "projectId": os.environ.get("projectId"),
    "storageBucket": os.environ.get("storageBucket"),
    "messagingSenderId": os.environ.get("messagingSenderId"),
    "appId": os.environ.get("apiKappIdy"),
}

firebase_creds = os.getenv("FIREBASE_CONFIG")
# Initialize Firebase Admin SDK (for server-side actions)
if not firebase_admin._apps:
    creds_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)

# Initialize Pyrebase (for client-side authentication)
firebase = pyrebase.initialize_app(firebase_config)
auth_client = firebase.auth()
