from app import app
from routes.helpers import admin_required, is_safe_url
from models import db, User
from forms import LoginForm, SignupForm
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from functools import wraps
from datetime import timedelta




# -------------------------------------------------------------------------------------- User-login Routes
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please re-login to access this page."
)
login_manager.needs_refresh_message_category = "danger"


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        (user, msg) = User.authenticate(form.username.data, form.password.data)
        if user:
            delta = timedelta(days=30)
            login_user(user, remember=True, duration=delta)
            flash(msg, "success")
            next = request.args.get('next')

            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('show_homepage'))
        else:
            flash(msg, "danger")

    return render_template("login/login.html", form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items(
        ) if k != "password" and k != "csrf_token"}
        new_user = User.register(form.password.data, data)
        db.session.add(new_user)
        db.session.commit()

        delta = timedelta(days=30)
        login_user(new_user, remember=True, duration=delta)
        flash('Signed up successfully!', "success")
        url = url_for('show_all_users')
        return redirect(url)
    else:
        return render_template("login/signup.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(f"{url_for('show_homepage')}")


# ------------------------------------------------------------------------------------------ User login functions

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    return None


