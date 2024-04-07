from flask import Flask, flash, render_template, request, redirect, session, url_for
import re
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key='6ede3c79f791dee2f4694d98ee678430'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='@Shara#23@'
app.config['MYSQL_DB']='rna'
mysql=MySQL(app)
# Function to validate the email
def is_valid_email(email):
    # Regular expression for validating an Email
    regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w+$'
    # If the string matches the regex, it is a valid email
    if re.search(regex, email):
        return True
    else:
        return False
    
@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        agree_policy = request.form.get('agree_policy')
        if not all([first_name, last_name, email, password, confirm_password]) or not agree_policy:
            error = "Please fill in all the fields and agree to the Terms of Service and privacy policy."
        elif password != confirm_password:
            error = "Passwords do not match. Please try again."
        elif not is_valid_email(email):
            error = "Please enter a valid email address."
        else:
            # Proceed with account creation
            return redirect(url_for('account'))
    if request.method=='POST':
        userDetails=request.form
        f_name=userDetails['first name']
        l_name=userDetails['last name']
        email=userDetails['email']
        password=userDetails['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM signup WHERE email=%s",(email))
        existing_user=cur.fectchone()
        if existing_user:
            flash ('Email already exists! Please use different email.')
            return redirect('/signup')
        else :
            cur.execute("INSERT INTO signup(first_name , last_name , email , password) VALUES(%s,%s,%s,%s)",(f_name,l_name,email,password))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
        

    return render_template('home.html', error=error)

@app.route('/database', methods=["GET", "POST"])
def database_page():
    if request.method == "POST":
        ...
    elif request.method == "GET":
        return render_template('database.html')

@app.route('/new', methods=["GET", "POST"])
def new_page():
    if request.method == "POST":
        ...
    elif request.method == "GET":
        return render_template('new.html')
@app.route('/en', methods=["GET", "POST"])  
def en_page():
    if request.method == "POST":
        ...
    elif request.method == "GET":
        return render_template('encrypt.html')
@app.route('/va', methods=["GET", "POST"])  
def va_page():
    if request.method == "POST":
        ...
    elif request.method == "GET":
        return render_template('va.html')
@app.route('/login' , methods=["GET","POST"])
def login():
    if request.method=='POST':
        userDetails=request.form
        email=userDetails['email']
        password=userDetails['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM signup WHERE email=%s AND password=%s", (email,password))
        user=cur.fetchall()
        if user:
         session['email']= email 
         return redirect('/database')
        else:
           return "Invalid email or password"
    return render_template('login.html')
   




@app.route('/account', methods=["GET","POST"])
def account():
    if request.method=='POST':
        userDetails=request.form
        f_name=userDetails['first name']
        l_name=userDetails['last name']
        email=userDetails['email']
        password=userDetails['password']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO signup(first_name , last_name , email , password ) VALUES(%s,%s,%s,%s)",(f_name,l_name,email,password))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template('account.html')

@app.route('/database')
def db():
    if 'email' in session :
        return render_template('database.html')
    else :
        return redirect('/login')
    

if __name__ == '__main__':
    app.run(debug=True)