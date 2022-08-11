""""""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

     
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement='ignore_fk')
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email  = db.Column(db.Text, nullable=False, unique=True)
    phone = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_authenticated = False
    is_active = True
    is_anonymous = True


    tasks = db.relationship("Task", backref="users", secondary="assignments")
   

    def __repr__(self):
        
        return f" {self.id} {self.first_name} {self.last_name} "

    #method required by flask-login to get the user's id as a string
    def get_id(self):
        return str(id)

    @classmethod
    def register(cls, pwd, data):

        hashed = bcrypt.generate_password_hash(pwd, rounds=14)

        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        new_user = cls(password=hashed_utf8, **data)

        if new_user:
            return new_user
        else:
            return False

    
    
    
class Task(db.Model):

     
    __tablename__ = "tasks"


    id = db.Column(db.Integer, primary_key=True, autoincrement='ignore_fk')
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    _type = db.Column(db.Enum('personal', 'organizational', name="types"), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    due_time  = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    time_completed = db.Column(db.DateTime, server_onupdate=db.func.now())

    


class Assignment(db.Model):

    __tablename__ = "assignments"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assigner_id = db.Column(db.Integer, nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    remind_asignee = db.Column(db.Boolean, nullable=False, default=True)
    notify_assigner = db.Column(db.Boolean, nullable=False, default=True)
 
    # tasks = db.relationship("Task", backref="assignments", foreign_keys=[Task.created_by])

   