from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    clients = db.relationship("Clients", backref="owner", lazy=True)

    def __repr__(self):
        return f"User({self.id}, username={self.username}, email={self.email})"

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    note = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    project = db.relationship("Project", backref="client", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"Clients({self.id}, name={self.name}, email={self.email}, phone={self.phone})"
    
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date)
    status = db.Column(db.String(50), nullable=False, default="pending")
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)

    tasks = db.relationship("Task", backref="project", cascade="all, delete-orphan", passive_deletes=True, lazy=True)
    invoice = db.relationship("Invoice", backref="project", uselist=False)

    def __repr__(self):
        return f"Project({self.id}, title={self.title}, description={self.description}, start_date={self.start_date}, deadline={self.deadline}, status={self.status}, client_id={self.client_id})"
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="todo")
    due_date = db.Column(db.Date, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE", name="fk_task_project_id"), nullable=False)

    def __repr__(self):
        return f"Task({self.id}, title={self.title}, status={self.status}, due_date={self.due_date})"
    
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="unpaid")
    paystack_reference  = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    def __repr__(self):
        return f"Invoice({self.id}, amount={self.amount}, status={self.status}, payment_reference={self.payment_reference})"




    