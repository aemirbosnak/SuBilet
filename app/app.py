
import re  
import os
import random, string
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__, static_folder='static') 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'subiletdb'
  
mysql = MySQL(app)  

#### CONSTANTS ####
PNR_LENGTH = 8

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

        cursor.execute('SELECT * From Traveler WHERE id = %s ', (user['id'],))
        userTraveler = cursor.fetchone()

        cursor.execute('SELECT * From Company WHERE id = %s ', (user['id'],))
        userCompany = cursor.fetchone()

        cursor.execute('SELECT * From Administrator WHERE id = %s', (user['id'],))
        userAdmin = cursor.fetchone()

        if userTraveler:
            userType = 'traveler'
        elif userCompany:
            userType = 'company'
        elif userAdmin:
            userType = 'admin'

        #create session
        if user:              
            session['loggedin'] = True
            session['userid'] = user['id']
            session['userType'] = userType
            message = 'Logged in successfully!'
            return redirect(url_for('main'))
        else:
            message = 'Please enter correct email / password !'

        cursor.close()
    
    return render_template('login.html', message = message)

@app.route('/travelerRegister', methods =['GET', 'POST'])
def travelerRegister():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'passwordRepeat' in request.form and 'phone' in request.form and 'TCK' in request.form and 'name' in request.form and 'surname' in request.form and 'age' in request.form :
        email = request.form['email']
        password = request.form['password']
        passwordRepeat = request.form['passwordRepeat']
        phone = request.form['phone']
        TCK = request.form['TCK']
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM User WHERE email = %s ', (email, ))
        accountExistWithSameEmail = cursor.fetchone()

        cursor.execute('SELECT * FROM User WHERE phone = %s ', (phone, ))
        accountExistWithSamePhone = cursor.fetchone()

        cursor.execute('SELECT * FROM Traveler WHERE TCK = %s ', (TCK, ))
        accountExistWithSameTCK = cursor.fetchone()

        if not email or not password or not phone or not TCK or not name or not surname or not age:
            message = 'Please fill out the form!'
        elif accountExistWithSameEmail:
            message = 'There is already an account with that email!'
        elif accountExistWithSameTCK:
            message = 'There is already an account with this TCK!'
        elif accountExistWithSamePhone:
            message = 'There is already an account with this phone number!'
        elif password != passwordRepeat:
            message = 'Password mismatch. Please enter same password!'
        elif int(age) < 18:
            message = 'To register, you must be bigger than 18 years old!'   
        else:
            cursor.execute('INSERT INTO User (id, email, password, phone, active) VALUES (NULL, % s, % s, % s, TRUE)', (email, password, phone, ))
            mysql.connection.commit()
            # find newly added traveler
            cursor.execute('SELECT * FROM User WHERE email = %s ', (email, ))
            newUser = cursor.fetchone()
            # get the user id and insert this user into Traveler
            newUserId = newUser['id']
            cursor.execute('INSERT INTO Traveler (id, TCK, name, surname, age, balance) VALUES (%s, % s, % s, % s, %s, 0)', (newUserId, TCK, name, surname, age, ))
            mysql.connection.commit()
            message = 'User successfully created! Please log in.'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('travelerRegister.html', message = message)

@app.route('/companyRegister', methods =['GET', 'POST'])
def companyRegister():
    message = ''
    if request.method == 'POST' and 'companyName' in request.form and 'companyEmail' in request.form and 'companyPhone' in request.form and 'website' in request.form and 'password' in request.form and 'passwordRepeat' in request.form:
        companyName = request.form['companyName']
        companyEmail = request.form['companyEmail']
        password = request.form['password']
        passwordRepeat = request.form['passwordRepeat']
        companyPhone = request.form['companyPhone']
        website = request.form['website']
        foundationDate = request.form['foundationDate']
        aboutCompany = request.form['aboutCompany']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM User WHERE email = %s ', (companyEmail, ))
        accountExistWithSameEmail = cursor.fetchone()

        cursor.execute('SELECT * FROM User WHERE phone = %s ', (companyPhone, ))
        accountExistWithSamePhone = cursor.fetchone()

        cursor.execute('SELECT * FROM Company WHERE company_name = %s ', (companyName, ))
        accountExistWithSameName = cursor.fetchone()

        cursor.execute('SELECT * FROM Company WHERE website = %s ', (website, ))
        accountExistWithSameWebsite = cursor.fetchone()

        if not companyName or not companyEmail or not password or not passwordRepeat or not companyPhone or not website:
            message = 'Please fill out the required fields!'
        elif accountExistWithSameEmail:
            message = 'There is already a company with that email!'
        elif accountExistWithSameName:
            message = 'There is already a company with this Name!'
        elif accountExistWithSamePhone:
            message = 'There is already a company with this phone number!'
        elif accountExistWithSameWebsite:
            message = 'There is already a company with this website!'
        elif password != passwordRepeat:
            message = 'Password mismatch. Please enter same password!'   
        else:
            cursor.execute('INSERT INTO User (id, email, password, phone, active) VALUES (NULL, % s, % s, % s, TRUE)', (companyEmail, password, companyPhone, ))
            mysql.connection.commit()
            # find newly added traveler
            cursor.execute('SELECT * FROM User WHERE email = %s ', (companyEmail, ))
            newUser = cursor.fetchone()
            # get the user id and insert this user into Traveler
            newCompanyId = newUser['id']
            cursor.execute('INSERT INTO Company (id,  company_name, website, foundation_date, about, validator_id, validation_date) VALUES (%s, % s, % s, % s, %s, NULL, NULL)', (newCompanyId, companyName, website, foundationDate, aboutCompany, ))
            mysql.connection.commit()
            message = 'Comany successfully created! Please wait to be validated.'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('companyRegister.html', message = message)

@app.route('/logout', methods =['GET', 'POST'])
def logout():
    session.pop('userid', default=None)
    session.pop('loggedin', default=None)
    session.pop('userType', default=None)

    if 'userid' in session or 'userType' in session or 'loggedin' in session:
        logoutMessage = 'User cannot logged out successfully, try again'
        return render_template('main.html')
    
    logoutMessage = 'Successfully logged out!'
    return redirect(url_for('main'))

@app.route('/main', methods=['GET', 'POST'])
def main():
    #main displays findTravelPage wheter a user is logged in or not
    return findTravel()
 
@app.route('/travel/<string:vehicle_type>/from:<string:departure_city>/to:<string:arrival_city>/date:<string:departure_date>/extra_date:<string:extra_date>', methods=['GET'])
def travels(vehicle_type, departure_city, arrival_city, departure_date, extra_date):
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

    if extra_date == 'none':
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
        cursor.execute(query, (departure_city, arrival_city, departure_date, vehicle_type))
        searchedTravels = cursor.fetchall()
    else:
        query = """
        SELECT C.id AS company_id, C.company_name, T.travel_id, T.depart_time, T.arrive_time, T.price, T.business_price, Dep.name AS dep_terminal_name, Dep.city AS dep_city, Ar.name AS ar_terminal_name, Ar.city AS ar_city
        FROM Travel T
        JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
        JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
        JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
        JOIN Company C ON T.travel_company_id = C.id
        WHERE Dep.city = %s
        AND Ar.city = %s
        AND DATE(T.depart_time) <= %s
        AND DATE(T.depart_time) >= %s
        AND V.type = %s
        ORDER BY {}
        """.format(sort_type)
        cursor.execute(query, (departure_city, arrival_city, extra_date, departure_date, vehicle_type))
        searchedTravels = cursor.fetchall()


    is_logged_in = session.get('loggedin', False)       #retrieves the value of is_logged_in from the session, if it's not present in the session, the default value False is used.
    user_id = session.get('userid')

    cursor.close()

    return render_template('listAvailableTravelsPage.html', searchedTravels=searchedTravels, vehicleType=vehicle_type, arrivalCity=arrival_city, departureCity=departure_city, departureDate=departure_date, extra_date=extra_date, sortType=sort_in, is_logged_in=is_logged_in, user_id=user_id)

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

        extra_date = 'none'
        if 'extra_date' in request.form:
            extra_date = request.form['extra_date']

        #perform checks
        if not departure_city or not arrival_city or not departure_date:
            error_message = "Please select fill in the form."
            return render_template('main.html', cities=cities, is_logged_in=is_logged_in, user_id =user_id, error_message=error_message)

        #redirect to listAvailableTravelsPage.html with relevant information
        return redirect(url_for('travels', vehicle_type=vehicle_type, departure_city=departure_city, arrival_city=arrival_city, departure_date=departure_date, extra_date=extra_date))
        
    cursor.close()

    #main.html is the current design
    return render_template('main.html', cities=cities, is_logged_in=is_logged_in, user_id=user_id,)

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

    cursor.close()

    return render_template('myTravelsPage.html', user_travels=user_travels, user_id=user_id)

@app.route('/travel/buy/<int:travel_id>/', methods=['GET', 'POST'])
def buy_travel(travel_id):
    user_id = session.get('userid')
    is_logged_in = session.get('loggedin', False)
    selected_coupon_id = None

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Get travel details
    query_travel = """
    SELECT c.company_name, dep.name AS departure_terminal, arr.name AS arrival_terminal, t.depart_time, t.price
    FROM Travel t
    JOIN Company c ON t.travel_company_id = c.id
    JOIN Terminal dep ON t.departure_terminal_id = dep.terminal_id
    JOIN Terminal arr ON t.arrival_terminal_id = arr.terminal_id
    WHERE t.travel_id = %s;
    """
    cursor.execute(query_travel, (travel_id,))
    travel_details = cursor.fetchone()

    # Get balance
    query_balance = """
    SELECT balance
    FROM Traveler
    WHERE Traveler.id = %s
    """
    cursor.execute(query_balance, (user_id,))
    balance = cursor.fetchone()

    # Get coupons
    query_coupons = """
    SELECT SC.coupon_name, SC.sale_rate, SC.coupon_id
    FROM Sale_Coupon SC
    INNER JOIN Coupon_Traveler CT ON SC.coupon_id = CT.coupon_id
    WHERE CT.user_id = %s AND CT.used_status = FALSE
    """
    cursor.execute(query_coupons, (user_id,))
    coupons = cursor.fetchall()

    pnr = generatePNR()
    seat_number = generateSeatNumber(travel_id)

    if request.method == 'POST':
        coupon_id = request.form.get('coupon_id')
        if coupon_id:
            selected_coupon_id = int(coupon_id)
            # Fetch the coupon details based on the coupon ID
            query_coupon = """
            SELECT sale_rate
            FROM Sale_Coupon
            WHERE coupon_id = %s
            """
            cursor.execute(query_coupon, (coupon_id,))
            coupon = cursor.fetchone()
            sale_rate = coupon['sale_rate']
            
            # Calculate the discounted price
            discounted_price = travel_details['price'] * (1 - sale_rate)
            
            # Update the travel_details dictionary with the discounted price
            travel_details['discounted_price'] = '{0:.5}'.format(discounted_price)
        else:
            travel_details['discounted_price'] = travel_details['price']

    return render_template('purchasePage.html', travel_id=travel_id, travel_details=travel_details, balance=balance, coupons=coupons, pnr=pnr, seat_number=seat_number, is_logged_in=is_logged_in, user_id=user_id, selected_coupon_id=selected_coupon_id)

@app.route('/coupons', methods=['GET', 'POST'])
def coupons():
    user_id = session['userid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Retrieve available coupons for the user
    query_available = """
    SELECT SC.coupon_name, SC.sale_rate
    FROM Sale_Coupon SC
    INNER JOIN Coupon_Traveler CT ON SC.coupon_id = CT.coupon_id
    WHERE CT.user_id = %s AND CT.used_status = FALSE
    """
    cursor.execute(query_available, (user_id,))
    available_coupons = cursor.fetchall()

    # Retrieve past coupons for the user
    query_past = """
    SELECT SC.coupon_name, SC.sale_rate
    FROM Sale_Coupon SC
    INNER JOIN Coupon_Traveler CT ON SC.coupon_id = CT.coupon_id
    WHERE CT.user_id = %s AND CT.used_status = TRUE
    """
    cursor.execute(query_past, (user_id,))
    past_coupons = cursor.fetchall()

    # Insert new coupon for the user
    if request.method == 'POST':
        # Get the coupon number entered by the user
        coupon_number = request.form['coupon_number']

        # Check if the coupon exists in the Sale_Coupon table
        query_check_coupon = "SELECT coupon_id FROM Sale_Coupon WHERE coupon_id = %s"
        cursor.execute(query_check_coupon, (coupon_number,))
        coupon = cursor.fetchone()

        if coupon:
            # Check if the coupon is already associated with the user
            query_check_exists = "SELECT coupon_id FROM Coupon_Traveler WHERE coupon_id = %s AND user_id = %s"
            cursor.execute(query_check_exists, (coupon_number, user_id))
            existing_coupon = cursor.fetchone()

            if existing_coupon:
                # Display an error message if the coupon is already associated with the user
                flash("Coupon already associated with your account.", "error")
            else:
                # Insert the coupon into the Coupon_Traveler table for the user
                query_insert_coupon = "INSERT INTO Coupon_Traveler (coupon_id, user_id) VALUES (%s, %s)"
                cursor.execute(query_insert_coupon, (coupon_number, user_id))
                mysql.connection.commit()

                # Redirect to the same page to display the updated list of available coupons
                return redirect(url_for('coupons', user_id=user_id))
        else:
            # Display an error message if the coupon does not exist
            flash("Invalid coupon number.", "error")

    return render_template('couponsPage.html', user_id=user_id, available_coupons=available_coupons, past_coupons=past_coupons)

@app.route('/userProfile', methods=['GET', 'POST'])
def userProfile(): 
    if 'userid' in session and 'loggedin' in session:
        user_id = session['userid']
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
    
@app.route('/updateTravelerProfile/', methods=['GET', 'POST'])
def updateTravelerProfile():
    if 'userid' in session and 'loggedin' in session:
        user_id = session['userid']
        if request.method == 'POST':
            # Get user information
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = """
            SELECT id, email, phone, TCK, name, surname, age, balance
            FROM User U NATURAL JOIN Traveler T
            WHERE U.id = %s AND U.active = TRUE
            """
            cursor.execute(query, (user_id,))
            userCurrentInfo = cursor.fetchone()

            newEmail = request.form['email'] 
            newPhone = request.form['phone'] 
            newName = request.form['name'] 
            newSurname = request.form['surname']
            newAge = request.form['age']
            # newEmail = request.form['email'] if 'email' in request.form else userCurrentInfo['email']
            # newPhone = request.form['phone'] if 'phone' in request.form else userCurrentInfo['phone']
            # newName = request.form['name'] if 'name' in request.form else userCurrentInfo['name']
            # newSurname = request.form['surname'] if 'surname' in request.form else userCurrentInfo['surname']
            # newAge = request.form['age']
            # newAge = int(newAge) if newAge else userCurrentInfo['age']

            if (userCurrentInfo['email'] != newEmail or userCurrentInfo['phone'] != newPhone):
                updateQuery = "UPDATE User SET email = %s, phone = %s WHERE id = %s"
                cursor.execute(updateQuery, (newEmail, newPhone, user_id,))

            if (userCurrentInfo['name'] != newName or userCurrentInfo['surname'] != newSurname or userCurrentInfo['age'] != newAge):
                updateQuery = "UPDATE Traveler SET name = %s, surname = %s, age = %s WHERE id = %s"
                cursor.execute(updateQuery, (newName, newSurname, newAge, user_id,))

            # Commit the changes to the database
            mysql.connection.commit()

            return redirect(url_for('userProfile', user_id=user_id))
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message=message)
    
@app.route('/balance', methods = [ 'GET', 'POST'])
def balance():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if 'userid' in session and 'loggedin' in session:
        user_id = session['userid']

        # Get balance
        query_balance = """
        SELECT balance
        FROM Traveler
        WHERE Traveler.id = %s
        """
        cursor.execute(query_balance, (user_id,))
        balance = cursor.fetchone()

        # Send amount to balance
        if request.method == 'POST':
            amount = request.form.get('amount')
            balance['balance'] += int(amount)

            query_newbalance = """
            UPDATE Traveler 
            SET balance = %s
            WHERE Traveler.id = %s
            """
            cursor.execute(query_newbalance, (balance['balance'], user_id))
            mysql.connection.commit()

            return redirect(url_for('balance'))
        
        return render_template('balancePage.html', user_id = user_id, balance=balance)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)

##############################
### COMPANY RELATED ROUTES ###
##############################

@app.route('/companysAllTravels/<string:upcomingOrPast>', methods = ['GET', 'POST'])
def companysAllTravels(upcomingOrPast):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        userid = session['userid']
        if upcomingOrPast == 'upcoming':
            #get upcoming travels belongs to this company and list
            query = """
            SELECT *
            FROM Company C 
            JOIN Travel T ON C.id = T.travel_company_id
            JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
            JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
            JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
            WHERE  C.id = %s AND T.depart_time > %s
            """
            cursor.execute(query, (userid, datetime.now()))
            travelDetailList = cursor.fetchall()
        elif upcomingOrPast == 'past':
            #get past travels belongs to the company and list
            query = """
            SELECT *
            FROM Company C 
            JOIN Travel T ON C.id = T.travel_company_id
            JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
            JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
            JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
            WHERE  C.id = %s AND T.depart_time < %s
            """
            cursor.execute(query, (userid, datetime.now()))
            travelDetailList = cursor.fetchall()
        
        cursor.close()
        return render_template('companysAllTravels.html', travelDetailList = travelDetailList, upcomingOrPast = upcomingOrPast )
    else:
        message = 'session is not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/addCompanyTravel/<string:travelVehicleType>', methods = ['GET', 'POST'])
def addCompanyTravel(travelVehicleType):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        companyId = session['userid']
        message = ''

        # get available terminals depending on the vehicle type
        queryAllAvailableTerminals = """
        SELECT *
        FROM Terminal
        WHERE active_status = 'active'AND type = %s
        ORDER BY city, name
        """
        cursor.execute(queryAllAvailableTerminals, (travelVehicleType,))
        allAvailableTerminals = cursor.fetchall()

        #get all vehicle models and models depending on type
        queryAllAvailableVehicleTypes = """
        SELECT *
        FROM Vehicle_Type
        WHERE type = %s
        ORDER BY model
        """
        cursor.execute(queryAllAvailableVehicleTypes, (travelVehicleType, ))
        allAvailableVehicleTypes = cursor.fetchall()

        if request.method == 'POST':
            # get values from the request form
            dep_terminal_id = request.form['dep_terminal_id']
            ar_terminal_id = request.form['ar_terminal_id']
            dep_time = request.form['dep_time']
            ar_time = request.form['ar_time']
            vehic_type_id = request.form['vehic_type_id']
            price = request.form['price']
            business_price = request.form['business_price']
            
            # dep_time_converted = datetime.strptime(dep_time, '%Y-%m-%d %H:%M:%S')
            if not dep_terminal_id or not ar_terminal_id or not dep_time or not ar_time or not vehic_type_id or not price:
                message = 'Please fill the form!'
            elif( dep_time < str(datetime.now()) ):
                message = "You cannot create a travel with a date of departure in the past!"
            elif( ar_time < dep_time ):
                message = "You cannot create a travel whose arrival time is smaller then departure time!"
            else:
                queryAddTravel = """
                INSERT INTO Travel (travel_id, travel_company_id, departure_terminal_id, arrival_terminal_id, depart_time, arrive_time, price, business_price, vehicle_type_id)
                VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(queryAddTravel, (companyId, dep_terminal_id, ar_terminal_id, dep_time, ar_time, price, business_price, vehic_type_id))
                # Commit the changes to the database
                mysql.connection.commit()
                message = 'Travel is added!'
            

        cursor.close()
        return render_template('addCompanyTravel.html', allAvailableTerminals = allAvailableTerminals, allAvailableVehicleTypes = allAvailableVehicleTypes, travelVehicleType = travelVehicleType, message = message  )
    else:
        message = 'session is not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/aTravelDetails/<int:travelId>', methods = [ 'GET', 'POST'])
def aTravelDetails(travelId):
        if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            companyId = session['userid']
            aTravelReservationDetails = None   

            #get travel information
            queryGetTravelInfo = """
            SELECT *
            FROM Travel T
            JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
            JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
            JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
            WHERE T.travel_id = %s
            """
            cursor.execute(queryGetTravelInfo, (travelId, ))
            theTravel = cursor.fetchone()

            if( theTravel['travel_company_id'] != companyId ):
                message= "This travel doesn't belongs to this company. Access Denied!"
            else:
                #get details of purchase, person who purchase this travel etc.
                queryATravelPurchaseDetails= """
                SELECT
                Booking.PNR,
                Booking.seat_number,
                Booking.seat_type,
                Purchased.purchased_time,
                Purchased.payment_method,
                Purchased.price AS amount,
                Sale_Coupon.coupon_name,
                Sale_Coupon.sale_rate,
                Traveler.TCK,
                Traveler.name,
                Traveler.surname
                FROM
                Travel
                JOIN Booking ON Booking.travel_id = Travel.travel_id
                JOIN Traveler ON Traveler.id = Booking.traveler_id
                JOIN Purchased ON Purchased.PNR = Booking.PNR
                LEFT JOIN Sale_Coupon ON Sale_Coupon.coupon_id = Purchased.coupon_id
                WHERE
                Travel.travel_id = %s
                """
                cursor.execute(queryATravelPurchaseDetails, (travelId,))
                aTravelPurchaseDetails = cursor.fetchall()

                # Get details of reservations, person who reserved this travel etc.
                # If a travel is past, no need to get the reservations 
                if (theTravel['depart_time'] > datetime.now()):
                    queryATravelReservationDetails= """
                    SELECT
                    Booking.PNR,
                    Booking.seat_number,
                    Booking.seat_type,
                    Reserved.reserved_time,
                    Reserved.purchased_deadline,
                    Traveler.TCK,
                    Traveler.name,
                    Traveler.surname
                    FROM
                    Travel
                    JOIN Booking ON Booking.travel_id = Travel.travel_id
                    JOIN Traveler ON Traveler.id = Booking.traveler_id
                    JOIN Reserved ON Reserved.PNR = Booking.PNR
                    WHERE
                    Travel.travel_id = %s
                    """
                    cursor.execute(queryATravelReservationDetails, (travelId,))
                    aTravelReservationDetails = cursor.fetchall()

            cursor.close()
            current_time = datetime.now()
            return render_template('aTravelDetails.html', theTravel = theTravel, current_time = current_time, aTravelPurchaseDetails = aTravelPurchaseDetails, aTravelReservationDetails = aTravelReservationDetails) 
        else:
            message = 'Session is not valid, please log in!'
            return render_template('login.html', message = message)
        
@app.route('/commentsOnATravel/<int:travelId>', methods = ['GET', 'POST'])
def commentsOnATravel(travelId):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        companyId = session['userid']

        #get travel information
        queryGetTravelInfo = """
        SELECT *
        FROM Travel T
        JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
        JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
        JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
        WHERE T.travel_id = %s
        """
        cursor.execute(queryGetTravelInfo, (travelId, ))
        theTravel = cursor.fetchone()

        if( theTravel['travel_company_id'] != companyId ):
            message= "This travel doesn't belongs to this company. Access Denied!"
        else:
            a = 1
            # Get comments on the travel and information about comment writers
            # Select statement in the query is written such that 
            # TCK, age and balance of the travelers are not obtained for privalage
            queryGetComment = """
            SELECT R.travel_id, R.traveler_id, R.comment, R.rating, T.name, T.surname
            FROM Review R
            JOIN Traveler T ON T.id = R.traveler_id
            WHERE R.travel_id = %s
            """
            cursor.execute(queryGetComment, (travelId,))
            allComments = cursor.fetchall()

        return render_template('commentsOnATravel.html', theTravel = theTravel, allComments = allComments)
    else:
        message = 'Session is not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/editUpcomingTravel/<int:travelId>', methods = [ 'GET', 'POST'])
def editUpcomingTravel(travelId):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        companyId = session['userid']
        isEditable = True
        message = ''

        queryGetTravelInfo = """
        SELECT *
        FROM Travel T
        JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
        JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
        JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
        WHERE T.travel_id = %s
        """
        cursor.execute(queryGetTravelInfo, (travelId, ))
        theTravel = cursor.fetchone()
        
        # Check if the travel is of the logged in company
        if( theTravel['travel_company_id'] != companyId):
            message = "This travel doesn't belong to your company. You cannot edit!"
            isEditable = False
            return render_template('editUpcomingTravel.html', isEditable = isEditable, message = message, theTravel = theTravel) 
        elif( theTravel['depart_time'] < datetime.now()): # check if the travel is past travel
            message = "This travel has been made. You cannot edit past travels!"
            isEditable = False
            return render_template('editUpcomingTravel.html', isEditable = isEditable, message = message, theTravel = theTravel) 
        else:
            isEditable = True

            travelVehicleType = theTravel['type'] # get the vehicle type such as plane, bus or train
            # get available terminals depending on the vehicle type
            queryAllAvailableTerminals = """
            SELECT *
            FROM Terminal
            WHERE active_status = 'active'AND type = %s
            ORDER BY city, name
            """
            cursor.execute(queryAllAvailableTerminals, (travelVehicleType,))
            allAvailableTerminals = cursor.fetchall()

            #get all vehicle models and models depending on type
            queryAllAvailableVehicleTypes = """
            SELECT *
            FROM Vehicle_Type
            WHERE type = %s
            ORDER BY model
            """
            cursor.execute(queryAllAvailableVehicleTypes, (travelVehicleType, ))
            allAvailableVehicleTypes = cursor.fetchall()
        
            # Get the information from the form 
            # Update the travel information
            if request.method == 'POST':
                # get values from the request form
                dep_terminal_id = request.form['dep_terminal_id']
                ar_terminal_id = request.form['ar_terminal_id']
                dep_time = request.form['dep_time']
                ar_time = request.form['ar_time']
                vehic_type_id = request.form['vehic_type_id']
                price = request.form['price']
                business_price = request.form['business_price']
                
                # dep_time_converted = datetime.strptime(dep_time, '%Y-%m-%d %H:%M:%S')
                if not dep_terminal_id or not ar_terminal_id or not dep_time or not ar_time or not vehic_type_id or not price:
                    message = 'Please fill the form!'
                elif( dep_time < str(datetime.now()) ):
                    message = "You cannot edit travel so that departure time is before now!"
                elif( ar_time < dep_time ):
                    message = "You cannot edit travel so that arrival time is before the departure time!"
                else:
                    queryUpdateTravel = """
                    UPDATE Travel
                    SET
                    departure_terminal_id = %s,
                    arrival_terminal_id = %s,
                    depart_time = %s,
                    arrive_time = %s,
                    price = %s,
                    business_price = %s, 
                    vehicle_type_id = %s
                    WHERE travel_id = %s AND travel_company_id = %s
                    """
                    cursor.execute(queryUpdateTravel, ( dep_terminal_id, ar_terminal_id, dep_time, ar_time, price, business_price, vehic_type_id, travelId, companyId,))
                    # Commit the changes to the database
                    mysql.connection.commit()
                    message = 'Travel is successfully updated!' 
                    # Get updated travel
                    cursor.execute(queryGetTravelInfo, (travelId, ))
                    theTravel = cursor.fetchone()

        return render_template('editUpcomingTravel.html', message = message, isEditable = isEditable, theTravel = theTravel, allAvailableTerminals = allAvailableTerminals, allAvailableVehicleTypes = allAvailableVehicleTypes ) 
    else:
        message = 'Session is not valid, please log in!'
        return render_template('login.html', message = message)
    

@app.route('/deleteATravel/<int:travelId>', methods = ['GET', 'POST'])
def deleteATravel(travelId):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        companyId = session['userid']
        message = ''

        queryGetTravelInfo = """
        SELECT *
        FROM Travel T
        JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
        JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
        JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
        WHERE T.travel_id = %s
        """
        cursor.execute(queryGetTravelInfo, (travelId, ))
        theTravel = cursor.fetchone()
        
        # Check if the travel is of the logged in company
        if( theTravel['travel_company_id'] != companyId):
            message = "This travel doesn't belong to your company. You cannot delete!"
        else:
            queryDeleteATravel = """
            DELETE FROM Travel WHERE travel_id = %s
            """
            cursor.execute(queryDeleteATravel, (travelId,))
            mysql.connection.commit()
            message = "The travel is deleted successfully!"

        flash(message)
        return redirect(url_for('companysAllTravels', upcomingOrPast = 'upcoming'))
    else:
        message = 'Session is not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/companyProfile/<int:companyId>', methods=['GET', 'POST'])
def companyProfile(companyId): 
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        #get user information
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
        SELECT id, email, phone, company_name, website, foundation_date, about
        FROM User U NATURAL JOIN Company C
        WHERE U.id = %s AND U.active = TRUE
        """
        cursor.execute(query, (companyId,))
        companyInfo = cursor.fetchone()
        return render_template('companyProfile.html', companyInfo = companyInfo)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/editCompanyProfile/<int:companyId>', methods=['GET', 'POST'])
def editCompanyProfile(companyId):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        if request.method == 'POST':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Get company information
            queryGetCompany = """
            SELECT id, email, phone, company_name, website, foundation_date, about
            FROM User U NATURAL JOIN Company C
            WHERE C.id = %s AND U.active = TRUE
            """
            cursor.execute(queryGetCompany, (companyId,))
            companyCurrentInfo = cursor.fetchone()

            newPhone = request.form['phone'] 
            newEmail = request.form['email']
            newName = request.form['companyName'] 
            newWebsite = request.form['website'] 
            newFoundationDate = request.form['foundationDate']
            newAbout = request.form['aboutCompany']

            if (companyCurrentInfo['email'] != newEmail or companyCurrentInfo['phone'] != newPhone):
                updateQuery = "UPDATE User SET email = %s, phone = %s WHERE id = %s"
                cursor.execute(updateQuery, (newEmail, newPhone, companyId,))

            if (companyCurrentInfo['company_name'] != newName or companyCurrentInfo['website'] != newWebsite or companyCurrentInfo['foundation_date'] != newFoundationDate or companyCurrentInfo['about'] != newAbout ):
                updateQuery = "UPDATE Company SET company_name = %s, website = %s, foundation_date = %s, about = %s WHERE id = %s"
                cursor.execute(updateQuery, (newName, newWebsite, newFoundationDate, newAbout, companyId,))

            # Commit the changes to the database
            mysql.connection.commit()
            message = 'Company information updated successfully!'
            cursor.execute(queryGetCompany, (companyId,))
            companyCurrentInfo = cursor.fetchone()
            return render_template('companyProfile.html', message = message, companyInfo = companyCurrentInfo )

        return companyProfile(companyId)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)
    
########################
### HELPER FUNCTIONS ###
########################

def generatePNR():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    while(True):
        length = PNR_LENGTH
        chars = string.ascii_uppercase + string.digits
        pnr = ''.join(random.choice(chars) for _ in range(length))

        # Check if pnr unique
        query_pnr_check = """
        SELECT COUNT(*) AS count
        FROM Booking 
        WHERE PNR = %s
        """
        cursor.execute(query_pnr_check, (pnr,))
        result = cursor.fetchone()

        if(result['count'] == 0):
            break
    
    return pnr

def generateSeatNumber(travel_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    query_seats = """
    SELECT num_of_seats, vehicle_type_id 
    FROM Travel 
    JOIN Vehicle_Type ON Travel.vehicle_type_id = Vehicle_Type.id 
    WHERE travel_id = %s
    """
    cursor.execute(query_seats, (travel_id,))
    result = cursor.fetchone()

    total_seats = result['num_of_seats']

    # Count the number of bookings made for the given travel
    query_num_bookings = """
    SELECT COUNT(*) 
    FROM Booking 
    WHERE travel_id = %s
    """
    cursor.execute(query_num_bookings, (travel_id,))
    booked_seats = cursor.fetchall()[0]

    # Generate random valid seat number
    while(True):
        seat_number = random.randint(1, total_seats)

        # Check if the randomly generated seat number is already booked
        query_check_seat = """
        SELECT COUNT(*) AS occupied
        FROM Booking 
        WHERE travel_id = %s AND seat_number = %s
        """
        cursor.execute(query_check_seat, (travel_id, seat_number))
        result = cursor.fetchone()
        seat = result['occupied']

        if(seat == 0):
            break

    return seat_number

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
