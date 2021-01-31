from flask import Flask, redirect, url_for, render_template, request, session, flash
import os
from pyautogui import hotkey
from datetime import timedelta
from functions import register, reload_files
from databaseControl import *


app = Flask(__name__)
app.secret_key = "8ghBsjdwagk2389sdgahwbr325te78gdau"
app.permanent_session_lifetime = timedelta(weeks=2)

users_file = open('users','r')
users = users_file.read()
users = users.strip('\n')
users_file.close()

passwords_file = open('passwords','r')
passwords = passwords_file.read()
passwords = passwords.strip('\n')
passwords_file.close()

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/login', methods=["POST",'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user_ = request.form['nm']
        password_ = request.form['ps']
        returns = checkUser(user_,password_)
        if returns == False:
            flash(user_.upper() + " and " + password_.upper() + " are not registerd, contact the administrator")
            return redirect(url_for('login'))
        elif returns == 1:
            return redirect(url_for('admin'))
        elif returns == 2 or returns == 3:
            return redirect(url_for('user'))
    else:
        if "admin" in session:
            flash("Already loged-in")
            return redirect(url_for('admin'))
        if 'user' in session:
            flash("Already loged-in")
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/login/logout')
def logout():
    if "admin" in session:
        user_ = session['admin']
        flash(user_ + " has loged out successefully!", "info")
    if 'user' in session:
        user_ = session['user'][0]
        flash(user_ + " has loged out successefully!", "info")
    session.pop("admin", None)
    session.pop('user', None)
    reload_files()
    
    return redirect(url_for('login'))

@app.route('/user')
def user():
    if 'user' in session:
        permLevel = session['user'][1]
        if permLevel == 2:
            return render_template('user2.html')
        if permLevel == 3:
            return render_template('user3.html')
        return
    else:
        flash("Log in First!")
        return redirect(url_for('login'))

@app.route('/admin', methods=['POST','GET'])
def admin():
    if "admin" in session: 
        if request.method == 'POST':
            user_ = session["admin"]
        return render_template('admin.html')
    else:
        flash("Log in First")
        return redirect(url_for('login'))

@app.route('/admin/register', methods=['POST','GET'])
def admin_register():
    if "admin" in session: 
        if request.method == 'POST':
            new_user = request.form['nm']
            new_passwrd = request.form['ps']
            new_perm = request.form['pl']
            createNewUser(new_user,new_passwrd,new_perm)
            commit()
            flash(new_user.upper() + " with password " + new_passwrd.upper() + " registerd\nNow reboot the website")
        return render_template('admin_register.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin/allusers', methods=['POST','GET'])
def admin_allusers():
    if 'admin' in session:
        items = all3users()
        return render_template('admin_allusers.html',users=items)
    else:
        flash('Log in first')
        return redirect(url_for('login'))

@app.route('/admin/resetDB', methods=['POST','GET'])
def resetDB():
    if 'admin' in session:
        if request.method == 'POST':
            sure = request.form['sure']
            if sure == 'banana':
                resetTable()
                flash("DataBase has reset successefully")
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('admin'))
        return render_template('admin_resetDB.html')
    else:
        flash('Log in first')
        return redirect(url_for('login'))

@app.route('/servers')
def servers():
    return render_template('servers.html')

@app.route('/servers/<servername>')
def servers_(servername):
    if "admin" in session:
        if servername == "7c-smp":
            return render_template('7c-smp.html')
        elif servername == "walter":
            return render_template('walter.html')
        elif servername == "web-server":
            return redirect(url_for('homepage'))
    if 'user' in session:
        permLevel = session['user'][1]
        if permLevel == 2:
            if servername == "7c-smp":
                return render_template('7c-smp.html')
            else:
                return render_template('not_allowed.html')
        if permLevel == 3:
            if servername == "our-sever":
                return
    else:
        flash("Log in first!")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=1000)