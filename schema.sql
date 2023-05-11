CREATE DATABASE IF NOT EXISTS subilet;
USE subilet;

CREATE TABLE User (
    id INT AUTO_INCREMENT,
    email VARCHAR(256) NOT NULL,
    password VARCHAR(256) NOT NULL,
    phone VARCHAR(256) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (phone)
);

CREATE TABLE Traveler (
    id INT,
    TCK VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    age TINYINT NOT NULL,
    balance DECIMAL(10,2) DEFAULT 0,
    PRIMARY KEY(id),
    FOREIGN KEY(id) REFERENCES User(id) ON DELETE CASCADE,
    UNIQUE (TCK),
    CONSTRAINT check_age
    CHECK ( age > 18 )
);

CREATE TABLE Administrator (
    id INT DEFAULT 0,
    username VARCHAR(256) NOT NULL,
    last_login_time DATETIME DEFAULT NULL,
    income DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY(id),
    FOREIGN KEY(id) REFERENCES User(id)
        ON DELETE CASCADE,
    UNIQUE(username)
);

CREATE TABLE Company (
    id INT,
    company_name VARCHAR(256),
    website VARCHAR(256),
    foundation_date DATE,
    about TEXT DEFAULT NULL,
    validator_id INT DEFAULT NULL,
    validation_date DATETIME DEFAULT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(id) REFERENCES User(id)
        ON DELETE CASCADE,
    FOREIGN KEY(validator_id) REFERENCES Administrator(id)
        ON DELETE SET NULL,
    UNIQUE (company_name),
    UNIQUE (website)
);

CREATE TABLE Report (
    report_id INT,
    report_date DATETIME,
    total_sales DECIMAL(15,2),
    total_reviews INT,
    total_company INT,
    pending_compan INT,
    total_travelers INT,
    total_bus INT,
    total_train INT,
    total_plane INT,
    report_generator_id INT,
    PRIMARY KEY(report_id),
    FOREIGN KEY(report_generator_id) REFERENCES Administrator(id) ON DELETE SET NULL,
    UNIQUE (report_date)
);

CREATE TABLE Sale_Coupon (
    coupon_id INT,
    coupon_name VARCHAR(20) NOT NULL,
    sale_rate DECIMAL(3,2) NOT NULL,
    expiration_date DATE NOT NULL,
    generation_date DATE NOT NULL,
    public_status ENUM( 'public', 'private' ) NOT NULL,
    PRIMARY KEY(coupon_id)
);

CREATE TABLE Coupon_Traveler(
    coupon_id INT,
    user_id INT,
    used_status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(coupon_id, user_id),
    FOREIGN KEY(coupon_id) REFERENCES Sale_Coupon(coupon_id)
        ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES Traveler(id)
        ON DELETE CASCADE
);

CREATE TABLE Vehicle_Type(
	id INT AUTO_INCREMENT,
    model VARCHAR(256) NOT NULL,
	type VARCHAR(256) NOT NULL,
	seat_formation VARCHAR(256) NOT NULL,
	num_of_seats INT NOT NULL DEFAULT 0,
	business_rows INT NOT NULL DEFAULT 0,
	PRIMARY KEY (id),
	UNIQUE ( model )
);

CREATE TABLE Terminal(
    terminal_id INT AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    city VARCHAR(256) NOT NULL,
    type ENUM( 'plane', 'train', 'bus' ) NOT NULL,
    active_status ENUM( 'active', 'inactive'),
    PRIMARY KEY (terminal_id),
    UNIQUE (name)
);

CREATE TABLE Travel(
	travel_id INT AUTO_INCREMENT,
	travel_company_id INT NOT NULL,
	departure_terminal_id INT NOT NULL,
	arrival_terminal_id INT NOT NULL,
	depart_time DATETIME NOT NULL,
	arrive_time DATETIME NOT NULL,
	price	 DECIMAL(10,2) NOT NULL,
	business_price DECIMAL(10,2),
	vehicle_type_id INT,
	PRIMARY KEY(travel_id),
	FOREIGN KEY(travel_company_id) REFERENCES Company(id)
        ON DELETE CASCADE,
	FOREIGN KEY(departure_terminal_id) REFERENCES Terminal(terminal_id)
		ON DELETE NO ACTION,
	FOREIGN KEY(arrival_terminal_id) REFERENCES Terminal(terminal_id)
		ON DELETE NO ACTION,
	FOREIGN KEY(vehicle_type_id) REFERENCES Vehicle_Type(id)
		ON DELETE SET NULL,
	CHECK (arrive_time > depart_time)
);

CREATE TABLE Booking(
	PNR VARCHAR(20),
	travel_id INT,
	seat_number INT NOT NULL,
	traveler_id INT,
    seat_type ENUM( 'business', 'regular' ) NOT NULL DEFAULT 'regular',
	PRIMARY KEY(PNR),
	FOREIGN KEY (travel_id) REFERENCES Travel(travel_id)
		ON DELETE CASCADE,
    FOREIGN KEY (traveler_id) REFERENCES Traveler(id) 
	    ON DELETE CASCADE
);

CREATE TABLE Reserved(
	PNR VARCHAR(20),
	reserved_time DATETIME NOT NULL,
	purchased_deadline DATETIME NOT NULL,
	PRIMARY KEY(PNR),
	FOREIGN KEY (PNR) REFERENCES Booking(PNR) 
		ON DELETE CASCADE
);

CREATE TABLE Purchased(
	PNR VARCHAR(20),
	purchased_time DATETIME NOT NULL,
	payment_method VARCHAR(20) NOT NULL,
	price INT NOT NULL DEFAULT 0,
	coupon_id INT DEFAULT NULL,
	PRIMARY KEY(PNR),
	FOREIGN KEY (PNR) REFERENCES Booking(PNR)
        ON DELETE CASCADE,
	FOREIGN KEY (coupon_id) REFERENCES Sale_Coupon(coupon_id)
		ON DELETE SET NULL
);

CREATE TABLE Journey(
	journey_name VARCHAR(256) NOT NULL,
	traveler_id INT,
	created_time DATETIME NOT NULL,
	isValid ENUM('valid', 'not valid') NOT NULL DEFAULT 'valid',
	PRIMARY KEY (journey_name, traveler_id),
	FOREIGN KEY (traveler_id) REFERENCES Traveler(id)
		ON DELETE CASCADE
); 

CREATE TABLE Travels_In_Journey(
	journey_name VARCHAR(256) NOT NULL,
	traveler_id INT,
	travel_id INT,
	PRIMARY KEY (journey_name, traveler_id, travel_id),
	FOREIGN KEY (journey_name) REFERENCES Journey(journey_name)
		ON DELETE CASCADE,
	FOREIGN KEY (traveler_id) REFERENCES Traveler(id)
		ON DELETE CASCADE,
	FOREIGN KEY (travel_id) REFERENCES Travel(travel_id)
		ON DELETE CASCADE
); 

CREATE TABLE Review(
	travel_id INT,
	traveler_id INT,
	comment TEXT DEFAULT NULL,
	rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
	PRIMARY KEY (travel_id, traveler_id),
    FOREIGN KEY (travel_id) REFERENCES Travel(travel_id)
		ON DELETE CASCADE,
	FOREIGN KEY (traveler_id) REFERENCES Traveler(id)
		ON DELETE CASCADE		
);


