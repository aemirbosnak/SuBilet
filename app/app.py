
import re  
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__, static_folder='static') 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'subiletdb'
  
mysql = MySQL(app)  

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    print("I am here")
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        print("I am here")
        #create session
        if user:              
            session['loggedin'] = True
            session['userid'] = user['id']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('main'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)

# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('userid', None)
#     return redirect(url_for('login'))

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'loggedin' in session:

        # # Display tasks
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM Task WHERE user_id = %s AND status = %s ORDER BY deadline ASC', (session['userid'], 'Todo'))
        # tasks = cursor.fetchall()

        # # Display completed tasks
        # cursor.execute('SELECT * FROM Task WHERE user_id = %s AND status = %s ORDER BY done_time DESC', (session['userid'], 'Done'))
        # completed_tasks = cursor.fetchall()

        # cursor.execute('SELECT * FROM TaskType')
        # task_types = cursor.fetchall()

        return render_template('main.html')
    
    else:
        return redirect(url_for('main'))
 

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
