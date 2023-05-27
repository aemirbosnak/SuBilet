
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
    return render_template('main.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
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

@app.route('/logout', methods =['GET', 'POST'])
def logout():
    session.pop('userid', default=None)
    session.pop('email', default=None)
    session.pop('loggedin', default=None)

    if 'userid' in session or 'username' in session or 'email' in session or 'loggedin' in session:
        logoutMessage = 'User cannot logged out successfully, try again'
        return render_template('tasks.html')
    
    logoutMessage = 'Successfully logged out!'
    return render_template('main.html', logoutMessage = logoutMessage)

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
 

@app.route('/travel/<vehicle_type>/from:<departure_city>/to:<arrival_city>/date:<departure_date>/', methods=['GET'])
def travels(vehicle_type, departure_city, arrival_city, departure_date):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    query = """
    SELECT *
    FROM Travel T
    JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
    JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
    JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
    WHERE Dep.city = %s
    AND Ar.city = %s
    AND DATE(T.depart_time) = %s
    AND V.type = %s
    """
    cursor.execute(query, (departure_city, arrival_city, departure_date, vehicle_type))
    searchedTravels = cursor.fetchall()
    return render_template('listAvailableTravelsPage.html', travels=searchedTravels)
    
# @app.route('/travels', methods=['GET', 'POST'])
# def travels():
#     if request.method == 'GET' and 'vehicleType' in request.form and 'departs_from' in request.form and 'arrives_to' in request.form and 'travelDate' in request.form:
#         vehicleType = request.form['vehicleType']
#         departs_from = request.form['departs_from']
#         arrives_to = request.form['arrives_to']
#         travelDate = request.form['travelDate']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#         query = """
#         SELECT *
#         FROM Travel T
#         JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
#         JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
#         JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
#         WHERE Dep.city = %s
#         AND Ar.city = %s
#         AND DATE(T.depart_time) = %s
#         AND V.type = %s
#         """
#         cursor.execute(query, (departs_from, arrives_to, travelDate, vehicleType))
#         searchedTravels = cursor.fetchall()
#         return render_template('travels.html', travels=searchedTravels)
#     else:
#         return redirect(url_for('login'))
    

@app.route('/trav', methods=['GET', 'POST'])
def listAvailableTravels():
    return render_template('listAvailableTravels.html')
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
