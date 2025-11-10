from __future__ import annotations
from datetime import date, datetime
import jwt
import datetime

import requests
from dotenv import load_dotenv

# import psycopg2
import psycopg
from flask import Flask, abort, render_template, redirect, url_for, flash, request, jsonify, Response
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, AnonymousUserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import abort
from email.message import EmailMessage
import smtplib
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from email.message import EmailMessage

MY_EMAIL = os.environ.get('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')
# SEND_GRID = os.environ.get('SENDGRID_API_KEY')
import csv
import os, sys, shutil, os.path
from flask import send_file
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# class DBConnect:
#     def __init__(self):
#         self.connection = psycopg2.connect(database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),
#                                           password=os.environ.get('DB_PASSWORD'),
#                                           host=os.environ.get('DB_HOST'), port=os.environ.get('DB_PORT'))
#
#         self.cursor = self.connection.cursor()

class DBConnect:
    def __init__(self):
        self.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

        self.host = os.getenv("DB_HOST")

        if not self.host:
            raise ValueError("DB_HOST is empty. Check your environment variables!")
        self.cursor = self.connection.cursor()

    def commit(self):
        """Commit current transaction"""
        self.connection.commit()

    def close(self):
        """Close cursor and connection"""
        self.cursor.close()
        self.connection.close()


# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    # Open a new cursor/connection to your DB
    con = DBConnect()
    # Fetch the user row by id
    con.cursor.execute("SELECT id, email, password, name FROM users WHERE id = %s", (user_id,))
    row = con.cursor.fetchone()
    con.cursor.close()

    if row:
        # Reconstruct the same User object you passed to login_user()
        user = User(id=row[0], email=row[1], password=row[2], name=row[3])
        return user
    else:
        return None  # Flask-Login will treat this as not logged in


login_manager = LoginManager()


class User:
    def __init__(self, id, email, password, name, active=True):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.active = active

    # Flask-Login required methods:
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        # Must return a string
        return str(self.id)


# def create_db():
#     try:
#         conn = psycopg2.connect(
#             host=os.environ.get('DB_HOST'),
#             database=os.environ.get('DB_NAME_DEFAULT'),  # Connect to the default 'postgres' database first
#             user=os.environ.get('DB_USER'),
#             password=os.environ.get('DB_PASSWORD'),
#             port=os.environ.get('DB_PORT')
#         )
#         conn.autocommit = True  # Set autocommit to True
#         cur = conn.cursor()
#
#         cur.execute(f"CREATE DATABASE {os.environ.get('DB_NAME')};")
#         print("Database created successfully!")
#
#         cur.close()
#         conn.close()
#     except psycopg.Error as e:
#         print(f"Duplicate DB: {e}")

import os
import psycopg


def create_db():
    try:
        # Connect to the default database (e.g. 'postgres')
        with psycopg.connect(
                host=os.environ.get('DB_HOST'),
                dbname=os.environ.get('DB_NAME_DEFAULT'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'),
                port=os.environ.get('DB_PORT')
        ) as conn:
            # Enable autocommit mode
            conn.autocommit = True

            with conn.cursor() as cur:
                db_name = os.environ.get('DB_NAME')
                cur.execute(f"CREATE DATABASE {db_name};")
                print("Database created successfully!")

    except psycopg.Error as e:
        print(f"Duplicate DB: {e}")


create_db()

# def create_table():
#     conn = psycopg.connect(database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),
#                            password=os.environ.get('DB_PASSWORD'),
#                            host=os.environ.get('DB_HOST'), port=os.environ.get('DB_PORT'))
#     # print('connected')
#     cur = conn.cursor()
#     conn.autocommit = True
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id SERIAL PRIMARY KEY,
#             email VARCHAR(255) NOT NULL,
#             password VARCHAR(100) NOT NULL,
#             name VARCHAR(50) NOT NULL
#         )
#         """)
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS list (
#         id SERIAL PRIMARY KEY,
#         user_id INTEGER,
#         name VARCHAR(100) NOT NULL,
#         FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#     );
#     """)
#
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS items (
#             id SERIAL PRIMARY KEY,
#             list_id INTEGER,
#             task VARCHAR(100) NOT NULL,
#             due_date VARCHAR(20),
#             assignee VARCHAR(50),
#             notes VARCHAR(250),
#             completed BOOLEAN,
#             FOREIGN KEY (list_id) REFERENCES list(id) ON DELETE CASCADE
#         );
#         """)
#
#     cur.close()
#     conn.close()

import os
import psycopg


def create_table():
    # Connect to your target database
    with psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
    ) as conn:
        conn.autocommit = True  # Apply changes immediately (no explicit commit needed)

        with conn.cursor() as cur:
            # Users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    name VARCHAR(50) NOT NULL
                );
            """)

            # List table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS list (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    name VARCHAR(100) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            # Items table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    list_id INTEGER,
                    task VARCHAR(100) NOT NULL,
                    due_date VARCHAR(20),
                    assignee VARCHAR(50),
                    notes VARCHAR(250),
                    completed BOOLEAN,
                    FOREIGN KEY (list_id) REFERENCES list(id) ON DELETE CASCADE
                );
            """)

        print("✅ Tables created successfully!")


create_table()


def to_dict(self):
    # Method 1.
    dictionary = {}
    # Loop through each column in the data record
    for column in self.__table__.columns:
        # Create a new dictionary entry;
        # where the key is the name of the column
        # and the value is the value of the column
        dictionary[column.name] = getattr(self, column.name)
        print(dictionary)
        return dictionary


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


@app.route('/register', methods=["GET", "POST"])
def register_user():
    con = DBConnect()
    register_form = RegisterUserForm()

    if register_form.validate_on_submit():
        email = register_form.email.data
        name = register_form.name.data
        # check if user email already exists and raise an erorr
        con.cursor.execute(f"SELECT id from users where users.email = '{email}';")
        result = con.cursor.fetchall()

        if result:
            flash("You've already signed up with that email, log in instead!")

            # change to login
            return redirect(url_for("login"))
        else:
            hash_password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256', salt_length=8)
            con.cursor.execute(f'SELECT * FROM users LIMIT 0')
            column_names = [desc[0] for desc in con.cursor.description]
            new_user = f"INSERT INTO users({column_names[1]}," \
                       f"{column_names[2]}, {column_names[3]})" \
                       f" VALUES('{email}','{hash_password}', '{name}');"
            con.cursor.execute(new_user)
            con.connection.commit()
            con.cursor.execute(f"SELECT * from users where users.email = '{email}';")
            result = con.cursor.fetchall()
            con.cursor.close()

            # Log in and authenticate user after adding details to database.
            user = User(id=result[0][0], email=result[0][1], password=result[0][2], name=result[0][3])
            login_user(user)

            # Can redirect() and get name from the current_user
            return redirect(url_for("home"))

    return render_template("register.html", form=register_form, current_user=current_user)


def get_user_lists(endpoint=None, params=None, headers=None, data=None, ):
    app_instance = create_app()

    with app_instance.app_context():
        base_url = current_app.config["BASE_URL"]
        endpoint = '/api/get_user_lists'
        params = {'user_id': current_user.id}
        response = requests.get(url=base_url + endpoint, params=params)
        response.raise_for_status()
        assert response.ok
        lists = response.json()['lists']
        return lists


@app.route('/api/get_user_lists', methods=['GET'])
def get_user_lists_api():
    if request.args.get("user_id"):
        user_id = request.args.get("user_id")

        try:
            con = DBConnect()
            con.cursor.execute(
                "SELECT * from list Where user_id = %s;", (user_id,)
            )
            lists = con.cursor.fetchall()
            con.cursor.close()

            if len(lists) > 0:
                return jsonify({
                    "message": "Lists returned successfully",
                    "lists": lists
                }), 200
            else:
                return jsonify({
                    "message": "User doesn't have any lists",
                    "lists": lists
                }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    if current_user.is_authenticated:
        # con = DBConnect()
        # con.cursor.execute(f"SELECT * from list where list.user_id = '{current_user.id}';")
        # lists = con.cursor.fetchall()
        # print(lists)
        # con.cursor.close()
        lists = get_user_lists()

        return render_template("index.html", all_lists=lists)
    else:
        lists = []
        return render_template("index.html", all_lists=lists)


@app.route("/add_list", methods=["GET", "POST"])
def add_new_list():
    if request.method == "POST":
        con = DBConnect()

        list_name = request.form["list_name"]
        if not list_name or list_name == "":
            flash("Please enter a name for the new list")
            return redirect(url_for("add_new_list"))
        else:
            con.cursor.execute(f"SELECT name from list where list.user_id = '{current_user.id}';")
            lists = con.cursor.fetchall()
            print(lists)
            for list_object in lists:
                if list_object[0].strip().upper() == list_name.strip().upper():
                    flash("That list already exists.  Please enter a unique list name")
                    return redirect(url_for("add_new_list"))

            con.cursor.execute(f'SELECT * FROM list LIMIT 0')
            column_names = [desc[0] for desc in con.cursor.description]

            new_list = f"INSERT INTO list({column_names[1]}," \
                       f"{column_names[2]})" \
                       f" VALUES('{current_user.id}','{list_name}');"
            con.cursor.execute(new_list)
            con.connection.commit()

            con.cursor.execute(
                f'SELECT * FROM list '
                f'WHERE list.user_id = %s AND list.name = %s;',
                (current_user.id, list_name)
            )

            added_list = con.cursor.fetchall()
            con.cursor.close()
            print(added_list[0])
            return redirect(url_for("show_list_details", list_id=added_list[0][0]))

    else:
        if current_user.is_authenticated:

            return render_template("add_list.html")
        else:
            flash("Please log in/register to add a new list")
            return redirect(url_for("login"))


@app.route("/list_details/<list_id>")
# @logged_in_only
def show_list_details(list_id):
    con = DBConnect()
    con.cursor.execute(
        f'SELECT * FROM items '
        f'WHERE items.list_id = {list_id};'
    )
    items = con.cursor.fetchall()
    print(items)

    con.cursor.execute(
        f'SELECT * FROM list '
        f'WHERE list.id = {list_id};'
    )

    list_object = con.cursor.fetchall()
    print(list_object)
    l_name = list_object[0][2]
    l_id = list_object[0][0]
    print(current_user.id)
    con.cursor.execute(
        f'SELECT * FROM list '
        f'WHERE list.user_id = {current_user.id};'
    )
    lists = con.cursor.fetchall()
    con.cursor.close()

    return render_template("list_details.html", requested_list=items, list_name=l_name, list_id=l_id, lists=lists)


@app.route("/<list_item_id>/<list_id>", methods=["GET", "POST"])
@logged_in_only
def update_list_item(list_item_id, list_id):
    con = DBConnect()
    con.cursor.execute(
        f'SELECT * FROM items '
        f'WHERE items.id = {list_item_id}'
        f' AND items.list_id = {list_id};'
    )
    item = con.cursor.fetchall()
    item.task = request.form["task"]
    item.due_date = request.form["due"]
    print(item.due_date)
    item.assignee = request.form["assign"]
    item.notes = request.form["notes"]
    if request.form.get("complete", True):
        if request.form.get("complete"):
            item.completed = 1
        else:
            item.completed = 0
    item.list_id = list_id
    con.cursor.close()
    # print(item.task,item.due_date,item.id,item.list_id)
    return redirect(url_for("show_list_details", list_id=list_id))


@app.route("/update_all_list_items/<int:list_id>", methods=["GET", "POST"])
# @logged_in_only
def update_all_list_items(list_id):
    # result = db.session.execute(db.select(ListItem).where(ListItem.list_id == list_id))
    # list_items = result.scalars().all()
    id_string = ""
    indexes = []

    if request.method == "POST":
        if request.form.get("ids"):
            ids = request.form.get("ids")
            if ids[1].isdigit() > 0:

                print(ids)
                print("test")
                for char in ids:
                    if char.isdigit():
                        id_string += char
                    if char == ",":
                        id_string += char
                print(id_string)
                id_list = id_string.split(",")
                print(id_list)

                for i in range(0, len(id_list)):
                    con = DBConnect()
                    con.cursor.execute(
                        f'SELECT * FROM items '
                        f'WHERE items.id = {id_list[i]};')
                    item = con.cursor.fetchall()
                    print(item)

                    n = str(i)
                    indexes.append(n)

                    task = request.form[f"task_{n}"]

                    due = request.form[f"due_{n}"]

                    assignee = request.form[f"assign_{n}"]

                    notes = request.form[f"notes_{n}"]
                    completed = 0

                    if request.form.get(f"complete_{n}", True):
                        if request.form.get(f"complete_{n}"):
                            completed = True
                        else:
                            completed = False

                    con.cursor.execute("""
                    UPDATE items
                    SET task = %s,
                    due_date = %s,
                    assignee = %s,
                    notes = %s,
                    completed = %s
                    WHERE id = %s;
                    """,
                                       (task, due, assignee, notes, completed, id_list[i]))
                    con.connection.commit()
                    con.cursor.close()

            # else:
            #   flash("Please add at least 1 item to the list first")

            task_fields = [key for key in request.form.keys() if key.startswith('task_')]
            print(task_fields)
            if len(task_fields) > 0:

                for i in range(0, len(task_fields)):
                    index = task_fields[i].split('_')[1]
                    if index not in indexes:
                        task = request.form[f"task_{index}"]
                        due = request.form[f"due_{index}"]
                        assignee = request.form[f"assign_{index}"]
                        notes = request.form[f"notes_{index}"]
                        completed = 0
                        if request.form.get(f"complete_{index}", True):
                            if request.form.get(f"complete_{index}"):
                                completed = True
                            else:
                                completed = False
                        con = DBConnect()
                        con.cursor.execute(f'SELECT * FROM items LIMIT 0')
                        column_names = [desc[0] for desc in con.cursor.description]
                        new_item = f"INSERT INTO items({column_names[1]}," \
                                   f"{column_names[2]}, {column_names[3]}, {column_names[4]}, {column_names[5]}, {column_names[6]})" \
                                   f" VALUES('{list_id}','{task}', '{due}', '{assignee}', '{notes}', '{completed}');"
                        con.cursor.execute(new_item)
                        con.connection.commit()
                        con.cursor.close()

            else:
                flash("Please add at least 1 item to the list first")

        return redirect(url_for("show_list_details", list_id=list_id))


@app.route("/add_list_item/<list_id>", methods=["GET", "POST"])
@logged_in_only
def add_list_item(list_id):
    if request.method == "POST":
        task_name = request.form["new_task"]
        due_date = request.form["new_due_date"]
        print(due_date)
        assignee = request.form["new_assignee"]

        notes = request.form["new_notes"]
        if not notes:
            notes = ""
        if request.form.get("new_complete"):
            completed = 1
        else:
            completed = 0
        con = DBConnect()
        con.cursor.execute(f'SELECT * FROM items LIMIT 0')
        column_names = [desc[0] for desc in con.cursor.description]

        new_item = f"INSERT INTO items({column_names[1]}," \
                   f"{column_names[2]}, {column_names[3]}, {column_names[4]}, {column_names[5]}, {column_names[6]})" \
                   f" VALUES('{list_id}','{task_name}', '{due_date}', '{assignee}', '{notes}', '{completed}');"
        con.cursor.execute(new_item)
        con.connection.commit()
        con.cursor.close()
        return redirect(url_for("show_list_details", list_id=list_id))


@app.route("/<int:list_item_id>/<int:list_id>")
@logged_in_only
def delete_list_item(list_item_id, list_id):
    con = DBConnect()
    con.cursor.execute("""
                        DELETE FROM items
                        WHERE id = %s
                        AND list_id = %s;
                        """,
                       (list_item_id, list_id)
                       )
    con.connection.commit()
    con.cursor.close()

    return redirect(url_for("show_list_details", list_id=list_id))


# @app.route("/move/<int:list_item_id>", methods=["GET", "POST"])
# @logged_in_only
# def move_list_item(list_item_id):
#     if request.method == "POST":
#         list_name = request.form.get("move_to")
#         print(list_name)
#         move_to_list = db.session.execute(db.select(ListTitle).where(ListTitle.name == list_name))
#         move_to_list = move_to_list.scalar()
#         selected_list_item = db.get_or_404(ListItem, list_item_id)
#         selected_list_item.list_id = move_to_list.id
#         db.session.commit()
#         return redirect(url_for("home"))
#     else:
#         # get list item details and current list
#         result = db.session.execute(db.select(ListItem).where
#                                     (ListItem.id == list_item_id))
#         list_item = result.scalar()
#         print(list_item.id)
#         result = db.session.execute(db.select(ListTitle).where(ListTitle.id == list_item.list_id))
#         current_list = result.scalar()
#         print(current_list.name)
#
#         # get all of the user's lists
#         result = db.session.execute(db.select(ListTitle).where(ListTitle.user_id == current_user.id))
#         lists = result.scalars().all()
#
#         return render_template("move_list_item.html", list_item=list_item, current_list=current_list, lists=lists)


@app.route("/update_list_name/<list_id>", methods=["GET", "POST"])
@logged_in_only
def update_list_name(list_id):
    name = request.form["list_name"]
    con = DBConnect()
    con.cursor.execute("""
                        UPDATE list
                        SET name = %s
                        WHERE id = %s;
                        """,
                       (name, list_id)
                       )
    con.connection.commit()
    con.cursor.close()
    return redirect(url_for("show_list_details", list_id=list_id))


@app.route("/delete_list/<int:list_id>")
@logged_in_only
def delete_list(list_id):
    con = DBConnect()
    con.cursor.execute("""
                            DELETE FROM list
                            WHERE id = %s;
                            """,
                       (list_id,)
                       )
    con.connection.commit()
    con.cursor.close()

    return redirect(url_for("home"))


@app.route("/email_list/<int:list_id>", methods=["GET", "POST"])
@logged_in_only
def email_list(list_id):
    if request.form["recipient"]:
        con = DBConnect()
        con.cursor.execute(
            f'SELECT * FROM list '
            f'WHERE list.id = %s;',
            (list_id,)
        )
        list_name = con.cursor.fetchone()
        l_name = list_name[2]
        con.cursor.execute(
            f'SELECT * FROM items '
            f'WHERE items.list_id = %s;',
            (list_id,)
        )
        list_items = con.cursor.fetchall()
        print(list_items)
        con.cursor.close()
        email = EmailMessage()
        email["from"] = MY_EMAIL
        email["to"] = request.form["recipient"]
        email["subject"] = f"{l_name}"
        list_dict = {}
        email_string = ""
        for i in range(0, len(list_items)):

            list_dict[i] = {"Task": list_items[i][2],
                            "Due Date": list_items[i][3],
                            "Assignee": list_items[i][4],
                            "Notes": list_items[i][5],
                            "Completed": list_items[i][6],
                            }
            if list_items[i][6] == 1:
                complete = "Yes"
            else:
                complete = "Pending"

            email_string += (f"{i + 1}. {list_items[i][3]}\n"
                             f"Due Date: {list_items[i][4]}\n"
                             f"Assignee: {list_items[i][5]}\n"
                             f"Notes: {list_items[i][6]}\n"
                             f"Completed: {complete}\n\n")

        print(email_string)

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


# @app.route("/email_list/<int:list_id>", methods=["GET", "POST"])
# @logged_in_only
# def email_list_send_grid(list_id):
#     if request.form["recipient"]:
#         con = DBConnect()
#         con.cursor.execute(
#             f'SELECT * FROM list '
#             f'WHERE list.id = %s;',
#             (list_id,)
#         )
#         list_name = con.cursor.fetchone()
#         l_name = list_name[2]
#         con.cursor.execute(
#             f'SELECT * FROM items '
#             f'WHERE items.list_id = %s;',
#             (list_id,)
#         )
#         list_items = con.cursor.fetchall()
#         print(list_items)
#         con.cursor.close()
#         list_dict = {}
#         email_string = ""
#         for i in range(0, len(list_items)):
#
#             list_dict[i] = {"Task": list_items[i][2],
#                             "Due Date": list_items[i][3],
#                             "Assignee": list_items[i][4],
#                             "Notes": list_items[i][5],
#                             "Completed": list_items[i][6],
#                             }
#             if list_items[i][6] == 1:
#                 complete = "Yes"
#             else:
#                 complete = "Pending"
#
#             email_string += (f"{i + 1}. {list_items[i][3]}\n"
#                              f"Due Date: {list_items[i][4]}\n"
#                              f"Assignee: {list_items[i][5]}\n"
#                              f"Notes: {list_items[i][6]}\n"
#                              f"Completed: {complete}\n\n")
#
#         print(email_string)
#         message = Mail(
#             from_email=MY_EMAIL,
#             to_emails=request.form["recipient"],
#             subject=f"{l_name}",
#             # html_content=email_string)
#             plain_text_content=email_string)
#
#         sg = SendGridAPIClient(SEND_GRID)
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#         flash("Email Sent")
#         return redirect(url_for("show_list_details", list_id=list_id))
#
#
#     else:
#         flash("Please enter a valid email address")
#         return redirect(url_for("show_list_details", list_id=list_id))
#

@app.route('/outstanding_tasks')
@logged_in_only
def outstanding_task_report():
    print(current_user.id)
    con = DBConnect()
    con.cursor.execute(
        f'''
    SELECT a.*, b.name AS list_name, c.name AS user_name
    FROM items a
    JOIN list b ON a.list_id = b.id
    JOIN users c ON b.user_id = c.id
    WHERE a.completed = false
      AND c.id = %s
    ORDER BY a.due_date ASC;
    ''',
        (current_user.id,)
    )
    outstanding_tasks = con.cursor.fetchall()
    con.cursor.close()
    print(outstanding_tasks)
    if request.args.get("mock_empty"):
        outstanding_tasks = []
    if len(outstanding_tasks) == 0:
        flash("There are no outstanding tasks")

    return render_template("outstanding_tasks.html", outstanding=outstanding_tasks)


@app.route("/clone/<list_name>/<list_id>", methods=["GET", "POST"])
@logged_in_only
def clone_list(list_name, list_id):
    con = DBConnect()
    clone_list_name = f"(Clone) {list_name}"
    con.cursor.execute(f'SELECT * FROM list LIMIT 0')
    column_names = [desc[0] for desc in con.cursor.description]

    new_list = f"INSERT INTO list({column_names[1]}," \
               f"{column_names[2]})" \
               f" VALUES('{current_user.id}','{clone_list_name}');"
    con.cursor.execute(new_list)
    con.connection.commit()
    con.cursor.execute(
        f'SELECT * FROM list '
        f'WHERE list.name = %s;',
        (clone_list_name,)
    )

    cloned_list = con.cursor.fetchall()
    new_list_id = cloned_list[0][0]

    con.cursor.execute(
        f'SELECT * FROM items '
        f'WHERE items.list_id = %s;',
        (list_id,)
    )

    list_items_to_clone = con.cursor.fetchall()
    con.cursor.execute(f'SELECT * FROM items LIMIT 0')
    column_names = [desc[0] for desc in con.cursor.description]

    for i in range(0, len(list_items_to_clone)):
        task_name = list_items_to_clone[i][2]
        due_date = list_items_to_clone[i][3]
        assignee = list_items_to_clone[i][4]
        notes = list_items_to_clone[i][5]
        completed = False

        new_item = f"INSERT INTO items({column_names[1]}," \
                   f"{column_names[2]}, {column_names[3]}, {column_names[4]}, {column_names[5]}, {column_names[6]})" \
                   f" VALUES('{new_list_id}','{task_name}', '{due_date}', '{assignee}', '{notes}', '{completed}');"
        con.cursor.execute(new_item)
        con.connection.commit()

    con.cursor.close()

    return redirect(url_for("show_list_details", list_id=new_list_id))


@app.route('/login', methods=["GET", "POST"])
def login():
    con = DBConnect()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        # Find user by email entered.
        con.cursor.execute(f"SELECT * from users where users.email = '{login_form.email.data}';")
        result = con.cursor.fetchall()
        con.cursor.close()

        if not result:
            flash("Invalid email")

        # Check stored password hash against entered password hashed.
        else:
            if check_password_hash(result[0][2], login_form.password.data):
                # Log in and authenticate user
                user = User(id=result[0][0], email=result[0][1], password=result[0][2], name=result[0][3])
                login_user(user)
                print(current_user.is_authenticated)

                return redirect(url_for('home'))
            else:
                flash("Invalid password")

    return render_template("login.html", form=login_form, current_user=current_user)


@app.route("/save_csv/<list_id>/<list_name>")
@logged_in_only
def save_to_csv(list_id, list_name):
    con = DBConnect()
    list_dict = {}
    con.cursor.execute(
        f'SELECT * FROM items '
        f'WHERE items.list_id = %s;',
        (list_id,)
    )

    requested_list = con.cursor.fetchall()
    con.cursor.close()
    print(len(requested_list))

    for n in range(0, len(requested_list)):
        if requested_list[n][6] == 1:
            completed = "Yes"
        else:
            completed = "Pending"
        list_dict[n] = {"Task": requested_list[n][2],
                        "Due Date": requested_list[n][3],
                        "Assignee": requested_list[n][4],
                        "Notes": requested_list[n][5],
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


@app.route('/download_template')
def download_template():
    csv_content = "Task,Due Date,Assignee,Notes,Complete\n"

    csv_content += "Example Task,2025-11-09,John Doe,Sample note,false\n"
    csv_content += "Another Task,2025-11-10,Mary Smith,tight timeline,true\n"

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=task_template.csv"
        }
    )


@app.route('/logout')
@logged_in_only
def logout():
    logout_user()
    return redirect(url_for('home'))


# REST API calls

@app.route('/api/add_new_list', methods=['POST'])
def add_new_list_api():
    try:
        print("Raw request data:", request.data)
        data = request.get_json(force=True)
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        name = data.get('name')
        user_id = data.get('user_id')

        print(f"Name: {name}, User ID: {user_id}")

        if not name or not user_id:
            return jsonify({"error": "Missing required fields"}), 400

        con = DBConnect()
        con.cursor.execute(
            "INSERT INTO list (user_id, name) VALUES (%s, %s) RETURNING id, user_id, name;",
            (user_id, name)
        )

        new_list = con.cursor.fetchone()
        con.connection.commit()

        con.cursor.close()

        return jsonify({"message": "List added successfully",
                        "list": {
                            "id": new_list[0],
                            "user_id": new_list[1],
                            "name": new_list[2]
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    con = DBConnect()
    # Find user by email entered.
    con.cursor.execute(f"SELECT * from users where users.email = '{email}';")
    result = con.cursor.fetchall()
    con.cursor.close()

    if check_password_hash(result[0][2], password):
        # Log in and authenticate user
        user = User(id=result[0][0], email=result[0][1], password=result[0][2], name=result[0][3])
        login_user(user)
        token = jwt.encode(
            {"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.secret_key,
            algorithm="HS256")
        return jsonify({
            "message": "Logged in successfully",
            "token": token
        })
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/api/login_test', methods=["GET", "POST"])
def login_api_test():
    mock = request.args.get('mock')
    print(f'Mock: {mock}')
    payload = request.get_json()
    email = payload.get("email")
    password = payload.get("password")
    print(email)

    con = DBConnect()
    # Find user by email entered.
    con.cursor.execute(f"SELECT * from users where users.email = '{email}';")
    result = con.cursor.fetchall()
    con.cursor.close()

    if check_password_hash(result[0][2], password):
        # Log in and authenticate user
        user = User(id=result[0][0], email=result[0][1], password=result[0][2], name=result[0][3])
        login_user(user)
        print(current_user.is_authenticated)

        if mock == '1':
            print('Reached here')

            # return redirect(url_for('home'))
        else:

            return jsonify({
                "message": "Logged in successfully",

            })

    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/api/verify_token', methods=['POST'])
def verify_token():
    token = request.json.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        # Optional: check expiration manually if not auto-validated
        exp = decoded.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            return jsonify({"error": "Token expired"}), 401
        return jsonify({"valid": True, "user": decoded}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


@app.route('/tasks_by_assignee')
@logged_in_only
def get_tasks_by_assignee_report():
    con = DBConnect()

    # con.cursor.execute("""
    # SELECT DISTINCT COALESCE(NULLIF(a.assignee, ''), 'Unassigned') AS assignee
    # FROM items a
    # JOIN list b ON a.list_id = b.id
    # JOIN users c ON b.user_id = c.id
    # WHERE a.completed = false
    # AND c.id = %s
    # ORDER BY assignee;
    # """, (current_user.id,))
    #
    # assignees = [r[0] for r in con.cursor.fetchall()]
    #
    # # 2️⃣ Build column definitions
    # columns_sql = ", ".join('"{}" text'.format(a or "Unassigned") for a in assignees)
    #
    # query = f"""
    # SELECT *
    # FROM crosstab(
    # $$
    # SELECT
    #     a.task,
    #     COALESCE(NULLIF(a.assignee, ''), 'Unassigned') AS assignee,
    #     '✔'
    # FROM items a
    # JOIN list b ON a.list_id = b.id
    # JOIN users c ON b.user_id = c.id
    # WHERE a.completed = false
    # AND c.id = {current_user.id}
    # ORDER BY 1,2
    # $$,
    # $$
    # SELECT DISTINCT COALESCE(NULLIF(a.assignee, ''), 'Unassigned') AS assignee
    # FROM items a
    # JOIN list b ON a.list_id = b.id
    # JOIN users c ON b.user_id = c.id
    # WHERE a.completed = false
    # AND c.id = {current_user.id}
    # ORDER BY assignee ASC
    # $$
    # ) AS ct(task text, {columns_sql});
    #
    # """

    # 1️⃣ Get all distinct assignees
    # 1) get assignees (normalized)
    # 1) get assignees (normalized)
    con.cursor.execute("""
        SELECT DISTINCT COALESCE(NULLIF(a.assignee, ''), 'Unassigned') AS assignee
        FROM items a
        JOIN list b ON a.list_id = b.id
        JOIN users c ON b.user_id = c.id
        WHERE a.completed = false
          AND c.id = %s
        ORDER BY assignee;
    """, (current_user.id,))
    assignees = [r[0] for r in con.cursor.fetchall()]

    # 2) build column defns for AS ct(...)
    columns_sql = ", ".join('"{}" text'.format(a or "Unassigned") for a in assignees)

    # 2b) build explicit select list for assignee columns (ct."Name1", ct."Name2", ...)
    select_assignee_cols = ", ".join('ct."{}"'.format(a or "Unassigned") for a in assignees)

    # 3) crosstab query that pivots by item id, but outer SELECT picks only the assignee columns (no ct.item_key)
    query = f"""
    SELECT
        i.task,
        i.list_id,
        i.id AS item_id,
        {select_assignee_cols}
    FROM crosstab(
        $$
        SELECT 
            a.id::text AS item_key,
            COALESCE(NULLIF(a.assignee, ''), 'Unassigned') AS assignee,
            '✔'
        FROM items a
        JOIN list b     ON a.list_id = b.id
        JOIN users c    ON b.user_id = c.id
        WHERE a.completed = false
          AND c.id = {current_user.id}
        ORDER BY 1,2
        $$,
        $$
        SELECT DISTINCT COALESCE(NULLIF(a.assignee, ''), 'Unassigned') AS assignee
        FROM items a
        JOIN list b ON a.list_id = b.id
        JOIN users c ON b.user_id = c.id
        WHERE a.completed = false
          AND c.id = {current_user.id}
        ORDER BY assignee ASC
        $$
    ) AS ct(item_key text, {columns_sql})
    JOIN items i ON i.id::text = ct.item_key
    WHERE i.completed = false
      AND EXISTS (
          SELECT 1 FROM list l WHERE l.id = i.list_id AND l.user_id = {current_user.id}
      );
    """

    con.cursor.execute(query)
    rows = con.cursor.fetchall()

    # 4️⃣ Execute the dynamic query
    try:
        con.cursor.execute(query)
        rows = con.cursor.fetchall()

        # import pandas as pd
        # df = pd.DataFrame(rows, columns=["task", "list_id", "item_id"] + assignees)
        # print(df)
    except:
        rows = []

    print(f'Rows length: {len(rows)}')
    if len(rows) > 0:

        for row in rows:
            print(row)

        totals = []

        # Loop through each assignee column index (skip first column = task name)
        for col_idx in range(1, len(rows[0])):
            count = sum(1 for row in rows if row[col_idx] == '✔')
            totals.append(count)

        totals_row = ('Totals', *totals)
        rows.append(totals_row)


    else:
        flash("There are no tasks by assignee.")

    return render_template("tasks_by_assignee.html", rows=rows, assignees=assignees)


@app.route("/<int:list_item_id>/<int:list_id>", methods=["GET", "POST"])
@logged_in_only
def update_task_to_complete(list_item_id, list_id):
    print(list_item_id)
    con = DBConnect()
    con.cursor.execute("""
        UPDATE items AS a
        SET completed = TRUE
        FROM list AS l
        JOIN users AS u ON l.user_id = u.id
        WHERE a.list_id = l.id
          AND a.id = %s
          AND a.list_id = %s
          AND u.id = %s;
    """, (list_item_id, list_id, f'{current_user.id}',))
    con.connection.commit()
    con.cursor.close()

    return redirect(url_for("get_tasks_by_assignee_report"))


def create_app():
    app_instance = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")  # default to development

    if os.getenv("FLASK_ENV") == "production":
        app.config.from_object("config.Config")
    elif os.getenv("FLASK_ENV") == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False), port=5002)
