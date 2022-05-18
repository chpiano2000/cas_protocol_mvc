from flask import render_template, url_for, flash, redirect, request, session
import jwt
from app import app, cas_client
from app.forms import RegistrationForm, LoginForm
from app.controllers.authentication import get_user_by_email, create_user, update_ticket
import urllib.parse

@app.route("/")
@app.route("/home")
def home():
    if 'email' in session:
        return render_template('home.html', title='dashboard')
    else:
        return redirect(url_for("login", service="http://localhost:5000/home"))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        create_user(form.email.data, form.name.data, form.password.data, form.phone.data)
        return redirect(url_for('/cas/login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/cas/login", methods=["GET", "POST"])
def login():

    service = request.args.get('service')
    ticket = request.args.get('ticket')

    if not ticket:
            # No ticket, the request come from end user, send to CAS login
        form = LoginForm()
        if form.validate_on_submit():
            user = get_user_by_email(form.email.data)
            if user:
                session["email"] = form.email.data
                encoded_jwt = jwt.encode({"email": form.email.data}, "secret", algorithm="HS256")
                update_ticket(form.email.data, encoded_jwt)

                decode_service = urllib.parse.unquote(service)
                return redirect(decode_service)
        return render_template('login.html', title='Login', form=form)


    app.logger.debug('ticket: %s', ticket)
    app.logger.debug('next: %s', next)


    payload = jwt.decode(ticket, "secret", algorithms=["HS256"])

    app.logger.debug(
        'CAS verify ticket response: email: %s', payload["email"])
    
    if not payload["email"]:
        return url_for("staging_redirect")
    else:
        session["email"] = payload["email"]
        return url_for('about')


@app.route("/staging/cas/login", methods=['GET', 'POST'])
def staging_redirect():
    service = request.args.get('service')
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user:
            session["email"] = form.email.data
            encoded_jwt = jwt.encode({"email": form.email.data}, "secret", algorithm="HS256")
            return redirect(url_for("login", ticket=encoded_jwt, next=service))
    
    # session["email"] = form.email.data
    # print(session)
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('email')
    return redirect('/cas/login')

