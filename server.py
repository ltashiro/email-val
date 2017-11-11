from flask import Flask, render_template, redirect, request, session, flash
import re 
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'Secretkey'
mysql = MySQLConnector (app,'emailsdb')#accessing the email database

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/') #bring out the webpage
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    form_valid = True
    if len(request.form['email']) == 0:
        flash ("Email cannot be blank")
        form_valid = False
    elif not EMAIL_REGEX.match(request.form['email']):
        flash ("Email is invalid")
        form_valid = False
    else:
        email = request.form ['email']
        session['email'] = email
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
             'email': request.form['email'],
           }
        mysql.query_db(query, data)
        return redirect('/success')


@app.route('/success', methods =['GET'])
def display():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    return render_template('success.html', emails=emails)

app.run(debug=True)
