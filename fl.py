from flask import Flask, render_template, request, redirect, url_for
import re
from waitress import serve 
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
        if not all([first_name, last_name, email, password, confirm_password]) or not agree_policy:
            error = "Please fill in all the fields and agree to the Terms of Service and privacy policy."
        elif password != confirm_password:
            error = "Passwords do not match. Please try again."
        elif not is_valid_email(email):
            error = "Please enter a valid email address."
        else:
            # Proceed with account creation
            return redirect(url_for('account'))

    return render_template('home.html', error=error)

@app.route('/account')
def account():
    return render_template('account.html')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=50100 , threads=2)