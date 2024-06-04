from __future__ import annotations
from datetime import date,datetime
from flask import Flask, abort, render_template, redirect, url_for, flash,request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, AnonymousUserMixin,login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text,ForeignKey,Boolean
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
#from forms import CreatePostForm,RegisterUserForm,LoginForm,CommentForm
# Add additional imports
from functools import wraps
from flask import abort
from email.message import EmailMessage
import smtplib
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from email.message import EmailMessage
MY_EMAIL = os.environ.get('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')
import csv
import os, sys, shutil, os.path
from flask import send_file



'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'dsfds'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)



# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    # This will act like a List of ListTitle objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    lists = relationship("ListTitle", back_populates="user")

class ListTitle(db.Model):
    __tablename__ = "list"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(250))

    user = relationship("User", back_populates="lists")
    #cascade as below will delete child records if parent record is deleted
    list_items = relationship("ListItem", cascade="all, delete-orphan", back_populates="item_name")

class ListItem(db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    list_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("list.id"))


    item_name = relationship("ListTitle", back_populates="list_items")
    task: Mapped[str] = mapped_column(String(250), nullable=False)
    due_date: Mapped[str] = mapped_column(String(250), nullable=True)
    assignee: Mapped[str] = mapped_column(String(50), nullable=True)
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=True)


with app.app_context():
    db.create_all()


class RegisterUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


def logged_in_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        print(current_user)
        if current_user.is_authenticated:
            return f(*args, **kwargs)
            # if current_user.id != 1:
            # return abort(403)
        else:
            return abort(403)

    return decorated_function

@app.route('/register', methods=["GET","POST"])
def register_user():
    register_form = RegisterUserForm()

    if register_form.validate_on_submit():
        email = register_form.email.data
        # check if user email already exists and raise an erorr
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")

            #change to login
            return redirect(url_for("login"))
        else:
            hash_password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256', salt_length=8)
            new_user = User(name=register_form.name.data,email=register_form.email.data,password=hash_password)
            db.session.add(new_user)
            db.session.commit()

            # Log in and authenticate user after adding details to database.
            login_user(new_user)

            # Can redirect() and get name from the current_user
            return redirect(url_for("home"))

    return render_template("register.html", form=register_form,current_user=current_user)


@app.route('/')
def home():
    if current_user.is_authenticated:
        result = db.session.execute(db.select(ListTitle).where (ListTitle.user_id==current_user.id))
        lists = result.scalars().all()
        return render_template("index.html",all_lists=lists)
    else:
        lists = []
        return render_template("index.html", all_lists=lists)


@app.route("/list_details/<list_id>")
#@logged_in_only
def show_list_details(list_id):
    result = db.session.execute(db.select(ListItem).where
                                (ListItem.list_id == list_id))


    # result = db.session.execute(db.select(ListTitle, ListItem).where
    #                             (ListTitle.id == list_id)
    #                             & (ListItem.list_id == list_id)
    #                             & (ListTitle.user_id == current_user.id))

    requested_list = result.scalars().all()
    print(len(requested_list))
    result = db.session.execute(db.select(ListTitle).where (ListTitle.user_id==current_user.id))
    lists = result.scalars().all()
    list_name = db.get_or_404(ListTitle, list_id)
    l_name = list_name.name
    l_id = list_name.id

    return render_template("list_details.html", requested_list=requested_list,list_name=l_name,list_id=l_id,lists=lists)

@app.route("/<list_item_id>/<list_id>", methods=["GET", "POST"])
@logged_in_only
def update_list_item(list_item_id,list_id):
    item = db.get_or_404(ListItem, list_item_id)
    item.task = request.form["task"]
    item.due_date = request.form["due"]
    print(item.due_date)
    item.assignee = request.form["assign"]
    item.notes = request.form["notes"]
    if request.form.get("complete",True):
        if request.form.get("complete"):
            item.completed = 1
        else:
            item.completed = 0
    item.list_id = list_id
    #print(item.task,item.due_date,item.id,item.list_id)
    db.session.commit()
    return redirect(url_for("show_list_details", list_id=list_id))

@app.route("/update_all_list_items/<int:list_id>", methods=["GET", "POST"])
@logged_in_only
def update_all_list_items(list_id):
    #result = db.session.execute(db.select(ListItem).where(ListItem.list_id == list_id))
    #list_items = result.scalars().all()
    id_string = ""


    if request.method == "POST":
        ids = request.form.get("ids")
        print(ids)
        for char in ids:
            if char.isdigit():
                id_string += char
            if char == ",":
                id_string += char
        print(id_string)
        id_list = id_string.split(",")
        print(id_list)

        for i in range(0, len(id_list)):
            result = db.session.execute(db.select(ListItem).where
                                        (ListItem.id == id_list[i]))
            item = result.scalar()

            n = str(i)

            #item = db.get_or_404(ListItem, id_list[i])
            print(item)
            item.task = request.form[f"task_{n}"]
            print(item.task)
            item.due_date = request.form[f"due_{n}"]
            print(item.due_date)
            item.assignee = request.form[f"assign_{n}"]
            print(item.assignee)
            item.notes = request.form[f"notes_{n}"]
            print(item.notes)
            if request.form.get(f"complete_{n}", True):
                if request.form.get(f"complete_{n}"):
                    item.completed = 1
                else:
                    item.completed = 0
            print(item.completed)

            item.list_id = list_id
            db.session.commit()

        return redirect(url_for("show_list_details", list_id=list_id))

@app.route("/add_list_item/<list_id>", methods=["GET", "POST"])
@logged_in_only
def add_list_item(list_id):
    if request.method == "POST":
        task_name = request.form["new_task"]
        due_date = request.form["new_due_date"]
        assignee = request.form["new_assignee"]
        print(assignee)
        notes = request.form["new_notes"]
        if not notes:
            notes = ""
        if request.form.get("new_complete"):
            completed = 1
        else:
            completed = 0
        new_list_item = ListItem(list_id=list_id,task=task_name,due_date=due_date,assignee=assignee,notes=notes,completed=completed)
        db.session.add(new_list_item)
        db.session.commit()
        return redirect(url_for("show_list_details", list_id=list_id))

@app.route("/<int:list_item_id>/<int:list_id>")
@logged_in_only
def delete_list_item(list_item_id,list_id):
    item_to_delete = db.get_or_404(ListItem, list_item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for("show_list_details", list_id=list_id))

@app.route("/move/<int:list_item_id>", methods=["GET", "POST"])
@logged_in_only
def move_list_item(list_item_id):

    if request.method == "POST":
        list_name = request.form.get("move_to")
        print(list_name)
        move_to_list = db.session.execute(db.select(ListTitle).where(ListTitle.name == list_name))
        move_to_list = move_to_list.scalar()
        selected_list_item = db.get_or_404(ListItem, list_item_id)
        selected_list_item.list_id = move_to_list.id
        db.session.commit()
        return redirect(url_for("home"))
    else:
        #get list item details and current list
        result = db.session.execute(db.select(ListItem).where
                                    (ListItem.id == list_item_id))
        list_item = result.scalar()
        print(list_item.id)
        result = db.session.execute(db.select(ListTitle).where(ListTitle.id == list_item.list_id))
        current_list = result.scalar()
        print(current_list.name)

        #get all of the user's lists
        result = db.session.execute(db.select(ListTitle).where(ListTitle.user_id == current_user.id))
        lists = result.scalars().all()

        return render_template("move_list_item.html", list_item=list_item, current_list=current_list,lists=lists)



@app.route("/add_list", methods=["GET", "POST"])
def add_new_list():
    if request.method == "POST":

        list_name = request.form["list_name"]
        if not list_name or list_name == "":
            flash("Please enter a name for the new list")
            return redirect(url_for("add_new_list"))
        else:
            result = db.session.execute(db.select(ListTitle).where(ListTitle.user_id == current_user.id))
            lists = result.scalars().all()
            for list_object in lists:
                if list_object.name.strip().upper() == list_name.strip().upper():
                    flash("That list already exists.  Please enter a unique list name")
                    return redirect(url_for("add_new_list"))

            new_list = ListTitle(name=list_name,user_id=current_user.id)
            db.session.add(new_list)
            db.session.commit()
            #added_list = db.session.execute(db.select(ListTitle).where(ListTitle.name == list_name))
            #added_list = added_list.scalar()

            added_list = db.session.query(ListTitle).filter(
                ListTitle.user_id == current_user.id, ).filter(
                ListTitle.name == list_name, )
            return redirect(url_for("show_list_details", list_id=added_list[0].id))

    else:
        if current_user.is_authenticated:
            return render_template("add_list.html")
        else:
            flash("Please log in/register to add a new list")
            return redirect(url_for("login"))

@app.route("/update_list_name/<list_id>", methods=["GET", "POST"])
@logged_in_only
def update_list_name(list_id):
    selected_list = db.get_or_404(ListTitle, list_id)
    selected_list.name = request.form["list_name"]
    selected_list.id = list_id
    db.session.commit()
    return redirect(url_for("show_list_details", list_id=list_id))

@app.route("/delete_list/<int:list_id>")
@logged_in_only
def delete_list(list_id):
    #db.session.delete(db.session.execute(db.select(ListItem).where(ListItem.list_id == list_id)))
    #db.session.commit()
    list_to_delete = db.get_or_404(ListTitle, list_id)
    db.session.delete(list_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/email_list/<int:list_id>", methods=["GET", "POST"])
@logged_in_only
def email_list(list_id):
    if request.form["recipient"]:
        list_name = db.get_or_404(ListTitle, list_id)
        l_name = list_name.name
        result = db.session.execute(db.select(ListItem).where
                                (ListItem.list_id == list_id))

        list_items = result.scalars().all()
        email = EmailMessage()
        email["from"] = MY_EMAIL
        email["to"] = request.form["recipient"]
        email["subject"] = f"{l_name}"
        list_dict = {}
        email_string = ""
        for i in range(0, len(list_items)):
            print(list_items)
            list_dict[i] = {"Task": list_items[i].task,
                            "Due Date": list_items[i].due_date,
                            "Assignee": list_items[i].assignee,
                            "Notes": list_items[i].notes,
                            "Completed": list_items[i].completed,
                            }
            if list_items[i].completed == 1:
                complete = "Yes"
            else:
                complete = "Pending"

            email_string += (f"{i + 1}. {list_items[i].task}\n"
                            f"Due Date: {list_items[i].due_date}\n"
                            f"Assignee: {list_items[i].assignee}\n"
                            f"Notes: {list_items[i].notes}\n"
                            f"Completed: {complete}\n\n")

        email.set_content(f"{email_string}")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.send_message(email)

        flash("Email Sent")
        return redirect(url_for("show_list_details", list_id=list_id))

    else:
        flash("Please enter a valid email address")
        return redirect(url_for("show_list_details", list_id=list_id))

@app.route('/outstanding_tasks')
@logged_in_only
def outstanding_task_report():
    print(current_user.id)
    result = db.session.query(ListTitle,ListItem).filter(
        ListTitle.user_id == current_user.id,).filter(
        ListTitle.id == ListItem.list_id,).filter(
        ListItem.completed == 0,).all()
    outstanding = result
    print(outstanding)
    for i in range(0,len(outstanding)):
        #this query result is a tuple
        if outstanding[i][1].due_date:
            formatted_date = datetime.strptime(outstanding[i][1].due_date,'%Y-%m-%d')
            formatted_date = formatted_date.strftime('%b %-d, %Y')
            outstanding[i][1].due_date = formatted_date
    return render_template("outstanding_tasks.html",outstanding=outstanding)


@app.route("/clone/<list_name>/<list_id>", methods=["GET", "POST"])
@logged_in_only
def clone_list(list_name,list_id):
    clone_list_name = f"(Clone) {list_name}"
    new_list = ListTitle(name=clone_list_name,user_id = current_user.id)
    db.session.add(new_list)
    db.session.commit()
    result = db.session.execute(db.select(ListTitle).where
                                (ListTitle.name == clone_list_name))
    cloned_list = result.scalar()
    new_list_id = cloned_list.id

    result = db.session.execute(db.select(ListItem).where
                                (ListItem.list_id == list_id))
    list_items_to_clone = result.scalars().all()

    for i in range(0,len(list_items_to_clone)):
        task_name = list_items_to_clone[i].task
        due_date = list_items_to_clone[i].due_date
        assignee = list_items_to_clone[i].assignee
        notes = list_items_to_clone[i].notes
        completed = 0
        new_list_item = ListItem(list_id=new_list_id, task=task_name, due_date=due_date, assignee=assignee, notes=notes,
                                 completed=completed)
        db.session.add(new_list_item)
        db.session.commit()

    return redirect(url_for("show_list_details", list_id=new_list_id))

@app.route('/login', methods=["GET","POST"])
def login():

    login_form = LoginForm()
    if login_form.validate_on_submit():

        # Find user by email entered.
        result = db.session.execute(db.select(User).where(User.email == login_form.email.data))
        user = result.scalar()

        if not user:
            flash("Invalid email")

        # Check stored password hash against entered password hashed.
        else:
            if check_password_hash(user.password, login_form.password.data):
                # Log in and authenticate user
                login_user(user)
                print(current_user.is_authenticated)
                return redirect(url_for('home'))
            else:
                flash("Invalid password")

    return render_template("login.html", form=login_form, current_user=current_user)

@app.route("/save_csv/<list_id>/<list_name>")
@logged_in_only
def save_to_csv(list_id,list_name):
    list_dict={}
    result = db.session.execute(db.select(ListItem).where
                                    (ListItem.list_id == list_id))

    requested_list = result.scalars().all()
    print(len(requested_list))

    for n in range(0, len(requested_list)):
        if requested_list[n].completed == 1:
            completed = "Yes"
        else:
            completed = "Pending"
        list_dict[n] = {"Task": requested_list[n].task,
                       "Due Date": requested_list[n].due_date,
                       "Assignee": requested_list[n].assignee,
                       "Notes": requested_list[n].notes,
                       "Completed": completed,
                       }

    with open(f"{list_name}_details.csv", "w", newline="") as f:

        for y in range(0, len(requested_list)):
            w = csv.DictWriter(f, list_dict[y].keys())
            if y == 0:
                w.writeheader()
            w.writerow(list_dict[y])

        filename = f"{list_name}_details.csv"


    return send_file(
        f'{filename}',
        mimetype='text/csv',
        download_name=f'{filename}',
        as_attachment=True)

        #flash(f"{filename} downloaded successfully")

    #return redirect(url_for("show_list_details", list_id=list_id))




@app.route('/logout')
@logged_in_only
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=False, port=5002)

