
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
    return main()

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        #create session
        if user:              
            session['loggedin'] = True
            session['userid'] = user['id']
            message = 'Logged in successfully!'
            return redirect(url_for('main'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)

@app.route('/logout', methods =['GET', 'POST'])
def logout():
    session.pop('userid', default=None)
    session.pop('loggedin', default=None)

    if 'userid' in session or 'username' in session or 'email' in session or 'loggedin' in session:
        logoutMessage = 'User cannot logged out successfully, try again'
        return render_template('main.html')
    
    logoutMessage = 'Successfully logged out!'
    return redirect(url_for('main'))

@app.route('/main', methods=['GET', 'POST'])
def main():
    #main displays findTravelPage wheter a user is logged in or not
    return findTravel()
 

@app.route('/travel/<string:vehicle_type>/from:<string:departure_city>/to:<string:arrival_city>/date:<string:departure_date>/', methods=['GET'])
def travels(vehicle_type, departure_city, arrival_city, departure_date):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    sort_type = 'T.depart_time'
    sort_in = 'earliest_to_latest'

    if request.method == 'GET' and 'sort_type' in request.args:
        sort_in = request.args.get('sort_type')

        if sort_in == 'earliest_to_latest':
            sort_type = 'T.depart_time'
        elif sort_in == 'latest_to_earliest':
            sort_type = 'T.depart_time DESC'
        elif sort_in == 'low_to_high':
            sort_type = 'T.price'
        elif sort_in == 'high_to_low':
            sort_type = 'T.price DESC'

    query = """
    SELECT C.id AS company_id, C.company_name, T.travel_id, T.depart_time, T.arrive_time, T.price, T.business_price, Dep.name AS dep_terminal_name, Dep.city AS dep_city, Ar.name AS ar_terminal_name, Ar.city AS ar_city
    FROM Travel T
    JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
    JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
    JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
    JOIN Company C ON T.travel_company_id = C.id
    WHERE Dep.city = %s
    AND Ar.city = %s
    AND DATE(T.depart_time) = %s
    AND V.type = %s
    ORDER BY {}
    """.format(sort_type)

    is_logged_in = session.get('loggedin', False)       #retrieves the value of is_logged_in from the session, if it's not present in the session, the default value False is used.
    user_id = session.get('userid')
    
    # cursor.execute(query)
    cursor.execute(query, (departure_city, arrival_city, departure_date, vehicle_type))
    searchedTravels = cursor.fetchall()

    return render_template('listAvailableTravelsPage.html', is_logged_in=is_logged_in, user_id=user_id, searchedTravels=searchedTravels, vehicleType = vehicle_type, arrivalCity = arrival_city, departureCity = departure_city, departureDate = departure_date, sortType=sort_in)


@app.route('/findTravel', methods=['GET', 'POST'])
def findTravel():
    #get cities from terminal table to show in drop down menu
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT DISTINCT city FROM Terminal ORDER BY city ASC"
    cursor.execute(query)

    cities = [row['city'] for row in cursor.fetchall()]
    is_logged_in = session.get('loggedin', False)       #retrieves the value of is_logged_in from the session, if it's not present in the session, the default value False is used.
    user_id = session.get('userid')

    if request.method == 'POST': 
        vehicle_type = request.form['vehicle_type']
        departure_city = request.form['from-location']
        arrival_city = request.form['to-location']
        departure_date = request.form['departure_date']

        #perform checks
        if not departure_city or not arrival_city or not departure_date:
            error_message = "Please select fill in the form."
            return render_template('main.html', cities=cities, is_logged_in=is_logged_in, user_id =user_id, error_message=error_message)

        #redirect to listAvailableTravelsPage.html with relevant information
        return redirect(url_for('travels', vehicle_type=vehicle_type, departure_city=departure_city, arrival_city=arrival_city, departure_date=departure_date))
        
    #main.html is the current design
    return render_template('main.html', cities=cities, is_logged_in=is_logged_in, user_id=user_id)

@app.route('/myTravels', methods=['GET', 'POST'])
def myTravels():
    user_id = session.get('userid')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    query = """
    SELECT Booking.PNR, Travel.depart_time, Terminal.name AS departure_terminal_name, Terminal2.name AS arrival_terminal_name, Company.company_name
    FROM Booking
    JOIN Travel ON Booking.travel_id = Travel.travel_id
    JOIN Terminal ON Travel.departure_terminal_id = Terminal.terminal_id
    JOIN Terminal AS Terminal2 ON Travel.arrival_terminal_id = Terminal2.terminal_id
    JOIN Company ON Travel.travel_company_id = Company.id
    WHERE Booking.traveler_id = %s;
    """
    cursor.execute(query, (user_id,))
    user_travels = cursor.fetchall()

    return render_template('myTravelsPage.html', user_travels=user_travels, user_id=user_id)

@app.route('/coupons/<int:user_id>', methods=['GET', 'POST'])
def coupons(user_id):
    return render_template('couponsPage.html', user_id=user_id)

@app.route('/userProfile/<int:user_id>', methods=['GET', 'POST'])
def userProfile(user_id): 
    if 'userid' in session and 'loggedin' in session:
        #get user information
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
        SELECT id, email, phone, TCK, name, surname, age, balance
        FROM User U NATURAL JOIN Traveler T
        WHERE U.id = %s AND U.active = TRUE
        """
        cursor.execute(query, (user_id,))
        userInfo = cursor.fetchone()
        return render_template('userProfile.html', user_id = user_id, userInfo = userInfo)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)
    

@app.route('/updateTravelerProfile/<int:user_id>', methods=['GET', 'POST'])
def updateTravelerProfile(user_id):
    if 'userid' in session and 'loggedin' in session:
        if request.method == 'POST':
            newEmail = request.form['email']
            newPhone = request.form['phone']
            newName = request.form['name']
            newSurname = request.form['surname']
            newAge = request.form['age']

            #get user information
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = """
            SELECT id, email, phone, TCK, name, surname, age, balance
            FROM User U NATURAL JOIN Traveler T
            WHERE U.id = %s AND U.active = TRUE
            """
            cursor.execute(query, (user_id,))
            userCurrentInfo = cursor.fetchone()

            updateQuery = "UPDATE User SET email = %s, phone = %s WHERE id = %s "
            cursor.execute(updateQuery, (newEmail, "888 888 88 88", user_id,))
            
            if(userCurrentInfo['email'] != newEmail or userCurrentInfo['phone'] != newPhone):
                updateQuery = "UPDATE User SET email = %s, phone = %s WHERE id = %s "
                cursor.execute(updateQuery, (newEmail, "888 888 88 88", user_id,))

            if(userCurrentInfo['name'] != newName or userCurrentInfo['surname'] != newSurname or userCurrentInfo['age'] != newAge ):
                updateQuery = "UPDATE Traveler SET name = %s, surname = %s, age = %s WHERE id = %s"
                cursor.execute(updateQuery, (newName, newSurname, newAge, user_id,))
            
        return redirect(url_for('userProfile', user_id = user_id))
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
