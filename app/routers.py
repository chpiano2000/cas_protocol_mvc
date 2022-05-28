from flask import render_template, redirect, request, session, url_for
import requests
from app import app
from app.config import (
    BASE_URL,
    STAGING_LOGIN_URL,
    STAGING_LOGOUT_URL,
    STAGING_REGISTER_URL,
    STAGING_VALIDATE_URL
)


@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    ticket = request.args.get("ticket")

    if ticket:
        user_info = requests.get(f"{STAGING_VALIDATE_URL}{ticket}")
        if user_info.status_code == 401:
            return redirect(url_for("login"))
        else:
            print(user_info.json().get("userInfo").get("token"))
            return render_template("home.html", user_info=user_info)
    
    else:
        return redirect(url_for("login"))



@app.route("/register", methods=["GET", "POST"])
def register():
    return redirect(f"{STAGING_REGISTER_URL}?service={BASE_URL}/home")


@app.route("/login", methods=["GET"])
def login():
    return redirect(f"{STAGING_LOGIN_URL}?service={BASE_URL}/home")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    url = f"{STAGING_LOGOUT_URL}?service={BASE_URL}/home"
    return redirect(url)
