from dataclasses import asdict
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from requests import session
# -/-/-/-/-/-/-/- # -> import statments 

"""
Hello nosy person looking through my code ( *・∀・)ノ゛!
I am currently extremly busy with university as the semester is coming to an end.
This project was completed in less than a day. I did my besy QA I could.
If you manage to break it somehow, fix it yourself :]
"""
# -/-/-/-/-/-/-/- # -> personal comments 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# -/-/-/-/-/-/-/- # -> terminal colors for better prints

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
# -/-/-/-/-/-/-/- # -> flask initializing

FireConfig = {
  "apiKey": "AIzaSyDOXZaRXvOpvszT4GoQZO1lmePP0jasTHc",
  "authDomain": "meet-moment.firebaseapp.com",
  "databaseURL": "https://meet-moment-default-rtdb.firebaseio.com",
  "projectId": "meet-moment",
  "storageBucket": "meet-moment.appspot.com",
  "messagingSenderId": "1008366474325",
  "appId": "1:1008366474325:web:ef4691e4b35fcdd7fcb0dc",
  "measurementId": "G-DRN841W2WP"
}

FireBase = pyrebase.initialize_app(FireConfig)
FireAuth = FireBase.auth()
DataBase = FireBase.database()
# -/-/-/-/-/-/-/- # -> firebase initializing

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' in login_session:
            return render_template("mainpage.html")
    else:
        return render_template("home.html")
# -/-/-/-/-/-/-/- # 

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in login_session:
        del login_session['username'] # deleting current logged in user
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
# -/-/-/-/-/-/-/- #

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        # -> getting information from html login form

        try:
            login_session['user'] = FireAuth.sign_in_with_email_and_password(email, password) 
            # -> user logged in successfully (from authentication)
            user = DataBase.child("Users").child(login_session['user']['localId']).get() # user object 
            # -> user found in the databse successfully
            userID = user.key()
            userInfo = user.val()['name']
            # -> accessing user values and attributes
            login_session['username'] = userInfo
            # -> user logged in flask session successfully

            print(f"{bcolors.OKBLUE}SignIN succ, email: {email}, password: {password}")
            return render_template("mainpage.html", userID = userID)
            # -> passing the userID to html file for viewing

        except:
            flash("Email or Password Incorrect!")
            return redirect(url_for('home'))
    else:
        return render_template("home.html")
# -/-/-/-/-/-/-/- #

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # -> getting information from html signup form 
        
        try:
            # hate this stupid name for a fucntion but whatever works i guess ¯\_(ツ)_/¯
            login_session['user'] = FireAuth.create_user_with_email_and_password(email, password)
            # -> user created successfully (for authentication)
            user = {"name":name, "email":email}
            DataBase.child("Users").child(login_session['user']['localId']).set(user)
            # -> user added to database successfully

            print(f"{bcolors.OKBLUE}SignUp succ, email: {email}, password: {password}")
            flash("SignUp successful!")
            return redirect(url_for('home'))

        except:       
            flash("Somethign went wrong :( ")
            return redirect(url_for('home'))
    else:
        return render_template("home.html")
# -/-/-/-/-/-/-/- #

if __name__ == '__main__':
    app.run(debug=True)