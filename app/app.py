
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
app.config['MYSQL_DB'] = 'subilet'
  
mysql = MySQL(app)  

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:              
            session['loggedin'] = True
            session['userid'] = user['id']
            session['email'] = user['email']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('main'))
        else:
            message = 'Please enter correct email / password !'

    return render_template('login.html', message = message)

@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'email' in request.form :
        email = request.form['email']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different email!'
  
        elif not email or not password or not email:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO User (id, email, email, password) VALUES (NULL, % s, % s, % s)', (username, email, password,))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':

        message = 'Please fill all the fields!'
    return render_template('register.html', message = message)

# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('userid', None)
#     return redirect(url_for('login'))

# @app.route('/main', methods=['GET', 'POST'])
# def main():
#     if 'loggedin' in session:

#         # Display tasks
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM Task WHERE user_id = %s AND status = %s ORDER BY deadline ASC', (session['userid'], 'Todo'))
#         tasks = cursor.fetchall()

#         # Display completed tasks
#         cursor.execute('SELECT * FROM Task WHERE user_id = %s AND status = %s ORDER BY done_time DESC', (session['userid'], 'Done'))
#         completed_tasks = cursor.fetchall()

#         cursor.execute('SELECT * FROM TaskType')
#         task_types = cursor.fetchall()

#         return render_template('main.html', tasks=tasks, completed_tasks=completed_tasks, task_types=task_types)
    
#     else:
#         return redirect(url_for('login'))
 
# @app.route('/add_task', methods=['GET', 'POST'])
# def add_task():
#     if 'loggedin' in session:
#         if request.method == 'POST':
#             title = request.form['title']
#             description = request.form['description']
#             task_type = request.form['task_type']
#             user_id = session['userid']
#             deadline_str = request.form['deadline']
#             deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
#             creation_time = datetime.now()

#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('INSERT INTO Task(title, description, status, deadline, task_type, creation_time, user_id) VALUES(%s, %s, %s, %s, %s, %s, %s)', (title, description, 'Todo', deadline, task_type, creation_time, user_id))
#             mysql.connection.commit()

#             return redirect(url_for('main'))

#     else:
#         return redirect(url_for('login'))
    
# @app.route('/finish_task/<int:task_id>', methods=['POST'])
# def finish_task(task_id):
#     if 'loggedin' in session:
#         if request.method == 'POST':
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             time = datetime.now()
#             cursor.execute('UPDATE Task SET status = %s, done_time = %s WHERE id = %s AND user_id = %s', ('Done', time, task_id, session['userid']))
#             mysql.connection.commit()

#             return redirect(url_for('main'))
    
#     else:
#         return redirect(url_for('login'))
    
# @app.route('/delete_task/<int:task_id>', methods=['POST'])
# def delete_task(task_id):
#     if 'loggedin' in session:
#         if request.method == 'POST':
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('DELETE FROM Task WHERE id = %s AND user_id = %s', (task_id, session['userid']))
#             mysql.connection.commit()

#             return redirect(url_for('main'))

#     else:
#         return redirect(url_for('login'))

# @app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
# def edit(task_id):
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM Task WHERE id = %s AND user_id = %s', (task_id, session['userid']))
#         task = cursor.fetchone()

#         cursor.execute('SELECT * FROM TaskType')
#         task_types = cursor.fetchall()

#         return render_template('edit.html', task=task, task_types=task_types)
    
#     else:
#         return redirect(url_for('login'))
    
# @app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
# def edit_task(task_id):
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
#         if request.method == 'POST':
#             title = request.form['title']
#             description = request.form['description']
#             task_type = request.form['task_type']
#             deadline_str = request.form['deadline']
#             deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')

#             cursor.execute('UPDATE Task SET title = %s, description = %s, task_type = %s, deadline = %s WHERE id = %s AND user_id = %s', (title, description, task_type, deadline, task_id, session['userid']))
#             mysql.connection.commit()

#             return redirect(url_for('main'))

#     else:
#         return redirect(url_for('login'))

# @app.route('/analysis', methods =['GET', 'POST'])
# def analysis():
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT title, (done_time - deadline) AS latency FROM Task WHERE user_id = %s AND status = %s AND done_time > deadline', (session['userid'], 'Done'))
#         late_tasks = cursor.fetchall()

#         cursor.execute('SELECT AVG(TIMESTAMPDIFF(SECOND, creation_time, done_time)) AS avg_time FROM Task WHERE user_id = %s AND status = %s', (session['userid'], 'Done'))
#         avg_time = cursor.fetchone()['avg_time']

#         cursor.execute('SELECT task_type, COUNT(*) AS num_completed FROM Task WHERE user_id = %s AND status = %s GROUP BY task_type ORDER BY num_completed DESC', (session['userid'], 'Done'))
#         completed_by_type = cursor.fetchall()

#         cursor.execute('SELECT title, deadline FROM Task WHERE user_id = %s AND status = %s ORDER BY deadline ASC', (session['userid'], 'Todo'))
#         uncompleted_tasks = cursor.fetchall()

#         cursor.execute('SELECT title, TIMESTAMPDIFF(SECOND, creation_time, done_time) AS time_taken FROM Task WHERE user_id = %s AND status = %s ORDER BY time_taken DESC LIMIT 2', (session['userid'], 'Done'))
#         longest_tasks = cursor.fetchall()

#         return render_template('analysis.html', late_tasks=late_tasks, avg_time=avg_time, completed_by_type=completed_by_type, uncompleted_tasks=uncompleted_tasks, longest_tasks=longest_tasks)

#     else:
#         return redirect(url_for('login'))
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
