"""
"""

from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from models import db, connect_db, User, Assignment, Task
from forms import LoginForm, SignupForm, CreateTaskForm, EditUserForm, EditTaskForm, AssignTaskForm
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from functools import wraps
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID, SECRET_KEY
from flask_debugtoolbar import DebugToolbarExtension
from datetime import timedelta
import os
from twilio.rest import Client
import requests
from urllib.parse import urlparse, urljoin

# -------------------------------------------------------------------------------- Setup and Configurations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///organizations_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# connects db and creates all tables on the db server
connect_db(app)
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please re-login to access this page."
)
login_manager.needs_refresh_message_category = "danger"


USER = current_user
BASE_URL = "https://api.txtlocal.com/send/"


@app.route('/')
def show_homepage():

    return render_template("home.html", current_user=current_user)

# ------------------------------------------------------------------------------------------ User login functions


def admin_required(func):
    @wraps(func)
    def validate_is_admin(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            flash("You must be an admin to access this page", "danger")
            return login_manager.unauthorized()

        return func(*args, **kwargs)

    return validate_is_admin


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    return None


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


# -------------------------------------------------------------------------------------- User-login Routes

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        (user, msg) = User.authenticate(form.username.data, form.password.data)
        if user:
            delta = timedelta(days=30)
            login_user(user, remember=True, duration=delta)
            flash(msg)
            next = request.args.get('next')

            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('show_homepage'))
        else:
            flash(msg)

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
        flash('Signed up successfully.')
        url = url_for('show_homepage')
        return redirect(url)
    else:
        return render_template("login/signup.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(f"{url_for('show_homepage')}")

# ------------------------------------------------------------------------------------------------- User Routes


@app.route("/users", methods=["GET"])
@login_required
def show_all_users():
    all_users = User.query.all()

    return render_template("users/all_users.html", users=all_users, current_user=current_user)


@app.route("/users/<int:id>", methods=["GET"])
@admin_required
def show_user_details(id):
    user = User.query.get_or_404(id)
    tasks = user.tasks

    return render_template("users/user_details.html", user=user, tasks=tasks)


@app.route("/users/<int:id>/my_tasks", methods=["GET"])
@login_required
def show_all_user_tasks(id):
    user = User.query.filter(User.id == id).first()
    
    tasks = user.tasks
    print("*****************",user)
    print("*****************",tasks)

    return render_template("users/all_user_tasks.html", user=user, tasks=tasks)


@app.route("/users/<int:id>", methods=["POST"])
def create_user(id):
    return "You didn't implement me yet!"


@app.route("/users/<int:id>/edit", methods=["GET", "PUT", "PATCH"])
@admin_required
def edit_user(id):
    user = load_user(id)
    form = EditUserForm(obj=user)
    return render_template("users/edit_user.html", form=form, user=user)


@app.route("/users/<int:id>", methods=["DELETE"])
@admin_required
def delete_user(id):
    return "You didn't implement me yet!"


# ------------------------------------------------------------------------------------------------ Task routes

@app.route("/create_task", methods=["GET", "POST"])
@admin_required
def create_task():
    form = CreateTaskForm()
    print(form.due_time.data)
    if form.validate_on_submit():

        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_task = Task(created_by=USER.id, **data)
        db.session.add(new_task)
        db.session.commit()
        flash("New Task Created!", "success")
        return redirect("/")
    return render_template("tasks/create_task.html", form=form)

@app.route("/tasks", methods=["GET"])
def show_all_tasks():
    tasks = Task.query.all()
    return render_template("tasks/all_tasks.html", tasks=tasks)

@app.route("/tasks/<int:id>", methods=["GET"])
def show_task(id):
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>", methods=["POST"])
def post_task(id):
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>", methods=["PUT", "PATCH"])
def edit_task(id):
    task = Task.query.get_or_404(id)
    form = EditTaskForm(obj=task)
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>/completed", methods=["PUT", "PATCH"])
def edit_completed_task(id):
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>/assignments", methods=["PUT", "PATCH"])
def edit_assignment(id):
    
    return "You didn't implement me yet!"

@app.route("/tasks/<int:id>/assign", methods=["GET", "POST"])
@admin_required
def assign_task(id):
    form = AssignTaskForm()
    task = Task.query.get(id)
    form.assignee_id.choices = [(u.id, u.first_name + " " + u.last_name) for u in User.query.all()]

    if form.validate_on_submit():
        form_data = {k:v for k,v in form.data.items() if k != "csrf_token" and k != "assignee_id"}
        data = {"assigner_id" : current_user.id, "task_id" : id, **form_data}
        assignees = form.assignee_id.data
        for assignee in assignees:
            new_assignment = Assignment(assignee_id=assignee, **data)
            print(data)
            print(new_assignment)
            db.session.add(new_assignment)
            db.session.commit()
        flash("Assignment Created!", "success")
        return redirect(url_for('show_all_user_tasks', id=current_user.id))
    return render_template("tasks/create_assignment.html", form=form, task=task)


@app.route("/tasks/upcoming", methods=["GET"])
def show_upcoming_tasks():
    return "You didn't implement me yet!"


@app.route("/tasks/incomplete", methods=["GET"])
def show_incomplete_tasks():
    return "You didn't implement me yet!"


@app.route("/tasks/completed", methods=["GET"])
def show_completed_tasks():
    return "You didn't implement me yet!"


@app.route("/assign", methods=["GET", "POST"])
def assign_task_by_default():
    user_id = current_user.id
    assign_task(user_id, 1)
    return redirect("/")  # (url_for('show_user_details', id=user_id))


# ------------------------------------------------------------------------------------------------------ Reminder routes


@app.route("/remind", methods=["POST", "GET"])
@login_required
def send_sms():

    # Your Account SID from twilio.com/console
    account_sid = ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token = AUTH_TOKEN

    client = Client(account_sid, auth_token)
    notification = client.notify.services(SERVICE_SID) \
        .notifications.create(
        # We recommend using a GUID or other anonymized identifier for Identity
        identity='00000002',
        body='Knok-Knok! You have gotten your first test')
    print(notification.sid)
    return render_template("test.html", display=notification.sid)


@app.route("/remind/daily", methods=["POST", "GET"])
@login_required
def send_daily_reminder():
    return "You didn't implement me yet!"


@app.route("/remind/<task_ids>", methods=["POST", "GET"])
@login_required
def remind_about_tasks(task_ids):
    return "You didn't implement me yet!"


@app.route("/remind/<user_ids>", methods=["POST", "GET"])
@login_required
def remind_users(user_ids):
    return "You didn't implement me yet!"


@app.route("/notify/<int:task_id>", methods=["POST", "GET"])
@admin_required
def notify_admin(task_id):
    return "You didn't implement me yet!"


@app.route("/bind")
@login_required
def setup_binding():

    # Your Account SID from twilio.com/console
    account_sid = ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token = AUTH_TOKEN

    client = Client(account_sid, auth_token)

    binding = client.notify.v1 \
        .services(SERVICE_SID) \
        .bindings \
        .create(
            identity='00000002',
            binding_type='sms',
            address='+12063198779'
        )

    return render_template("test.html", display=binding.sid)


@app.route("/status", methods=['POST'])
def incoming_sms():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)
    logging.info('SID: {}, Status: {}'.format(message_sid, message_status))
    return ('', 204)


# ------------------------------------------------------------------------ For debugging, to be deleted later

def assign_task(user_id, task_id):
    user = load_user(user_id)
    task = Task.query.get(task_id)
    user.tasks.append(task)
    db.session.add(task)
    db.session.commit()


@app.route("/change", methods=["POST", "GET"])
def change_admin_status():
    USER.change_admin()
    db.session.commit()
    flash("Admin status changed", "success")
    return redirect("/")
