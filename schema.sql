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

INSERT INTO User (id, email, password, phone, active) VALUES
(1, 'admin1@example.com', '123456', '555 444 33 22', TRUE),
(2, 'admin2@example.com', '123456', '555 444 33 23', TRUE),
(3, 'admin3@example.com', '123456', '555 444 33 24', TRUE),
(4, 'company1@example.com', '123456', '555 444 33 25', TRUE),
(5, 'company2@example.com', '123456', '555 444 33 26', TRUE),
(6, 'company3@example.com', '123456', '555 444 33 27', TRUE),
(7, 'traveler1@example.com', '123456', '555 444 33 28', TRUE),
(8, 'traveler2@example.com', '123456', '555 444 33 29', TRUE),
(9, 'traveler3@example.com', '123456', '555 444 33 30', TRUE);

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
    CHECK ( age >= 18 )
);

INSERT INTO Traveler (id, TCK, name, surname, age, balance) VALUES
(7, '11111111111', 'traveler1Name', 'traveler1Surname', 18, 10000 ),
(8, '11111111112', 'traveler2Name', 'traveler2Surname', 18,  50000),
(9, '11111111113', 'traveler3Name', 'traveler3Surname', 18, 8000 );

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

INSERT INTO Administrator (id, username, last_login_time, income) VALUES
(1, 'admin1', '2023-05-09 17:00:00', 1000.00),
(2, 'admin2', '2023-05-10 17:00:00', 2000.00),
(3, 'admin3', '2023-05-11 17:00:00', 3000.00);

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

INSERT INTO Company (id, company_name, website, foundation_date, about, validator_id, validation_date) VALUES
(4, 'company1', 'https://company1.com.tr', '2000-01-01', 'about company 1', 1, '2000-01-02' ),
(5, 'company2', 'https://company2.com.tr', '2000-01-01', 'about company 2', 1, '2000-01-02' ),
(6, 'company3', 'https://company3.com.tr', '2000-01-01', 'about company 3', 1, '2000-01-02' );

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
    coupon_id INT AUTO_INCREMENT,
    coupon_name VARCHAR(20) NOT NULL,
    sale_rate DECIMAL(3,2) NOT NULL,
    expiration_date DATE NOT NULL,
    generation_date DATE NOT NULL,
    public_status ENUM( 'public', 'private' ) NOT NULL,
    PRIMARY KEY(coupon_id)
);

INSERT INTO Sale_Coupon (coupon_id, coupon_name, sale_rate, expiration_date, generation_date, public_status) VALUES
(1, 'indirim10', 0.10, '2023-08-31', '2023-05-01', 'public' ),
(2, 'indirim20', 0.20, '2023-08-31', '2023-05-01', 'public' ),
(3, 'indirim30', 0.30, '2023-08-31', '2023-05-01', 'public' ),
(4, 'indirim10', 0.10, '2023-12-31', '2023-05-02', 'private' ),
(5, 'indirim20', 0.20, '2023-12-31', '2023-05-02', 'private' ),
(6, 'indirim30', 0.30, '2023-12-31', '2023-05-02', 'private' );

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

INSERT INTO Vehicle_Type (id, model, type, seat_formation, num_of_seats, business_rows) VALUES
(1, 'Travego1', 'bus', '2-2', 52, 0 ),
(2, 'Tourismo', 'bus', '2-2', 60, 0 ),
(3, 'Boeing737-1', 'plane', '3-3', 180, 5 ),
(4, 'Boeing777-1', 'plane', '3-3-3', 360, 10 );

CREATE TABLE Terminal(
    terminal_id INT AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    city VARCHAR(256) NOT NULL,
    type ENUM( 'plane', 'train', 'bus' ) NOT NULL,
    active_status ENUM( 'active', 'inactive'),
    PRIMARY KEY (terminal_id),
    UNIQUE (name)
);

INSERT INTO Terminal (terminal_id, name, city, type, active_status) VALUES
( 1, 'Atatürk Airport', 'İstanbul', 'plane', 'active'),
( 2, 'Sabiha Gökçen Airport', 'İstanbul', 'plane', 'active'),
( 3, 'Esenboğa Airport', 'Ankara', 'plane', 'active'),
( 4, 'Adana Şakirpaşa Airport', 'Adana', 'plane', 'active'),
( 5, 'Harem Bus Terminal', 'İstanbul', 'bus', 'active'),
( 6, 'Ankara Train Station', 'Ankara', 'train', 'active'),
( 7, 'Antalya Airport', 'Antalya', 'plane', 'active'),
( 8, 'Dalaman Airport', 'Muğla', 'plane', 'active'),
( 9, 'Söğütlüçeşme Train Station', 'İstanbul', 'train', 'active'),
( 10, 'Çanakkale Bus Terminal', 'Çanakkale', 'bus', 'active'),
( 11, 'Konya Airport', 'Konya', 'plane', 'active'),
( 12, 'Alsancak Train Station', 'İzmir', 'train', 'active'),
( 13, 'Bursa Bus Terminal', 'Bursa', 'bus', 'active'),
( 14, 'Gazipaşa Airport', 'Antalya', 'plane', 'active'),
( 15, 'Haydarpaşa Train Station', 'Istanbul', 'train', 'active'),
( 16, 'Denizli Bus Terminal', 'Denizli', 'bus', 'active'),
( 17, 'Kemer Train Station', 'Antalya', 'train', 'active');


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
-- the type of terminal for departure and arrival must be same

INSERT INTO Travel (travel_id, travel_company_id, departure_terminal_id, arrival_terminal_id, depart_time, arrive_time, price, business_price, vehicle_type_id) VALUES
(1, 4, 1, 3, '2023-06-01 10:00:00', '2023-06-01 12:00:00', 999.00, 1399.00, 3),
(2, 4, 3, 1, '2023-06-01 13:00:00', '2023-06-01 15:00:00', 999.00, 1399.00, 3),
(3, 4, 3, 4, '2023-08-01 19:00:00', '2023-08-01 21:00:00', 899.00, 1299.00, 4),
(4, 4, 3, 4, '2023-04-12 19:00:00', '2023-04-12 21:00:00', 899.00, 1299.00, 3),
(5, 4, 5, 10, '2023-06-25 09:00:00', '2023-06-25 15:00:00', 299.00, NULL, 1),
(6, 4, 16, 13, '2023-06-25 09:00:00', '2023-06-25 16:00:00', 299.00, NULL, 2),
(7, 5, 1, 3, '2023-06-01 10:00:00', '2023-06-01 12:00:00', 1299.00, 1799.00, 3),
(8, 5, 3, 1, '2023-06-01 13:00:00', '2023-06-01 15:00:00', 999.00, 1399.00, 3),
(9, 5, 3, 4, '2023-08-01 19:00:00', '2023-08-01 21:00:00', 899.00, 1299.00, 4),
(10, 5, 3, 4, '2023-04-12 19:00:00', '2023-04-12 21:00:00', 899.00, 1299.00, 3),
(11, 5, 5, 10, '2023-06-25 09:00:00', '2023-06-25 15:00:00', 349.00, NULL, 1),
(12, 5, 16, 13, '2023-06-25 09:00:00', '2023-06-25 16:00:00', 349.00, NULL, 2),
(13, 6, 1, 3, '2023-06-01 10:00:00', '2023-06-01 12:00:00', 1199.00, 1699.00, 3),
(14, 6, 3, 1, '2023-06-01 13:00:00', '2023-06-01 15:00:00', 899.00, 1199.00, 3),
(15, 6, 3, 4, '2023-08-01 19:00:00', '2023-08-01 21:00:00', 799.00, 1199.00, 4),
(16, 6, 3, 4, '2023-04-12 19:00:00', '2023-04-12 21:00:00', 799.00, 1199.00, 3),
(17, 6, 5, 10, '2023-06-25 09:00:00', '2023-06-25 15:00:00', 249.00, NULL, 1),
(18, 6, 16, 13, '2023-06-25 09:00:00', '2023-06-25 16:00:00', 259.00, NULL, 2);

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

INSERT INTO Booking (PNR, travel_id, seat_number, traveler_id, seat_type) VALUES
('PLANE111', 1, 43, 7, 'regular'),
('PLANE112', 1, 44, 8, 'regular'),
('PLANE113', 1, 1, 9, 'business'),
('BUS101', 5, 12, 9, 'regular'),
('BUS102', 5, 15, 8, 'regular'),
('BUS103', 5, 20, 7, 'regular');

CREATE TABLE Reserved(
	PNR VARCHAR(20),
	reserved_time DATETIME NOT NULL,
	purchased_deadline DATETIME NOT NULL,
	PRIMARY KEY(PNR),
	FOREIGN KEY (PNR) REFERENCES Booking(PNR) 
		ON DELETE CASCADE
);

INSERT INTO Reserved (PNR, reserved_time, purchased_deadline) VALUES
('PLANE111', '2023-02-01 10:00:00', '2023-05-30 10:00:00'),
('BUS101', '2023-03-01 12:15:00', '2023-06-22 09:00:00');


CREATE TABLE Purchased(
	PNR VARCHAR(20),
	purchased_time DATETIME NOT NULL,
	payment_method VARCHAR(20) NOT NULL,
	price  DECIMAL(10,2) NOT NULL DEFAULT 0,
	coupon_id INT DEFAULT NULL,
	PRIMARY KEY(PNR),
	FOREIGN KEY (PNR) REFERENCES Booking(PNR)
        ON DELETE CASCADE,
	FOREIGN KEY (coupon_id) REFERENCES Sale_Coupon(coupon_id)
		ON DELETE SET NULL
);

INSERT INTO Purchased (PNR, purchased_time, payment_method, price, coupon_id) VALUES
('PLANE112', '2023-04-01 19:00:00', 'creadit card', 999.00, NULL),
('PLANE113', '2023-05-01 21:00:00', 'creadit card', 1399.00, NULL),
('BUS102', '2023-05-10 08:00:00', 'creadit card', 299.00, NULL),
('BUS103', '2023-05-10 23:30:00', 'creadit card', 299.00, NULL);


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


