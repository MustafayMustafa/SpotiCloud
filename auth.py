import urllib.parse
import os
import threading
import webbrowser
import secrets
import requests
from flask import Flask, request, redirect
from dotenv import load_dotenv
import secrets

load_dotenv()
app = Flask(__name__)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SK")
redirect_uri = "http://localhost:3000/callback"
scope = "playlist-read-private"


@app.route("/login")
def login():
    print("Authorise Spotify")
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
    }
    auth_request_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(auth_request_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")

    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(token_url, data=data)
    token_info = response.json()
    access_token = token_info.get("access_token")

    return f"Access Token: {access_token}"


def open_browser():
    print("Opening browser to authenticate user")
    webbrowser.open("http://localhost:3000/login")


if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(port=3000, debug=True)
