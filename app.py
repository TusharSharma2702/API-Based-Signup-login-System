from flask import Flask, render_template, request, jsonify, redirect, url_for, g
from password_hasher import hasher
import sqlite3
import re

# Create an instance of Flask
app = Flask(__name__, template_folder="templates", static_url_path='/static')

# Define the name of the database
DATABASE = 'signupdata.db'

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)                                              # Retrieve the database connection from the 'g' object, if it exists, otherwise set it to None
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)                                # create a connection to the database if not exist
        # Create the "users" table if it doesn't exist
        with db:
            db.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )''')
    return db

# Teardown function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Function to add user data to the database
def add_data_db(username, email, hashed_password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    db.commit()
    cursor.close()

# Function to check user login credentials
def check_login(email,hashed_password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?",(email,))
    data = cursor.fetchone()
    cursor.close()
    if data == None:
        return render_template("error.html",error="e-mail not registered try sign in")
    
    if hashed_password == data[3]:
        return redirect(url_for("home",username=data[1]))
    else :
        return render_template("error.html", error="Passwords is incorrect")
    
# Function to check if the password follows the criteria
def check_password_format(password):
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$", password):
        return True
    
# Function to check if the email matches the email format
def check_email_format(email):
    if not re.match(r"[a-zA-Z0-9\.\_]+[@][a-z]+[\.][a-z]+", email):
        return True


# Function to check if email is already registered
def check_mail(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?",(email,))
    data = cursor.fetchone()
    cursor.close()
    if data != None:
        return True
    
    
# Function to check if username is already in use
def check_username(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
    data = cursor.fetchone()
    cursor.close()
    if data != None:
        return True
    

#define routes for signup page that support both GET and POST request
@app.route("/",methods=["GET", "POST"])
@app.route("/signup",methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form.to_dict()                                   # Extract form data from the request and convert it to a dictionary
        username = data.get("username")                                 # get value of username field
        email = data.get("email")                                       # get value of email field
        password = data.get("password")                                 # get value of password field
        confirm_password = data.get("confirm_password")                 # get value of confirm password field

        if not username or not email or not password:                   # Check if any required fields are missing
            return render_template("error.html", error="Missing required fields"),400
        
        if password != confirm_password:                                # Check if the passwords match
            return render_template("error.html", error="Passwords do not match"),400
        
        if check_email_format(email):                                   # Check if the email format is valid
            return render_template("error.html", error="Not a valid E-mail Id"),400
        
        if check_password_format(password):                             # Check if the password format is valid
            return render_template("error.html", error='''Password musut conatin 
                                   atleast one lowercase, one uppercase, 
                                   one numeric and a special character 
                                   and must be 8 character long'''),400
        
        if check_username(username):                                    # Check if the username is already registered
            return render_template("error.html", error="username already registered try different username"),400
        
        if check_mail(email):                                           # Check if the email is already registered
            return render_template("error.html", error="E-mail already registered try sign in"),400

        hashed_password = hasher(password)                              # Hash the password
        add_data_db(username, email, hashed_password)                   # Add user data to the database
        return redirect(url_for("login"))                               # Redirect the user to the login page after successful signup
    
    return render_template("signup.html")                               # Render the signup.html template for GET requests

#define routes for login page that support both GET and POST request
@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form.to_dict()                                   # Extract form data from the request and convert it to a dictionary
        email = data.get("email")                                       # Get value of email field
        password = data.get("password")                                 # Get value of Password field
        if not email or not password:                                   # Check if any required fields are missing
            return render_template("error.html",error="Missing required fields")
        
        hashed_password = hasher(password)                              # Hash the password
        return check_login(email, hashed_password)                      # Check login credentials

    return render_template("login.html",)                               # Render the signup.html template for GET requests

#define route for home page
@app.route("/home/<username>")
def home(username):
    return render_template("home.html", username=username)              # Render the home.html template 

if __name__=="__main__":
    app.run(debug=True)