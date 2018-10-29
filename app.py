from flask import Flask, render_template, request, g, redirect, url_for, flash, Response, session, send_from_directory
from dbconnect import connection
from MySQLdb import escape_string as thwart
from flask_bootstrap import Bootstrap
from flask_oauth import OAuth
import google.oauth2.credentials
import googleapiclient.discovery
import google_auth_oauthlib.flow
import os
import urllib
import boto3
import gc
from flask_wtf import FlaskForm
from functools import wraps
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from filters import datetimeformat, file_type 
from resources import get_bucket, get_buckets_list
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'
app.config.update(DEBUG = True,)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type


class RegistrationForm(Form):
   username = TextField('Username', [validators.Length(min=3, max=20)])
   firstname = TextField('First name', [validators.Length(min=3, max=20)])
   lastname = TextField('Last name', [validators.Length(min=3, max=20)])
   email = TextField('Email Address', [validators.Required()])
   password = PasswordField('Password', [validators.Required(), 
   validators.EqualTo('confirm', message="Passwords must match.")])
   confirm = PasswordField('Retype Password')
   

@app.route('/register/', methods=['GET','POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.username.data
	    firstname = form.firstname.data
	    lastname = form.lastname.data
            email = form.email.data
            password = str(form.password.data)
	    c, conn = connection()
            x = c.execute("SELECT * FROM users WHERE username = (%s)", 
            (thwart(username),))
            if int(x) > 0:
                flash("Username already exists")
                return render_template('register.html', form=form)
            else:
                c.execute("INSERT INTO users (username, firstname, lastname, password, email, tracking) VALUES ( %s, %s, %s, %s, %s, %s)", (thwart(username), thwart(firstname), thwart(lastname),
                    thwart(password), thwart(email), thwart("/FILE DRIVE/")))
                conn.commit()
                flash("Thank you for registering!")
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
        return render_template("register.html", form=form)        
    except Exception as e:
        return(str(e))


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Need to login first")
            return redirect(url_for('login_page'))

    return wrap

@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
   # session.clear()
    session['logged_in'] = False
    session.pop('username')
    flash("Logged out")
   # gc.collect()
    return redirect(url_for('index'))

@app.route('/login/<userid>/<name>', methods=['GET', 'POST'])
def files_fb(userid, name):
    # check if the username exists in the database
    firstname = ''
    lastname = ''
    password = ''
    email = ''
    name_good = urllib.unquote(name)
    name_arr = name_good.split(' ')
    if len(name_arr) >=2:
        firstname = name_arr[0]
        lastname = name_arr[1]
    elif len(name_arr) == 1:
        firstname = name_arr[0]
    print firstname, lastname

    try:
        c, conn = connection()
        x = c.execute("SELECT * FROM users WHERE username = (%s)", (thwart(userid),))
        if int(x) > 0:
	    print 'User Found in db'
	else:
	    #c.execute("DELETE FROM users WHERE username=%s", thwart(userid))
	    #conn.commit()
	    c.execute("INSERT INTO users (username, firstname, lastname, password, email, tracking) VALUES ( %s, %s, %s, %s, %s, %s)", (thwart(userid), thwart(firstname), thwart(lastname),
                    thwart(password), thwart(email), thwart("/FILE DRIVE/")))
            conn.commit()
	    print 'use ' + userid + ' added to database'
	    flash('User ' + userid + 'added to database')
	
	session['logged_in'] = True
        session['username'] = userid
	print 'Hello' + session['username']

        flash("Hello " + session['username'])
        return redirect(url_for("files"))
    except Exception as e:
        return(str(e))


@app.route('/login/', methods=['GET','POST'])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             (thwart(request.form['username']),))
            password_db = c.fetchone()[4]
	    if str(request.form['password']) ==  password_db:
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("Hello " + session['username'])
                return redirect(url_for("files"))
            else:
                error = "Invalid credentials, try again."
        gc.collect()
        return render_template("login.html", error=error)

    except Exception as e:
        flash(e)
        error = "Invalid credentials, try again (Exception)."
        return render_template("login.html", error = error)  

@app.route('/', methods=['GET', 'POST'])
def index():
   return  render_template("index.html")

class myfile:
    def __init__(self, name, firstname, lastname, desc, upload, update):
	self.key = name
	self.desc = desc
	self.upload = upload
	self.update = update
	self.firstname = firstname
	self.lastname = lastname

@app.route('/files', methods=['GET', 'POST'])
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()
    userfiles = []

    for file in summaries:
	try:
	    c, conn = connection()
	   # find the details from the userfiles DB
	    data = c.execute("SELECT * FROM userfiles WHERE filepath = (%s)", (thwart(file.key),))
	    fetched_data = c.fetchone()
	    my_file = myfile(file.key, fetched_data[2], fetched_data[3], fetched_data[7], fetched_data[5], fetched_data[6])
	    username_returned = file.key.split('/')[0]
            if session['username'] == username_returned:
       		userfiles.append(my_file)
       	    elif session['username'] == 'admin':
                userfiles.append(my_file)	
	except Exception as e:
	    print e

    return render_template('files.html',files=userfiles)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    my_bucket = get_bucket()
    filepath = str(session['username']+'/'+file.filename)
    my_bucket.Object(filepath).put(Body=file)

    summaries = my_bucket.objects.filter(Prefix=filepath)
    for file in summaries:
	timestamp = file.last_modified.strftime('%Y-%m-%d %H:%M:%S')    	

    description = request.form['description']
    first_name = ''
    last_name = ''
    try:
        c, conn = connection()
        data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             (thwart(session['username']),))
        fetched_data = c.fetchone()
        first_name = fetched_data[2]
        last_name = fetched_data[3]
    except Exception as e:
	flash(e)

    try:
	c, conn = connection()
        x = c.execute("SELECT * FROM userfiles WHERE filepath = (%s)", (thwart(filepath),))
        if int(x) > 0:
	    c.execute("update userfiles set updatedtime = %s, description = %s where filepath = %s", (thwart(timestamp), thwart(description), thwart(filepath)))
            conn.commit()
	else:
	    c.execute("INSERT INTO userfiles (username, firstname, lastname, filepath, uploadtime, updatedtime, description) VALUES (%s, %s, %s, %s, %s, %s, %s)", (thwart(session['username']), thwart(first_name), thwart(last_name), thwart(filepath), thwart(timestamp), thwart(timestamp), thwart(description)))
            conn.commit()
		
    except Exception as e:
        return(str(e))


    flash('File uploaded successfully'+ timestamp + description)
    return redirect(url_for('files'))


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template("privacy.html")

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()
    link = "https://d1el42vvlz2y8n.cloudfront.net/" + str(key)
    f = urllib.urlopen(link)
    myfile = f.read()
    return Response(
       file_obj['Body'].read(),
   #	myfile,
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
