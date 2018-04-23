from flask import Flask, request, redirect
import cgi
import re
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)
 
app = Flask(__name__)
app.config['DEBUG'] = True

def is_blank(stringinput):
    if stringinput == "" or " " in stringinput:
        return True
    else:
        return False

def valid_legnth(stringinput):
    if len(stringinput) > 2 and len(stringinput) < 20:
        return True
    else:
        return False 

def valid_characters(stringinput):
    lan = r"[^A-Za-z0-9]"
    if re.search(lan,stringinput):
        return False
    else:
        return True

def valid_email(stringinput):
    if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", stringinput) != None:
        return True
    else:
        return False    








@app.route("/")
def index():
    template = jinja_env.get_template('user-signup.html')
    username_error =""
    password_error =""
    verify_error =""
    email_error =""
    username =""
    email=""
    return template.render(username = username,email = email,
 username_error=username_error, password_error = password_error,
  verify_error = verify_error, email_error = email_error)

@app.route("/", methods=['POST'])
def submit():
    template = jinja_env.get_template('user-signup.html')
    username = cgi.escape(request.form['username'])
    password = cgi.escape(request.form['password'])
    verify = cgi.escape(request.form['verify'])
    email = cgi.escape(request.form['email'])
    username_error = ""
    password_error = ""
    verify_error = ""
    email_error = ""


    if (is_blank(username)) == True:
        username_error = "That's not a valid username"

    if (is_blank(password)) == True:
        password_error = "That's not a valid password"

    if (valid_legnth(username)) == False:
        username_error = "That's not a valid username"

    if (valid_legnth(password)) == False:
        password_error = "That's not a valid password"

    if (valid_characters(username)) == False:
        username_error = "That's not a valid username"

    if (valid_characters(password)) == False:
        password_error = "That's not a valid password"

    if password != verify:
        verify_error = "Passwords don't match"


    if email != "":
        if (valid_legnth(email)) == False:
            email_error = "That's not a valid Email"

        if " " in email:
            email_error = "That's not a valid Email"

        if (valid_email(email)) == False:
            email_error = "That's not a valid Email"

    if not username_error and not password_error and not verify_error and not email_error:
        return redirect("/welcome?username={0}".format(username))


    return template.render(username = username, password = "",
 verify ="", email = email, username_error=username_error,
 password_error = password_error, verify_error = verify_error,
email_error = email_error)

@app.route("/welcome")
def welcome():

    username = cgi.escape(request.args.get('username'))
    template = jinja_env.get_template('welcome.html')
   
    return template.render(username = username)



app.run()



# username_error = "That's not a valid username"
# password_error = "That's not a valid password"
# verify_error = "Passwords don't match"
# email_error = "That's not a valid email"
