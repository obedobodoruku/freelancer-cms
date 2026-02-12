from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm, LoginForm, CreateClientForm, EditClientForm, CreateProjectForm, EditProjectForm, CreateProjectTask, EditTaskForm
from app.models import User, Clients, Project, Task
from flask_login import login_user, login_required, logout_user, current_user

@app.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("home.html", title="Home Page")

@app.route("/client", methods=["GET", "POST"])
def index():
    clients = Clients.query.filter_by(user_id=current_user.id).all()
    return render_template("clients.html", clients=clients, title="Clients Page")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully")
        return redirect(url_for("index"))
    return render_template("register.html", form=form, title="Register Page")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in")
            return redirect(url_for("index"))
        flash("Login unsuccessful. Please check email and password")
    return render_template("login.html", form=form, title="Login Page")

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/create_client", methods=["GET", "POST"])
def create_client():
    form = CreateClientForm()
    if form.validate_on_submit():
        client = Clients(name=form.name.data, email=form.email.data, phone=form.phone.data, note=form.note.data, user_id=current_user.id)
        db.session.add(client)
        db.session.commit()
        flash("Your Client has been added")
        return redirect(url_for("index"))
    return render_template("create_client.html", form=form, title="Create a Client")

@app.route("/delete_client/<int:client_id>", methods=["GET"])
@login_required
def delete_client(client_id):
    if current_user.is_authenticated:
        client = Clients.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        flash(f"Client {client.name} has been deleted")
        return redirect(url_for("index"))
    if client.owner != current_user:
        flash("You do not have permission to delete this client")
        return redirect(url_for("index"))
    return render_template("clients.html", client_id=client_id)

@app.route("/edit_client/<int:client_id>", methods=["GET", "POST"])
@login_required
def edit_client(client_id):
    client = Clients.query.get_or_404(client_id)
    form = EditClientForm()
    if request.method == "POST":
        if form.validate_on_submit():
            client.name = form.name.data
            client.email = form.email.data
            client.phone = form.phone.data
            client.note = form.note.data
            db.session.commit()
            flash(f"Client {client.name} has been updated")
            return redirect(url_for("index"))
    elif request.method == "GET":
        form.name.data = client.name
        form.email.data = client.email
        form.phone.data = client.phone
        form.note.data = client.note

    return render_template("edit_client.html", form=form, client_id=client_id, title=f"Edit Client {client.id}")

@app.route("/project/<int:project_id>", methods=["GET", "POST"])
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    ##client = Clients.query.filter_by()
    return render_template("project.html", project=project, title=f"Project {project.title}")

@app.route("/create_project/<int:client_id>", methods=["GET", "POST"])
@login_required
def create_project(client_id):
    client = Clients.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()
    form = CreateProjectForm()

    if form.validate_on_submit():
        project = Project(title=form.title.data, description=form.description.data, start_date=form.start_date.data, deadline=form.deadline.data, status=form.status.data, client=client)
        db.session.add(project)
        db.session.commit()
        flash(f"Client {client.name} project has been created")
        return redirect(url_for("index"))
    
    return render_template("create_project.html",form=form, client_id=client_id, title=f"Client {client.name} project")

@app.route("/edit_project/<int:project_id>", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = EditProjectForm()

    if request.method == "POST":
        if form.validate_on_submit():
            project.title = form.title.data
            project.description = form.description.data
            project.start_date = form.start_date.data
            project.deadline = form.deadline.data
            project.status = form.status.data
            db.session.commit()
            flash(f"Project {project.id} has been updated")
            return redirect(url_for("project", project_id=project.id))
    elif request.method == "GET":
        form.title.data = project.title
        form.description.data = project.description
        form.start_date.data = project.start_date
        form.deadline.data = project.deadline
        form.status.data = project.status

    return render_template("edit_project.html", project_id=project_id, form=form, title=f"Edit Project {project.id}")

@app.route("/delete_project/<int:project_id>", methods=["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash(f"Project has been deleted")
    return redirect(url_for("index"))

@app.route("/create_task/<int:project_id>", methods=["GET", "POST"])
@login_required
def create_task(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    form = CreateProjectTask()
    if form.validate_on_submit():
        task = Task(title=form.title.data, status=form.status.data, due_date=form.due_date.data, project_id=project.id)
        db.session.add(task)
        db.session.commit()
        flash("Project task has been added")
        return redirect(url_for("project", project_id=project.id))
    return render_template("create_task.html", project_id=project_id, form=form, title=f"Create Project {project.id} task")

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    project = task.project
    form = EditTaskForm()
    if request.method == "POST":
        if form.validate_on_submit():
            task.title = form.title.data 
            task.status = form.status.data           
            task.due_date = form.due_date.data
            db.session.commit()
            flash(f"Task {task.id} has been updated")
            return redirect(url_for("project", project_id=project.id))
    elif request.method == "GET":
        form.title.data = task.title
        form.status.data = task.status
        form.due_date.data = task.due_date 
    return render_template("edit_task.html", form=form, title=f"Task {task.id} Update")

@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    project = task.project
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("project", project_id=project.id))

