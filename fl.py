from flask import Flask,  render_template, request, redirect, url_for, jsonify
import re

from aes_program import encrypt_file
import os


# database iconnection





app = Flask(__name__)





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
        
        if password != confirm_password:
            error = "Passwords do not match. Please try again."
        elif not is_valid_email(email):
            error = "Please enter a valid email address."
        else:
            # Proceed with account creation
            return redirect(url_for('login'))
    
        

    return render_template('home.html',error=error)

@app.route('/database', methods=["GET", "POST"])
def database_page():
   

    if request.method == "POST":
        ...
    else:  # This covers the "GET" method
        return render_template('database.html')
    

@app.route('/all')
def all():
    return render_template('all.html')
@app.route('/new', methods=["GET", "POST"])
def new_page():
    if request.method == "POST":
       return redirect(url_for('encrypt'))
    return render_template('new.html')


@app.route('/qw')
def qw():
    return render_template('qw.html')
@app.route('/en', methods=["GET", "POST"])  
def en_page():
    if request.method == "POST":
        file = request.files['file']
        key = request.form['key']
        key_size = int(request.form['keySize'])
        # Save the uploaded file temporarily
        file_path = r"C:\Users\Ranu Ramesh\Pictures\dna files"
        file.save(file_path)

        # Encrypt the file
        encrypt_file(file_path, key, key_size)

        # Return success message or redirect to another page
        return jsonify({'message': 'File encrypted successfully'})
    elif request.method == "GET":
        return render_template('encrypt.html')

@app.route('/va', methods=["GET", "POST"])  
def va_page():
    if request.method == "POST":
       ...
    elif request.method == "GET":
        ...
        
    
    return render_template('va.html')



@app.route('/login' , methods=["GET","POST"])
def login():
    error=None
    if request.method=='POST':
        userDetails=request.form
        email=userDetails['email']
        password=userDetails['password']
        
        return redirect('/database')
        
    return render_template('login.html',error=error)
   




@app.route('/account', methods=["GET","POST"])
def account():
    error = None
    if request.method=='POST':
        userDetails=request.form
        f_name=userDetails['first_name']
        l_name=userDetails['last_name']
        email=userDetails['email']
        password=userDetails['password']
        confirm_password = request.form['confirm_password']

        agree_policy = request.form.get('agree_policy')
        
        if password != confirm_password:
            error = "Passwords do not match. Please try again."
        elif not is_valid_email(email):
            error = "Please enter a valid email address."
        else:
            # Proceed with account creation
            return redirect('/login')

    return render_template('account.html', error=error)



if __name__ == '__main__':
    app.run(debug=True)
