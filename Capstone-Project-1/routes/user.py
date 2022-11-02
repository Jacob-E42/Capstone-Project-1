from app import app


from routes.login import admin_required
from routes.reminder import remind_user
from models import db, connect_db, User, Assignment, Task
from forms import LoginForm, SignupForm, CreateTaskForm, EditUserForm, EditTaskForm, AssignUserForm, AssignTaskForm
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID, SECRET_KEY
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension
from datetime import timedelta
import requests
from urllib.parse import urlparse, urljoin
from twilio.rest import Client
import os
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


@app.route("/users/my_tasks", methods=["GET"])
@login_required
def show_all_user_tasks():
    user = User.query.get(current_user.id)
    tasks = user.tasks

    return render_template("users/all_user_tasks.html", user=user, tasks=tasks)


# @app.route("/users/<int:id>", methods=["POST"])
# def create_user(id):
#     return "You didn't implement me yet!"


@app.route("/users/<int:id>/edit", methods=["GET", "POST", "PUT", "PATCH"])
@admin_required
def edit_user(id):
    user = load_user(id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        for (k, v) in data.items():
            setattr(user, k, v)
        db.session.add(user)
        db.session.commit()
        flash("User updated!", "success")
        return redirect(url_for('show_user_details', id=user.id))

    return render_template("users/edit_user.html", form=form, user=user)


@app.route("/users/<int:id>", methods=["POST", "DELETE"])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted!", "danger")
    return redirect(url_for('show_all_users'))


@app.route("/users/<int:id>/assign", methods=["GET", "POST"])
@admin_required
def assign_task_to_user(id):
    form = AssignTaskForm()
    user = User.query.get(id)
    assigned_task_ids = [task.id for task in user.tasks]
    form.task_id.choices = [(task.id, task.title) for task in Task.query.all()]

    if form.validate_on_submit():
        form_data = {k: v for k, v in form.data.items() if k !=
                     "csrf_token" and k != "task_id"}
        data = {"assigner_id": current_user.id, "assignee_id": id, **form_data}
        task_choices = form.task_id.data

        for task in task_choices:
            if (task in task_choices and task not in assigned_task_ids) or len(assigned_task_ids) == 0:
                new_assignment = Assignment(task_id=task, **data)
                db.session.add(new_assignment)
                db.session.commit()
                flash("Assignment Created!", "success")
        for task in assigned_task_ids:
            if task not in task_choices:
                assignment = Assignment.query.filter_by(task_id=task).first()
                db.session.delete(assignment)
                db.session.commit()
                flash("Assignment deleted", "success")
        return redirect(url_for('show_all_tasks'))
    return render_template("users/create_assignment.html", form=form, user=user)