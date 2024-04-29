from flask import Flask, flash, render_template, request, redirect, session, url_for, jsonify
import re
from flask_mysqldb import MySQL
import mysql.connector
from aes_program import encrypt_file, decrypt_file


# database iconnection
connection = mysql.connector.connect(host="localhost", user="root", passwd="@Shara#23@", database="rna")


cursor = connection.cursor()
# some other statements with the help of cursor
connection.close()



app = Flask(__name__,template_folder="../Downloads")



app.secret_key='6ede3c79f791dee2f4694d98ee678430'

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
        f_name=userDetails['first_name']
        l_name=userDetails['last_name']
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
    if 'email' not in session:
        return redirect('/login')

    if request.method == "POST":
        ...
    else:  # This covers the "GET" method
        cur = mysql.connection.cursor()
        cur.execute("SELECT project_name FROM newdb")
        project_names = cur.fetchall()
        cur.close()
        return render_template('all.html', project_names=project_names)

@app.route('/all')
def all():
    return render_template('all.html')
@app.route('/new', methods=["GET", "POST"])
def new_page():
    if request.method == "POST":
        userDetails=request.form
        p_name=userDetails['project_name']
        description=userDetails['description']
        notes=userDetails['notes']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO newdb(project_name , description , notes)VALUES(%s,%s,%s)",(p_name,description,notes))
        mysql.connection.commit()
        cur.close()
        return redirect('/encrypt')
    elif request.method == "GET":
        return render_template('new.html')
    


@app.route('/en', methods=["GET", "POST"])  
def en_page():
    if request.method == "POST":
        file = request.files['file']
        key = request.form['key']
        key_size = int(request.form['key_size'])
        # Save the uploaded file temporarily
        file_path = r"C:\Users\Ranu Ramesh\Pictures\dna files"
        file.save(file_path)

        # Encrypt the file
        encrypt_file(file_path, key, key_size)

        # Return success message or redirect to another page
        return jsonify({'message': 'File encrypted successfully'})
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO upload(encryption_key)VALUES(%s)",(key))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('list_files'))
            


    elif request.method == "GET":
        return render_template('encrypt.html')

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    # Handle file decryption
    # Similar to file upload route but with decryption logic

    return jsonify({'message': 'File decrypted successfully'})

@app.route('/va', methods=["GET", "POST"])  
def va_page():
    if request.method == "POST":
       ...
    elif request.method == "GET":
        encryption_key = request.args.get('encryption_key')
        
    
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


@app.route('/sub')
def sub():
     return render_template('crip.html')


if __name__ == '__main__':
    app.run(debug=True)