import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite3 import *
from KNN import main as algo_main


# Configure application
app = Flask(__name__)
db = connect("Project.db")
# Ensure responses aren't cached

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def hp():
    return render_template("login.html")


@app.route("/airportdetails", methods=["GET", "POST"])
def airport_details():
    if request.method == "POST":
        airportid = request.form.get('airportid')
        year = request.form.get('year')
        city = request.form.get('city')
        name = request.form.get('name')
        state = request.form.get('state')
        country = request.form.get('country')

        params = (airportid, name, year, city, state, country)
        cur.execute("INSERT INTO airport VALUES(?, ?, ?, ?, ?, ?)", params)
        db.commit()
        return render_template("output.html", message='Succesfully Updated Airport Table')
    else:
        return render_template("airportdetails.html")


@app.route("/trafficdetails", methods=["GET", "POST"])
def traffic_details():
    if request.method == "POST":
        destination  = request.form.get('destiantion')
        north, south, east, west, north_east, south_east, south_west, north_west = request.form.get('north'), request.form.get('south'), \
        request.form.get('east'), request.form.get('west'), request.form.get('north-east'),request.form.get('south-east'), \
        request.form.get('south-west'), request.form.get('north-west')

        params = (north, north_east, east, south_east, south, south_west,west, north_west)
        cur.execute("INSERT INTO traffic VALUES(?, ?, ?, ?, ?, ?, ?, ?)", params)
        con.commit()
        return render_template("output.html", message="Succesfully Updated Airport Table")
    else:
        return render_template('trafficdetails.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        user_name = request.form.get('username')
        login_password = request.form.get('password')
        first_name = request.form.get('first name')
        last_name = request.form.get('last name')
        email = request.form.get('mail')
        confirm_password = request.form.get('confirmation')
        city = request.form.get('city')
        ph_no = request.form.get('mobile number')
        pincode = request.form.get('pincode')


        if not user_name:
            return render_template("error.html", message = "must enter username", code=403)

        if not login_password:
            return render_template("error.html", message = "must enter password", code=403)

        if not first_name:
            return render_template("error.html", message = "must enter first name", code=403)

        if not last_name:
            return render_template("error.html", message = "must enter last name", code=403)

        if not login_password == confirm_password:
            return render_template("error.html", message = "Passwords Mismatch!", code=403)

        if not email:
            return render_template("error.html", message = "must enter Email ID", code=403)

        params = (user_name, first_name, last_name, email, login_password, city, ph_no, pincode)
        rows = db.execute("INSERT INTO users (username, first_name, last_name, email, password, city, mobile, pincode) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", params)
        db.commit()
        session["user_id"] = rows.fetchall()[0]

        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return redirect(url_for("login"))
    else:
        return render_template("register.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":

        user_name = request.form.get('username')
        login_password = request.form.get('password')

        check = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user_name, login_password))
        check = check.fetchall()

        if not check:
            return render_template("error.html", message="No User Found with the Username!")

        session["user_id"] = check[0][0]
        return render_template("homepage.html")

    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("login.html")


@app.route("/search", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        source, destination = request.form.get('source'), request.form.get('destination')
        message = "Accuracy of the algorithm is: {}".format(algo_main())

        return render_template('error.html', message = message)
    else:
        return render_template("homepage.html")


@app.route("/myaccount", methods=["GET", "POST"])
def accountdetails():
    if session:
        params = (session["user_id"], )

        tmp = db.execute("SELECT * FROM users WHERE id=?", params)
        tmp = tmp.fetchall()
        return render_template("myaccount.html", details = tmp)
    else:
        return render_template('homepage.html')


@app.route("/changepassword", methods=["GET", "POST"])
def changepassword():
    if request.method == "POST":
        # Ensure current password is not empty
        if not request.form.get("current_password"):
            return render_template("error.html", message="must provide password")

        # Ensure new password is not empty
        if not request.form.get("New_Password"):
            return render_template("error.html", message="must provide New Password")

        # Ensure confirm password is not empty
        if not request.form.get("password"):
            return render_template("error.html", message="must provide Confirm Password")

        # Ensure new and confirm passwords match
        if not request.form.get("New_Password") == request.form.get("password"):
            return render_template("error.html", message="Passwords not matched!")

        params = (session["user_id"], )
        # Query database for user_id
        rows = db.execute("SELECT password FROM users WHERE id = ?", params)
        rows = rows.fetchall()

        # Ensure current password is correct
        if len(rows) != 1:
            return render_template("error.html", message="Many users")

        params = (request.form.get('password'), session["user_id"])
        rows = db.execute("UPDATE users SET PASSWORD = ? WHERE ID = ?", params)

        return render_template("output.html", message="Password Updated Successfully!")
    else:
        return render_template("changepassword.html")
