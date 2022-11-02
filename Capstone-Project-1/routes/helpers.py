from app import app
from routes.login import admin_required
from models import db, User,  Task
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import current_user
from twilio.rest import Client


@app.route("/bind")
@admin_required
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


def assign_task(user_id, task_id):
    user = load_user(user_id)
    task = Task.query.get(task_id)
    
    db.session.add(task)
    db.session.commit()


# @app.route("/change", methods=["POST", "GET"])
# def change_admin_status():
#     current_user.change_admin()
#     db.session.commit()
#     flash("Admin status changed", "success")
#     return redirect("/")