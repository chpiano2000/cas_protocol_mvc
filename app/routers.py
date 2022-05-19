from datetime import datetime, timedelta
import requests
from flask import render_template, url_for, flash, redirect, request, session, Response
from app import app, BASE_URL
from app.forms import RegistrationForm, LoginForm
from app.controllers.authentication import (
    get_user_by_email,
    create_user,
    update_users,
    remove_ticket,
    get_user_by_ticket,
    refresh_ticket,
)
from app.utils import (
    generate_token,
    url_decoder,
    generate_ticket_body,
    xml_return,
    check_token_expired,
)


@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    ticket = request.args.get("ticket")

    # if request.method == "POST":
    return redirect(url_for("validate", ticket=ticket, service="http://localhost:5000/home"))

    # if "email" in session:
    #     # check if client's token is expired
    #     if check_token_expired(session["expires"]):
    #         return redirect(url_for("login", service="http://localhost:5000/home"))
    #     return render_template("home.html", title="dashboard")
    # else:
    # return redirect(url_for("login", service="http://localhost:5000/home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        create_user(
            form.email.data, form.name.data, form.password.data, form.phone.data
        )
        return redirect(url_for("/cas/login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/cas/login", methods=["GET", "POST"])
def login():

    service = request.args.get("service")

    app.logger.debug("service: %s", service)

    if not service:
        service = "http://localhost:5000/home"

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user:
            session["email"] = form.email.data
            ticket = f"TS-{generate_ticket_body()}"
            update_users(form.email.data, ticket, service)

            return redirect(
                url_for(
                    "home",
                    ticket=ticket
                ),
                code=307,
            )

    return render_template("login.html", title="Login", form=form)


@app.route("/cas/serviceValidate", methods=["POST"])
def validate():
    service = request.args.get("service")
    ticket = request.args.get("ticket")

    app.logger.debug("ticket: %s", ticket)
    app.logger.debug("service: %s", service)

    if request.method == "POST":
        data = get_user_by_ticket(ticket)
        if data:
            data["_id"] = str(data["_id"])
            token = generate_token()
            data["token"] = token

            session["email"] = data["email"]
            session["token"] = token
            session["expires"] = datetime.now() + timedelta(hours=1)

            return redirect(url_for("home"))
        else:
            return {"error": "invalid ticket"}


@app.route("/cas/logout", methods=["GET", "POST"])
def logout():
    remove_ticket(session["email"])
    session.pop("email")
    session.pop("token")
    session.pop("expires")
    return redirect("/cas/login")
