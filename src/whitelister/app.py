import uuid
from werkzeug.exceptions import HTTPException
import json
import requests
import os
from pathlib import Path
from requests import HTTPError

from flask import Flask, request, abort
from flask_cors import CORS

secret = os.environ["SECRET"]
filepath = Path(os.environ["FILEPATH"])

app = Flask(__name__)

CORS(app)

@app.errorhandler(HTTPException)
def err(error):
    return error.description, error.code

@app.route("/whitelist", methods=["POST"])
def hello_world():
    data = request.get_json()

    r_secret: str = data.get('secret')
    r_username: str = data.get('username')

    if r_secret != secret:
        abort(401, description="Invalid secret")

    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{r_username}")
    try:
        response.raise_for_status()
    except HTTPError:
        abort(422, "Invalid username")
    
    data = response.json()

    id = str(uuid.UUID(data['id']))
    username = data['name']

    with open(filepath, "r+") as file:
        
        fdata = json.load(file)

        for user in fdata:
            if user["uuid"] == id:
                abort(422, "User already added")
        
        fdata.append({"uuid": id, "username": username})
        file.seek(0)
        json.dump(fdata, file, indent=2)
        file.truncate()

    return "Added username"
    

    
