
import re  
import os
import random, string
from datetime import datetime, timedelta
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

        if user:
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
            session['loggedin'] = True
            session['userid'] = user['id']
            session['userType'] = userType
            #message = 'Logged in successfully!'
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
            message = 'To register, you should be older than 18!'   
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
        SELECT C.id AS company_id, C.company_name, T.travel_id, T.depart_time, T.arrive_time, T.vehicle_type_id, T.price, T.business_price, Dep.name AS dep_terminal_name, Dep.city AS dep_city, Ar.name AS ar_terminal_name, Ar.city AS ar_city
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
        SELECT C.id AS company_id, C.company_name, T.travel_id, T.depart_time, T.arrive_time, T.vehicle_type_id, T.price, T.business_price, Dep.name AS dep_terminal_name, Dep.city AS dep_city, Ar.name AS ar_terminal_name, Ar.city AS ar_city
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

    updatedTravels = []  # Updated list of travels with available seats

    for travel in searchedTravels:
        travel_id = travel['travel_id']
        vehicle_type = travel['vehicle_type_id']

        # Count the number of booked seats for the travel
        booking_query = """
        SELECT COUNT(*) AS booked_seats 
        FROM Booking 
        WHERE travel_id = %s
        """
        cursor.execute(booking_query, (travel_id,))
        booked_seats = cursor.fetchone()['booked_seats']

        # Get the total number of seats available for the vehicle type
        seats_query = """
        SELECT num_of_seats 
        FROM Vehicle_Type 
        WHERE id = %s
        """
        cursor.execute(seats_query, (vehicle_type,))
        total_seats = cursor.fetchone()['num_of_seats']

        # Check if there are available seats
        if booked_seats < total_seats:
            updatedTravels.append(travel)

    searchedTravels = updatedTravels

    is_logged_in = session.get('loggedin', False)       #retrieves the value of is_logged_in from the session, if it's not present in the session, the default value False is used.
    user_id = session.get('userid')

    travel_seat = None
    if request.method == 'GET' and 'travel_seat' in request.args:
        travel_seat = int(request.args.get('travel_seat'))

        query = """
                SELECT seat_formation, num_of_seats 
                FROM Travel T
                JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
                WHERE T.travel_id = %s
                """
        cursor.execute(query, (travel_seat, ))
        seating_info = cursor.fetchone()

        query = """
                SELECT seat_number 
                FROM Booking 
                WHERE travel_id = %s
                """
        cursor.execute(query, (travel_seat, ))
        occupied = [x['seat_number'] for x in cursor.fetchall()]

        formation = [int(x) for x in seating_info['seat_formation'].split("-")]
        col = sum(formation)
        row = int(seating_info['num_of_seats']/col)

        return render_template('listAvailableTravelsPage.html', travel_seat=travel_seat,
                               searchedTravels=searchedTravels, vehicleType=vehicle_type, arrivalCity=arrival_city,
                               departureCity=departure_city, departureDate=departure_date, extra_date=extra_date,
                               sortType=sort_in, is_logged_in=is_logged_in, user_id=user_id, formation=formation, row=row, tot_col=col, occupied=occupied)

    cursor.close()


    return render_template('listAvailableTravelsPage.html', travel_seat=travel_seat, searchedTravels=searchedTravels, vehicleType=vehicle_type, arrivalCity=arrival_city, departureCity=departure_city, departureDate=departure_date, extra_date=extra_date, sortType=sort_in, is_logged_in=is_logged_in, user_id=user_id)

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
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'traveler':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user_id = session.get('userid')

        commentAreaOnAPNR = None
        if request.method == 'GET' and 'commentAreaOnAPNR' in request.args:
            commentAreaOnAPNR = request.args.get('commentAreaOnAPNR')


        upcomingOrPast = 'upcoming'
        if request.method == 'GET' and 'upcomingOrPast' in request.args:
            upcomingOrPast = request.args.get('upcomingOrPast')

        # Fetch all terminals
        cursor.execute("SELECT terminal_id, city FROM Terminal")
        terminals = cursor.fetchall()

        # Fetch the list of vehicle types
        cursor.execute("SELECT id, type FROM Vehicle_Type")
        vehicles = cursor.fetchall()

        # Filter and remove duplicates from terminals
        departure_terminals = []
        arrival_terminals = []
        for terminal in terminals:
            if terminal['city'] not in [t['city'] for t in departure_terminals]:
                departure_terminals.append(terminal)
            if terminal['city'] not in [t['city'] for t in arrival_terminals]:
                arrival_terminals.append(terminal)

        # Filter and remove duplicates from vehicle types
        vehicle_types = []
        for vehicle_type in vehicles:
            if vehicle_type['type'] not in [v['type'] for v in vehicle_types]:
                vehicle_types.append(vehicle_type)

        # Retrieve filter values from the request arguments
        if request.method == 'GET':
            travel_date = request.args.get('travelDate')
            departure_terminal = request.args.get('departureTerminal')
            arrival_terminal = request.args.get('arrivalTerminal')
            travel_type = request.args.get('travelType')

        # Initialize the WHERE clause of the query
        where_clause = 'WHERE Booking.traveler_id = %s'
        query_params = [user_id]

        # Add conditions to the WHERE clause based on the filter values
        if travel_date:
            where_clause += ' AND DATE(Travel.depart_time) = %s'
            query_params.append(travel_date)
        if departure_terminal:
            where_clause += ' AND Travel.departure_terminal_id = %s'
            query_params.append(departure_terminal)
        if arrival_terminal:
            where_clause += ' AND Travel.arrival_terminal_id = %s'
            query_params.append(arrival_terminal)
        if travel_type:
            where_clause += ' AND Travel.vehicle_type_id = %s'
            query_params.append(travel_type)

        query = """
        SELECT Travel.travel_id, Booking.PNR, Booking.seat_number, Travel.depart_time, Terminal.name AS departure_terminal_name, Terminal2.name AS arrival_terminal_name, Company.company_name
        FROM Booking
        JOIN Travel ON Booking.travel_id = Travel.travel_id
        JOIN Terminal ON Travel.departure_terminal_id = Terminal.terminal_id
        JOIN Terminal AS Terminal2 ON Travel.arrival_terminal_id = Terminal2.terminal_id
        JOIN Company ON Travel.travel_company_id = Company.id
        {}
        AND Travel.depart_time {} %s
        ORDER BY Travel.depart_time {}
        """

        if upcomingOrPast == 'past':
            comparison_operator = '<'
            order_by = 'DESC'
        else:
            comparison_operator = '>'
            order_by = 'ASC'

        formatted_query = query.format(where_clause, comparison_operator, order_by)
        cursor.execute(formatted_query, tuple(query_params + [datetime.now()]))
        user_travels = cursor.fetchall()

        currentRating = '1'
        if request.method == 'GET' and 'rating' in request.args:
            currentRating = request.args.get('rating')

        query_reserved = """
        SELECT Reserved.PNR
        FROM Reserved
        JOIN Booking ON Reserved.PNR = Booking.PNR
        WHERE Booking.traveler_id = %s
        AND Reserved.PNR = Booking.PNR
        """
        cursor.execute(query_reserved, (user_id,))
        reserved_travels = [row['PNR'] for row in cursor.fetchall()]

        for row in user_travels:
            if row['PNR'] in reserved_travels:
                row['reserved'] = True

        cursor.close()

        return render_template('myTravelsPage.html', user_travels=user_travels, user_id=user_id, upcomingOrPast = upcomingOrPast, commentAreaOnAPNR = commentAreaOnAPNR, currentRating = currentRating, reserved_travels=reserved_travels, departure_terminals=departure_terminals, arrival_terminals=arrival_terminals, vehicle_types=vehicle_types)
    else:
        message = 'session is not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/makeComment/<int:travel_id>', methods = ['GET', 'POST'])
def makeComment(travel_id):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'traveler':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user_id = session.get('userid')
        message = ""

        if request.method == 'POST':
            if 'comment' in request.form and 'rating' in request.form:
                # get comment and rating from the request form
                comment = request.form['comment']
                rating = request.form['rating']

                queryMakeComment = """
                INSERT INTO Review ( travel_id, traveler_id, comment, rating) VALUES (%s, % s, % s, % s)
                """
                cursor.execute(queryMakeComment, (travel_id, user_id, comment, rating))
                mysql.connection.commit()
                message = "Comment successfully made! "
            else:
                message = "Please fill the form!"

        flash(message)
        return redirect(url_for('myTravels'))
    else:
        message = 'session is not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/travel/buy/<int:travel_id>/', methods=['GET', 'POST'])
def buy_travel(travel_id):
    user_id = session.get('userid')
    is_logged_in = session.get('loggedin', False)
    selected_coupon_id = None

    pnr = generatePNR()
    seat_number = generateSeatNumber(travel_id)
    seat_chosen = False
    reserved_booking = None

    if request.method == "POST" and 'seat_number' in request.form:
        if request.form['seat_number']:
            seat_number = request.form['seat_number']
            seat_chosen = True

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST" and 'reserve_PNR' in request.form:
        pnr = request.form['reserve_PNR']

        query_reserved_booking = """
        SELECT *
        FROM Booking
        WHERE PNR = %s
        """
        cursor.execute(query_reserved_booking, (pnr, ))
        reserved_booking = cursor.fetchone()

        seat_number = reserved_booking['seat_number']
        seat_chosen = True

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

    # Get list of all journeys
    query_journey = """
    SELECT *
    FROM Journey J
    WHERE J.traveler_id = %s
    """
    cursor.execute(query_journey, (user_id,))
    journeys = cursor.fetchall()

    # Check if travel is associated with a journey
    query_check_journey = """
    SELECT COUNT(*) AS cnt
    FROM Travels_In_Journey 
    WHERE travel_id = %s;
    """
    cursor.execute(query_check_journey, (travel_id,))
    journey_count = cursor.fetchone()['cnt']

    query_journey_name = """
    SELECT journey_name
    FROM Travels_In_Journey 
    WHERE travel_id = %s;
    """
    cursor.execute(query_journey_name, (travel_id,))
    journey = cursor.fetchone()

    journey_name = None
    if journey:
        journey_name = journey['journey_name']

    if request.method == 'POST' and "addTravelToJourney" in request.form:
        selected_journey = request.form['selectedJourney']
        query_addTravelToJourney = """
        INSERT INTO Travels_In_Journey VALUES
        (%s, %s, %s)
        """
        cursor.execute(query_addTravelToJourney, (selected_journey, user_id, travel_id,))
        mysql.connection.commit()
        return redirect(url_for('journeys'))

    # apply coupon
    if request.method == 'POST':
        coupon_id = request.form.get('coupon_id', type=int)
        if coupon_id:
            selected_coupon_id = coupon_id
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
            selected_coupon_id = None
            travel_details['discounted_price'] = travel_details['price']

    # reserve
    if request.method == 'POST' and "reserve" in request.form:
        ## do not deduct from balance
        # Generate the current timestamp
        reserved_time = datetime.now()

        # Calculate the purchase deadline (2 days before departure time)
        depart_time = travel_details['depart_time']
        purchase_deadline = depart_time - timedelta(days=2)
        
        query_insert_booking = """
        INSERT INTO Booking(PNR, travel_id, seat_number, traveler_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_insert_booking, (pnr, travel_id, seat_number, user_id))

        # Insert data into Reserved table
        query_insert_reserved = """
        INSERT INTO Reserved(PNR, reserved_time, purchased_deadline)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query_insert_reserved, (pnr, reserved_time, purchase_deadline))
        mysql.connection.commit()

        return redirect(url_for('myTravels'))
    
    # purchase
    if request.method == 'POST' and "purchase" in request.form:
        # Generate the current timestamp
        purchase_time = datetime.now()

        # Check if a coupon is used
        coupon_id = request.form.get('coupon_id')

        # Calculate the price to be deducted from the balance
        if coupon_id:
            # Fetch the coupon details based on the coupon ID
            query_coupon = """
            SELECT sale_rate
            FROM Sale_Coupon
            WHERE coupon_id = %s
            """
            cursor.execute(query_coupon, (coupon_id,))
            coupon = cursor.fetchone()
            sale_rate = coupon['sale_rate']

            # Update the coupon to be used
            query_update_coupon = """
            UPDATE Coupon_Traveler
            SET used_status = %s
            WHERE coupon_id = %s 
            AND user_id = %s
            """
            cursor.execute(query_update_coupon, (True, coupon_id, user_id))
            mysql.connection.commit()

            # Calculate the discounted price
            discounted_price = travel_details['price'] * (1 - sale_rate)
        else:
            # No coupon applied, use the original price
            discounted_price = travel_details['price']

        # Calculate the updated balance
        updated_balance = balance['balance'] - discounted_price

        # Check if user has sufficient funds
        if updated_balance < 0:
            flash("Insuffiecient funds!", "error")
            return redirect(url_for('buy_travel', travel_id=travel_id))

        # If purchasing already booked (reserved) travel 
        if reserved_booking:
            query_insert_purchased = """
            INSERT INTO Purchased(PNR, purchased_time, payment_method, price, coupon_id)
            VALUES (%s, %s, %s, %s, %s) 
            """
            cursor.execute(query_insert_purchased, (pnr, purchase_time, 'credit card', discounted_price, coupon_id))

            query_delete_reserved = """
            DELETE FROM Reserved
            WHERE PNR = %s
            """
            cursor.execute(query_delete_reserved, (pnr,))

            query_update_balance = """
            UPDATE Traveler
            SET Balance = %s
            WHERE id = %s
            """
            cursor.execute(query_update_balance, (updated_balance, user_id))
            mysql.connection.commit()

        else:
            query_insert_booking = """
            INSERT INTO Booking(PNR, travel_id, seat_number, traveler_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_insert_booking, (pnr, travel_id, seat_number, user_id))

            query_insert_purchased = """
            INSERT INTO Purchased(PNR, purchased_time, payment_method, price, coupon_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert_purchased, (pnr, purchase_time, 'credit card', discounted_price, coupon_id))

            query_update_balance = """
            UPDATE Traveler
            SET Balance = %s
            WHERE id = %s
            """
            cursor.execute(query_update_balance, (updated_balance, user_id))
            mysql.connection.commit()

        return redirect(url_for('myTravels'))
    return render_template('purchasePage.html', travel_id=travel_id, travel_details=travel_details, reserved_booking=reserved_booking, balance=balance, coupons=coupons, pnr=pnr, seat_number=seat_number, seat_chosen=seat_chosen, is_logged_in=is_logged_in, user_id=user_id, selected_coupon_id=selected_coupon_id, journeys = journeys, journey_count=journey_count, journey_name=journey_name)

@app.route('/coupons', methods=['GET', 'POST'])
def coupons():
    user_id = session['userid']
    time_now = datetime.now().date()
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
        coupon_name = request.form['coupon_name']

        # Check if the coupon exists in the Sale_Coupon table
        query_check_coupon = """
        SELECT coupon_id, expiration_date, public_status 
        FROM Sale_Coupon 
        WHERE coupon_name = %s
        """
        cursor.execute(query_check_coupon, (coupon_name,))
        coupon = cursor.fetchone()

        if coupon:
            coupon_id = coupon['coupon_id']
            expiration_date = coupon['expiration_date']
            public_status = coupon['public_status']

            # Check if the coupon is already associated with the user
            query_check_exists = """
            SELECT coupon_id 
            FROM Coupon_Traveler 
            WHERE coupon_id = %s 
            AND user_id = %s
            """
            cursor.execute(query_check_exists, (coupon_id, user_id))
            existing_coupon = cursor.fetchone()

            if public_status == 'public' and not existing_coupon:
                # Insert the coupon into the Coupon_Traveler table for the user
                query_insert_coupon = "INSERT INTO Coupon_Traveler (coupon_id, user_id) VALUES (%s, %s)"
                cursor.execute(query_insert_coupon, (coupon_id, user_id))
                mysql.connection.commit()

                # Redirect to the same page to display the updated list of available coupons
                return redirect(url_for('coupons'))
            elif public_status == 'private':
                if existing_coupon:
                    # Display an error message if the coupon is already associated with the user
                    flash("Coupon already associated with your account.", "error")
                else:
                    # Insert the coupon into the Coupon_Traveler table for the user
                    query_insert_coupon = "INSERT INTO Coupon_Traveler (coupon_id, user_id) VALUES (%s, %s)"
                    cursor.execute(query_insert_coupon, (coupon_id, user_id))
                    mysql.connection.commit()

                    # Redirect to the same page to display the updated list of available coupons
                    return redirect(url_for('coupons'))
            else:
                # Display error message if the coupon is public and already associated with the user
                flash("Coupon is not available.", "error")
        else:
            # Display an error message if the coupon does not exist
            flash("Invalid coupon number.", "error")

    return render_template('couponsPage.html', available_coupons=available_coupons, past_coupons=past_coupons)

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

@app.route('/journeys', methods = [ 'GET', 'POST'])
def journeys():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if 'userid' in session and 'loggedin' in session:
        user_id = session['userid']

        # Get list of all journeys
        query_journey = """
        SELECT *
        FROM Journey J
        WHERE J.traveler_id = %s
        """
        cursor.execute(query_journey, (user_id,))
        journeys = cursor.fetchall()

        # Get list of all travels that are inside journeys
        query_travelInJourney = """
        SELECT *, T1.city as dep_city, T2.city as arr_city
        FROM Travels_In_Journey natural join Travel join Company on travel_company_id = id join Terminal T1 on departure_terminal_id = T1.terminal_id join Terminal T2 on arrival_terminal_id = T2.terminal_id
        WHERE traveler_id = %s
        """
        cursor.execute(query_travelInJourney, (user_id,))
        travelsInJourneys = cursor.fetchall()

        # Get journeys that are booked
        query_booked_journeys = """
        SELECT T.travel_id
        FROM Journey J
        INNER JOIN Travels_In_Journey T ON J.journey_name = T.journey_name
        INNER JOIN Booking B ON T.travel_id = B.travel_id
        WHERE J.traveler_id = %s
        """
        cursor.execute(query_booked_journeys, (user_id,))
        booked_journeys = cursor.fetchall()

        booked_journey_ids = [journey['travel_id'] for journey in booked_journeys]

        if request.method == 'POST':
            newJourneyName = request.form.get('journeyForm')
            createdTime = datetime.now()

            query_addNewJourney = """
            INSERT INTO Journey VALUES 
            (%s, %s, %s, "valid")
            """
            cursor.execute(query_addNewJourney, (newJourneyName, user_id, createdTime,))
            mysql.connection.commit()

            return redirect(url_for('journeys'))
        
        return render_template("journeysPage.html", journeys = journeys, travelsInJourneys = travelsInJourneys, booked_journey_ids=booked_journey_ids)
    else:
        message = "Session is not valid, please log in!"
        return render_template("login.html", message = message)

@app.route('/buy_all', methods=['POST'])
def buy_all():
    user_id = session.get('userid')
    action = request.form.get('action')
    journey_name = request.form['journey_name']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if action == 'buy':
        # Get all travel IDs associated with the user's journey
        query_travel_ids = """
        SELECT T.travel_id
        FROM Travels_In_Journey TIJ
        JOIN Travel T ON TIJ.travel_id = T.travel_id
        WHERE TIJ.traveler_id = %s
        AND TIJ.journey_name = %s
        """
        cursor.execute(query_travel_ids, (user_id, journey_name))
        travel_ids = [row['travel_id'] for row in cursor.fetchall()]

        # Get all travel ids of purchased travels
        query_purchased_ids = """
        SELECT DISTINCT B.travel_id
        FROM Booking B
        JOIN Purchased ON Purchased.PNR = B.PNR
        WHERE B.traveler_id = %s
        """
        cursor.execute(query_purchased_ids, (user_id,))
        purchased_ids = [row['travel_id'] for row in cursor.fetchall()]

        # Buy each travel
        for travel_id in travel_ids:
            if travel_id not in purchased_ids:
                buy_one(travel_id)

    elif action == 'reserve':
        # Get all travel IDs associated with the user's relevant journey
        query_travel_ids = """
        SELECT T.travel_id
        FROM Travels_In_Journey TIJ
        JOIN Travel T ON TIJ.travel_id = T.travel_id
        WHERE TIJ.traveler_id = %s
        AND TIJ.journey_name = %s
        """
        cursor.execute(query_travel_ids, (user_id, journey_name))
        travel_ids = [row['travel_id'] for row in cursor.fetchall()]

        # Get all travel ids of reserved travels
        query_purchased_ids = """
        SELECT DISTINCT B.travel_id
        FROM Booking B
        JOIN Reserved ON Rezerved.PNR = B.PNR
        WHERE B.traveler_id = %s
        """
        cursor.execute(query_purchased_ids, (user_id,))
        reserved_ids = [row['travel_id'] for row in cursor.fetchall()]

        # Reserve each travel
        for travel_id in travel_ids:
            if travel_id not in reserved_ids:
                reserve_one(travel_id)

    return redirect(url_for('journeys'))

##############################
### COMPANY RELATED ROUTES ###
##############################

@app.route('/companysAllTravels/<string:upcomingOrPast>', methods = ['GET', 'POST'])
def companysAllTravels(upcomingOrPast):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        userid = session['userid']
       
       
        sort_type = 'depart_time'
        sort_in = 'earliest_to_latest'

        if request.method == 'GET' and 'sort_type' in request.args:
            sort_in = request.args.get('sort_type')

            if sort_in == 'earliest_to_latest':
                sort_type = 'depart_time'
            elif sort_in == 'latest_to_earliest':
                sort_type = 'depart_time DESC'
            elif sort_in == 'low_to_high':
                sort_type = 'price'
            elif sort_in == 'high_to_low':
                sort_type = 'price DESC'

        if upcomingOrPast == 'upcoming':
            #get upcoming travels belongs to this company and list
            query = """
            SELECT *
            FROM companies_travels_detail_view
            WHERE  company_id = %s AND depart_time > %s
            ORDER BY {}
            """.format(sort_type)

            cursor.execute(query, (userid, datetime.now()))
            travelDetailList = cursor.fetchall()
        elif upcomingOrPast == 'past':
            #get past travels belongs to the company and list
            query = """
            SELECT *
            FROM companies_travels_detail_view
            WHERE company_id = %s AND depart_time < %s
            ORDER BY {}
            """.format(sort_type)
            cursor.execute(query, (userid, datetime.now()))
            travelDetailList = cursor.fetchall()
        
        cursor.close()
        return render_template('companysAllTravels.html', travelDetailList = travelDetailList, upcomingOrPast = upcomingOrPast, sort_type = sort_in )
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
            FROM travel_detail_view
            WHERE travel_id = %s
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
        FROM travel_detail_view
        WHERE travel_id = %s
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
        FROM travel_detail_view
        WHERE travel_id = %s
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

            travelVehicleType = theTravel['vehicle_type'] # get the vehicle type such as plane, bus or train
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
        message2 = None

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

        # Find if there is any booking (reservations and purchase) on the travel
        queryFindAnyBooking = """
        SELECT COUNT(*) AS booking_count
        FROM Booking 
        WHERE travel_id = %s
        """

        cursor.execute(queryFindAnyBooking, (travelId,))
        booking_count = cursor.fetchall()
        
        # Check if the travel is of the logged in company
        if( theTravel['travel_company_id'] != companyId):
            message = "This travel doesn't belong to your company. You cannot delete!"
        elif booking_count[0]['booking_count'] > 0:
            message = "There are " + str(booking_count[0]['booking_count']) 
            message = message + " bookings for this travel. To be able to delete this travel you need to delete these bookings first."
            message2 = "deleteTravelError"
        else:
            queryDeleteATravel = """
            DELETE FROM Travel WHERE travel_id = %s
            """
            cursor.execute(queryDeleteATravel, (travelId,))
            mysql.connection.commit()
            message = "The travel is deleted successfully."

        flash(message, message2)
        return redirect(url_for('companysAllTravels', upcomingOrPast = 'upcoming'))
    else:
        message = 'Session is not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/deleteAndRefundAPurchase/<string:PNRToBeDeleted>', methods=['GET', 'POST'])
def deleteAndRefundAPurchase(PNRToBeDeleted):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        companyId = session['userid']

        # Get user id, travel id and paid amount for the purchase
        queryGetInfo = """
        SELECT T.id AS traveler_id, B.travel_id AS travel_id, P.price AS paid_amount
        FROM Traveler T
        JOIN Booking B ON T.id = B.traveler_id
        JOIN Purchased P ON P.PNR = B.PNR
        WHERE B.PNR = %s
        """
        cursor.execute(queryGetInfo, (PNRToBeDeleted,))
        info = cursor.fetchone()

        # Check if the PNR is for the travel of the logged in company
        queryIsTravelBelongsToCompany = """
        SELECT *
        FROM Travel T
        WHERE T.travel_id = %s AND T.travel_company_id = %s
        """
        cursor.execute(queryIsTravelBelongsToCompany, (info['travel_id'], companyId))
        isExist = cursor.fetchone()

        if isExist:
            # Delete PNR from both Purchase and Booking
            # Thanks to cascade, deleting from Booking is enough
            queryDeletePNRFromBooking = """
            DELETE FROM Booking WHERE PNR = %s
            """
            cursor.execute(queryDeletePNRFromBooking, (PNRToBeDeleted,))
            cursor.connection.commit()
            message = "The booking is deleted."

            # Refund the paid amount
            queryRefund = """
            UPDATE Traveler SET balance = balance + %s WHERE id = %s
            """
            cursor.execute(queryRefund, (info['paid_amount'], info['traveler_id']))
            mysql.connection.commit()
            message = message + ' Paid amount for the travel with the ' + PNRToBeDeleted + ' PNR is refunded to the traveler.'
        else:
            message = "This PNR doesn't belong to one of your travels, so you cannot delete corresponding booking!"
        
        flash(message)
        return redirect(url_for('aTravelDetails', travelId = info['travel_id'] ))
    else:
        message = 'Session is not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/deleteAndGiveFreeTravel/<string:PNRToBeDeleted>', methods=['GET', 'POST'])
def deleteAndGiveFreeTravel(PNRToBeDeleted):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        companyId = session['userid']

        # Get user TCK, name, surname, travel_id which PNR belongs to, seat number, seat type, arrival and departure informations
        queryGetCurrentInfo = """
        SELECT 
        T.id AS traveler_id,
        T.TCK,
        T.name AS traveler_name, 
        T.surname AS traveler_surname, 
        B.travel_id, 
        B.seat_number, 
        B.seat_type, 
        Dep.city AS dep_ter_city, 
        Dep.name AS dep_ter_name, 
        Ar.city AS ar_ter_city,
        Ar.name AS ar_ter_name,
        TL.depart_time,
        TL.arrive_time
        FROM Traveler T
        JOIN Booking B ON T.id = B.traveler_id
        JOIN Purchased P ON P.PNR = B.PNR
        JOIN Travel TL ON TL.travel_id = B.travel_id
        JOIN Terminal Dep ON Dep.terminal_id = TL.departure_terminal_id
        JOIN Terminal Ar ON Ar.terminal_id = TL.arrival_terminal_id
        WHERE B.PNR = %s
        """
        cursor.execute(queryGetCurrentInfo, (PNRToBeDeleted,))
        currrentInfo = cursor.fetchone()

        # Check if the PNR is for the travel of the logged in company
        queryIsTravelBelongsToCompany = """
        SELECT *
        FROM Travel T
        WHERE T.travel_id = %s AND T.travel_company_id = %s
        """
        cursor.execute(queryIsTravelBelongsToCompany, (currrentInfo['travel_id'], companyId))
        isExist = cursor.fetchone()

        # For sorting possible travels, get request is used
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

        if isExist:
            # get all other upcoming travels of the company
            query = """
            SELECT *
            FROM Company C 
            JOIN Travel T ON C.id = T.travel_company_id
            JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
            JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
            JOIN Vehicle_Type V ON V.id = T.vehicle_type_id
            WHERE  C.id = %s AND T.depart_time > %s AND T.travel_id <> %s
            ORDER BY {}
            """.format(sort_type)

            cursor.execute(query, (companyId, datetime.now(), currrentInfo['travel_id']))
            travelDetailList = cursor.fetchall()

        else:
            message = "This PNR doesn't belong to one of your travels, so you cannot delete corresponding booking!"
            flash(message)
            return redirect(url_for('aTravelDetails', travelId = currrentInfo['travel_id'] ))
        
        if request.method == 'POST' and 'freeTravelId' in request.form:
            freeTravelId = request.form['freeTravelId']
            newPNR = generatePNR()
            newSeat = generateSeatNumber(freeTravelId)
            paymentMethod = 'gift'
            paymentPrice = 0
            seat_type = 'random'

            # add a tuple to the Booking table
            queryInsertBooking = """
            INSERT INTO Booking (PNR, travel_id, seat_number, traveler_id, seat_type)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(queryInsertBooking, (newPNR, freeTravelId, newSeat, currrentInfo['traveler_id'], seat_type))
            cursor.connection.commit()

            # add a tuple to the Purchased table
            queryInsertPurchased = """
            INSERT INTO Purchased (PNR, purchased_time, payment_method, price, coupon_id) 
            VALUES (%s, %s, %s, %s, NULL)
            """
            cursor.execute(queryInsertPurchased, (newPNR, datetime.now(), paymentMethod, paymentPrice))
            cursor.connection.commit()
            message1 = "A new Booking is completed for traveler with " + currrentInfo['TCK'] + " TCK number."

            # Delete PNR from both Purchase and Booking
            # Thanks to cascade, deleting from Booking is enough
            queryDeletePNRFromBooking = """
            DELETE FROM Booking WHERE PNR = %s
            """
            cursor.execute(queryDeletePNRFromBooking, (PNRToBeDeleted,))
            cursor.connection.commit()
            message = "The current booking is deleted." + message1
            flash(message)
            return redirect(url_for('aTravelDetails', travelId = currrentInfo['travel_id'] ))
       
        # flash(message)
        return render_template('deleteAndGiveFreeTravel.html', PNRToBeDeleted = PNRToBeDeleted, currrentInfo = currrentInfo, travelDetailList = travelDetailList, sort_type = sort_in )
    else:
        message = 'Session is not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/deleteAReservation/<string:PNRToBeDeleted>', methods=['GET', 'POST'])
def deleteAReservation(PNRToBeDeleted):
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        companyId = session['userid']

        # Get user id, travel id and paid amount for the purchase
        queryGetInfo = """
        SELECT T.id AS traveler_id, B.travel_id AS travel_id
        FROM Traveler T
        JOIN Booking B ON T.id = B.traveler_id
        WHERE B.PNR = %s
        """
        cursor.execute(queryGetInfo, (PNRToBeDeleted,))
        info = cursor.fetchone()

        # Check if the PNR is for the travel of the logged in company
        queryIsTravelBelongsToCompany = """
        SELECT *
        FROM Travel T
        WHERE T.travel_id = %s AND T.travel_company_id = %s
        """
        cursor.execute(queryIsTravelBelongsToCompany, (info['travel_id'], companyId))
        isExist = cursor.fetchone()

        if isExist:
            # Delete PNR from both Reserved and Booking
            # Deleting from Booking is enough due to cascade feature
            queryDeletePNRFromReserved = """
            DELETE FROM Booking WHERE PNR = %s
            """
            cursor.execute(queryDeletePNRFromReserved, (PNRToBeDeleted,))
            cursor.connection.commit()
            message = "The reservation is deleted."
        else:
            message = "This PNR doesn't belongs to one of your travels, so you cannot delete corresponding reservation!"
        
        flash(message)
        return redirect(url_for('aTravelDetails', travelId = info['travel_id'] ))
    else:
        message = 'Session is not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/companyProfile/<int:companyId>', methods=['GET', 'POST'])
def companyProfile(companyId): 
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company' or session['userType'] == 'admin':
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
    if 'userid' in session and 'loggedin' in session and 'userType' in session and session['userType'] == 'company' or session['userType'] == 'admin':
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
    
###############################
### ADMIN RELATED ROUTES ###
###############################

@app.route('/companies', methods=['GET', 'POST'])
def companies():
    if 'userid' in session and 'loggedin' in session:
        sort_type = 'C.id ASC'
        sort_in = 'sort_by_name'
        filter_in = 'all'
        filter_type = 'all'
        filterClause = ''

        if request.method == 'GET' and 'sort_type' in request.args or 'filter_type' in request.args:
            sort_in = request.args.get('sort_type')
            if sort_in == 'sort_by_name':
                sort_type = 'C.company_name'
            elif sort_in == 'validation_date_earliest_to_latest':
                sort_type = ' C.validation_date DESC'
            elif sort_in == 'validation_date_latest_to_earliest':
                sort_type = ' C.validation_date ASC'
            elif sort_in == 'foundation_date_earliest_to_latest':
                sort_type = 'C.foundation_date DESC'
            elif sort_in == 'foundation_date_latest_to_earliest':
                sort_type = 'C.foundation_date ASC'
            elif sort_in == 'sort_by_id':
                sort_type = 'C.id ASC'
            else:
                sort_type = 'C.id ASC'

            filter_in = request.args.get('filter_type')
            if filter_in == 'validated':
                filter_type = 'validated'
                filterClause = 'WHERE C.validation_date IS NOT NULL'
            elif filter_in == 'unvalidated':
                filter_type = 'unvalidated'
                filterClause = 'WHERE C.validation_date IS NULL'
            elif filter_in == 'active':
                filter_type = 'active'
                filterClause = 'WHERE U.active = TRUE'
            elif filter_in == 'inactive':
                filter_type = 'inactive'
                filterClause = 'WHERE U.active = FALSE'
            else:
                filter_type = 'all'
                filterClause = ''

        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        queryCompanies = """
        SELECT
        C.id,
        C.company_name,
        C.website,
        C.foundation_date,
        C.about,
        C.validation_date,
        U.email,
        U.phone,
        U.active,
        A.username as admin_username
        FROM Company C
        NATURAL JOIN User U
        LEFT JOIN Administrator A ON A.id = C.validator_id
        {whereClause}
        ORDER BY {sortClause}
        """.format(whereClause = filterClause, sortClause = sort_type)
        cursor.execute(queryCompanies)
        allCompanies = cursor.fetchall()

        return render_template('companies.html', allCompanies = allCompanies, sortType = sort_in, filterType = filter_in)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/deactivateCompany/<int:companyId>', methods = ['GET', 'POST'] )
def deactivateCompany(companyId):
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None

        # check the company
        queryGetCompany = """
        SELECT company_name
        FROM Company
        WHERE id = %s
        """
        cursor.execute(queryGetCompany, (companyId,))
        companyInfo = cursor.fetchone()
        
        if companyInfo:
            queryDeactivate = """
            UPDATE User SET active = FALSE WHERE id = %s
            """
            cursor.execute(queryDeactivate, (companyId,))
            cursor.connection.commit()
            message = 'Company ' + companyInfo['company_name'] + ' is succesfully deactivated.'

        flash(message)
        return redirect(url_for('companies'))
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/activateCompany/<int:companyId>', methods = ['GET', 'POST'] )
def activateCompany(companyId):
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None

        # check the company
        queryGetCompany = """
        SELECT company_name
        FROM Company
        WHERE id = %s
        """
        cursor.execute(queryGetCompany, (companyId,))
        companyInfo = cursor.fetchone()
        
        if companyInfo:
            queryDeactivate = """
            UPDATE User SET active = TRUE WHERE id = %s
            """
            cursor.execute(queryDeactivate, (companyId,))
            cursor.connection.commit()
            message = 'Company ' + companyInfo['company_name'] + ' is succesfully activated.'

        flash(message)
        return redirect(url_for('companies'))
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/validateCompany/<int:companyId>', methods = ['GET', 'POST'] )
def validateCompany(companyId):
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None

        # check the company
        queryGetCompany = """
        SELECT company_name
        FROM Company
        WHERE id = %s
        """
        cursor.execute(queryGetCompany, (companyId,))
        companyInfo = cursor.fetchone()
        
        if companyInfo:
            queryValidate = """
            UPDATE Company SET validator_id = %s, validation_date = %s WHERE id = %s
            """
            current_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(queryValidate, (session['userid'], current_date,companyId))
            cursor.connection.commit()
            message = 'Company ' + companyInfo['company_name'] + ' is validated.'

        flash(message)
        return redirect(url_for('companies'))
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/couponManagement', methods = ['GET', 'POST'])
def couponManagement():
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None

        # get all coupons
        queryGetCoupons = """
        SELECT *
        FROM Sale_Coupon
        """
        cursor.execute(queryGetCoupons)
        allCoupons = cursor.fetchall()

        return render_template('couponManagement.html', allCoupons = allCoupons)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/createCoupon', methods = [ 'GET', 'POST'])
def createCoupon():
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None

        if request.method == 'POST':
            if 'coupon_name' in request.form and request.form['coupon_name'] and \
            'sale_rate' in request.form and request.form['sale_rate'] and \
            'expiration_date' in request.form and request.form['expiration_date'] and \
            'public_status' in request.form and request.form['public_status']:
                
                coupon_name = request.form['coupon_name']
                sale_rate = request.form['sale_rate']
                expiration_date = request.form['expiration_date']
                public_status = request.form['public_status']
                current_date = datetime.now().strftime("%Y-%m-%d")

                # check if sale rate is between 0 to 1
                if float(sale_rate) < 0.0 or float(sale_rate) > 1.0:
                    message = 'Sale rate must be between 0 and 1'
                    return render_template('createCoupon.html', message = message)

                #check if there is a non-expired coupon with the given name
                queryFindCoupon = """
                SELECT *
                FROM Sale_Coupon
                WHERE coupon_name = %s AND expiration_date > %s AND public_status = %s
                """
                cursor.execute(queryFindCoupon, (coupon_name, current_date, public_status))
                existingCoupon = cursor.fetchone()
                if existingCoupon:
                    message = 'There is an available coupon with ' + coupon_name + ' name! '
                    message = message + 'To be able to create a coupon with the same name, the expiration date of existing coupon must be passed.'
                else:
                    # create new coupon and insert in to Sale_Coupon table
                    queryInsertCoupon = """
                    INSERT INTO Sale_Coupon (coupon_id, coupon_name, sale_rate, expiration_date, generation_date, public_status)
                    VALUES (NULL, %s, %s, %s, %s, %s)
                    """
                
                    cursor.execute(queryInsertCoupon, (coupon_name, sale_rate, expiration_date, current_date, public_status))
                    cursor.connection.commit()
                    message = 'A coupon with ' + coupon_name + ' name, ' + sale_rate + ' sale rate, ' + expiration_date + 'expiration date and with ' + public_status + ' availability is created.'
                    flash(message)
                    return redirect(url_for('couponManagement'))
            else:
                message = 'Please fill the form!'

        return render_template('createCoupon.html', message = message)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/deleteACoupon/<int:couponId>', methods = [ 'GET', 'POST' ])
def deleteACoupon(couponId):
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None
        # check if there is a coupon with that id
        queryFindCoupon = """
        SELECT *
        FROM Sale_Coupon
        WHERE coupon_id = %s
        """
        cursor.execute(queryFindCoupon, (couponId,))
        theCoupon = cursor.fetchone()

        if theCoupon:
            queryDeleteCoupon = """
            DELETE FROM Sale_Coupon WHERE coupon_id = %s
            """
            cursor.execute(queryDeleteCoupon, (couponId,))
            cursor.connection.commit()
            message = 'The ' + theCoupon['coupon_name'] + ' coupon with ' + str(theCoupon['sale_rate']) + ' sale rate, ' + theCoupon['expiration_date'].strftime("%Y-%m-%d") + 'expiration date and with ' + theCoupon['public_status']  + ' availability is deleted.'
        else:
            message = "There is no such coupon!"

        flash(message)
        return redirect(url_for('couponManagement'))
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/vehicleManagement', methods = ['GET', 'POST'])
def vehicleManagement():
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None

        # get all vehicles
        queryGetVehicles = """
        SELECT *
        FROM Vehicle_Type
        """
        cursor.execute(queryGetVehicles)
        allVehicles = cursor.fetchall()

        return render_template('vehicleManagement.html', allVehicles = allVehicles)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)

@app.route('/createVehicleType', methods = [ 'GET', 'POST'])
def createVehicleType():
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None

        if request.method == 'POST':
            if 'vehicle_type' in request.form and request.form['vehicle_type'] and \
            'vehicle_seat_formation' in request.form and request.form['vehicle_seat_formation'] and \
            'vehicle_num_of_seats' in request.form and request.form['vehicle_num_of_seats'] and \
            'vehicle_business_rows' in request.form and request.form['vehicle_business_rows'] and \
            'vehicle_model' in request.form and request.form['vehicle_model'] :
                
                vehicle_type = request.form['vehicle_type']
                vehicle_seat_formation = request.form['vehicle_seat_formation']
                vehicle_num_of_seats = request.form['vehicle_num_of_seats']
                vehicle_business_rows = request.form['vehicle_business_rows']
                vehicle_model = request.form['vehicle_model']

                seatNumList = vehicle_seat_formation.strip().split('-')
                numSeatsInRow = sum(int(seat) for seat in seatNumList if seat != '')

                # check if the given seat formation is in the correct format
                if not validate_seat_formation(vehicle_seat_formation):
                    message = "Invalid format for seat formation "
                elif int(vehicle_num_of_seats) % numSeatsInRow != 0:
                    # check if the total seat number matches is divisable by seat number in a row
                    message = "The total number of seats in the vehicle is not divisible by number of seats in a row!"
                elif int(vehicle_business_rows) > (int(vehicle_num_of_seats) / numSeatsInRow):
                    # check if the business row is equal or smaller than the total row
                    message = "Number of rows for business class cannot be larger than the number of rows the vehicle have!"
                else:    
                    # check if there is such vehicle type which all properties are some with given values
                    queryFindVehicle = """
                    SELECT *
                    FROM Vehicle_Type
                    WHERE model = %s AND type = %s AND seat_formation = %s AND num_of_seats = %s AND business_rows = %s
                    """
                    cursor.execute(queryFindVehicle, (vehicle_model, vehicle_type, vehicle_seat_formation, vehicle_num_of_seats, vehicle_business_rows))
                    existingVehicleType = cursor.fetchone()
                    if existingVehicleType:
                        message = 'There is already an existing vehicle type that has the same properties'
                        return render_template('createVehicleType.html', message = message)
                    else:
                        # create the vehicle type
                        queryInsertVehicle = """
                        INSERT INTO Vehicle_Type (id, model, type, seat_formation, num_of_seats, business_rows)
                        VALUES (NULL, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(queryInsertVehicle, (vehicle_model, vehicle_type, vehicle_seat_formation, vehicle_num_of_seats, vehicle_business_rows))
                        cursor.connection.commit()
                        message = "New vehicle Type successfully added!"
                        flash(message)
                        return redirect(url_for('vehicleManagement'))
            else:
                message = 'Please fill the form!'

        return render_template('createVehicleType.html', message = message)
    else:
        message = 'Session was not valid, please log in!'
        return render_template('login.html', message = message)
    
@app.route('/deleteAVehicleType/<int:vehicleTypeId>', methods = [ 'GET', 'POST' ])
def deleteAVehicleType(vehicleTypeId):
    if 'userid' in session and 'loggedin' in session and session['userType'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = None

        queryFindVehicleType = """
        SELECT *
        FROM Vehicle_Type
        WHERE id = %s
        """
        cursor.execute(queryFindVehicleType, (vehicleTypeId,))
        theVehicleType = cursor.fetchone()

        if theVehicleType:
            queryDeleteVehicleType = """
            DELETE FROM Vehicle_Type WHERE id = %s
            """
            cursor.execute(queryDeleteVehicleType, (vehicleTypeId,))
            cursor.connection.commit()
            message = "The vehicle type " + theVehicleType['model'] + " is deleted."
        else:
            message = "There is no such vehicle type"

        flash(message)
        return redirect(url_for('vehicleManagement'))
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

def buy_one(travel_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    user_id = session.get('userid')

    pnr = generatePNR()
    seat_number = generateSeatNumber(travel_id)

    # Check if the travel_id is associated with a reserved booking
    query_check_reserved_booking = """
    SELECT *
    FROM Booking
    JOIN Reserved ON Booking.PNR = Reserved.PNR
    WHERE travel_id = %s AND traveler_id = %s
    """
    cursor.execute(query_check_reserved_booking, (travel_id, user_id))
    reserved_booking = cursor.fetchone()

    if reserved_booking:
        pnr = reserved_booking['PNR']
        seat_number = reserved_booking['seat_number']

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

    # Generate the current timestamp
    purchase_time = datetime.now()

    # Check if a coupon is used
    coupon_id = request.form.get('coupon_id')

    # Calculate the price to be deducted from the balance
    if coupon_id:
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
    else:
        # No coupon applied, use the original price
        discounted_price = travel_details['price']

    # Calculate the updated balance
    updated_balance = balance['balance'] - discounted_price

    # Check if user has sufficient funds
    if updated_balance < travel_details['price']:
        flash("Insuffiecient funds!", "error")
        return redirect(url_for('buy_travel', travel_id=travel_id))

    # If purchasing already booked (reserved) travel 
    if reserved_booking:
        query_insert_purchased = """
        INSERT INTO Purchased(PNR, purchased_time, payment_method, price, coupon_id)
        VALUES (%s, %s, %s, %s, %s) 
        """
        cursor.execute(query_insert_purchased, (pnr, purchase_time, 'credit card', discounted_price, coupon_id))

        query_delete_reserved = """
        DELETE FROM Reserved
        WHERE PNR = %s
        """
        cursor.execute(query_delete_reserved, (pnr,))

        query_update_balance = """
        UPDATE Traveler
        SET Balance = %s
        WHERE id = %s
        """
        cursor.execute(query_update_balance, (updated_balance, user_id))
        mysql.connection.commit()

    else:
        query_insert_booking = """
        INSERT INTO Booking(PNR, travel_id, seat_number, traveler_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_insert_booking, (pnr, travel_id, seat_number, user_id))

        query_insert_purchased = """
        INSERT INTO Purchased(PNR, purchased_time, payment_method, price, coupon_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert_purchased, (pnr, purchase_time, 'credit card', discounted_price, coupon_id))

        query_update_balance = """
        UPDATE Traveler
        SET Balance = %s
        WHERE id = %s
        """
        cursor.execute(query_update_balance, (updated_balance, user_id))
        mysql.connection.commit()

    return

def reserve_one(travel_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    user_id = session.get('userid')

    pnr = generatePNR()
    seat_number = generateSeatNumber(travel_id)

    # Check if the travel_id is associated with a reserved booking
    query_check_reserved_booking = """
    SELECT *
    FROM Booking
    JOIN Reserved ON Booking.PNR = Reserved.PNR
    WHERE travel_id = %s AND traveler_id = %s
    """
    cursor.execute(query_check_reserved_booking, (travel_id, user_id))
    reserved_booking = cursor.fetchone()

    if reserved_booking:
        pnr = reserved_booking['PNR']
        seat_number = reserved_booking['seat_number']

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

    # Generate the current timestamp
    reserved_time = datetime.now()

    # Calculate the purchase deadline (2 days before departure time)
    depart_time = travel_details['depart_time']
    purchase_deadline = depart_time - timedelta(days=2)
    
    query_insert_booking = """
    INSERT INTO Booking(PNR, travel_id, seat_number, traveler_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query_insert_booking, (pnr, travel_id, seat_number, user_id))

    # Insert data into Reserved table
    query_insert_reserved = """
    INSERT INTO Reserved(PNR, reserved_time, purchased_deadline)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query_insert_reserved, (pnr, reserved_time, purchase_deadline))
    mysql.connection.commit()

def validate_seat_formation(seat_formation):
    seat_numbers = seat_formation.split('-')
    if len(seat_numbers) < 2 or len(seat_numbers) > 4:
        return False
    for seat in seat_numbers:
        if not seat.isdigit():
            return False
    if seat_formation.endswith('-'):
        return False
    return True

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
