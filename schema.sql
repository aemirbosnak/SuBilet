ALTER DATABASE subiletdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS subiletdb;
USE subiletdb;

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
(9, 'traveler3@example.com', '123456', '555 444 33 30', TRUE),
(10, 'traveler4@example.com', '123456', '555 444 33 31', TRUE),
(11, 'traveler5@example.com', '123456', '555 444 33 32', TRUE),
(12, 'company4@example.com', '123456', '555 444 33 33', TRUE),
(13, 'company5@example.com', '123456', '555 444 33 34', TRUE),
(14, 'company6@example.com', '123456', '555 444 33 35', FALSE);

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
(9, '11111111113', 'traveler3Name', 'traveler3Surname', 18, 8000 ),
(10, '11111111114', 'traveler4Name', 'traveler4Surname', 21, 8000 ),
(11, '11111111115', 'traveler5Name', 'traveler4Surname', 23, 800);

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
    foundation_date DATE DEFAULT NULL,
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
(5, 'company2', 'https://company2.com.tr', '2001-02-03', 'about company 2', 2, '2001-02-05' ),
(6, 'company3', 'https://company3.com.tr', '2002-03-04', 'about company 3', 1, '2002-03-05' ),
(12, 'company4', 'https://company4.com.tr', '2002-03-04', 'about company 4', NULL, NULL ),
(13, 'company5', 'https://company5.com.tr', '2002-03-04', 'about company 5', NULL, NULL ),
(14, 'company6', 'https://company6.com.tr', '2005-04-05', 'about company 6', 2, '2005-05-06' );

CREATE TABLE Report (
    report_id INT AUTO_INCREMENT,
    report_date DATETIME,
    admin_number INT,
    traveler_number INT,
    company_number INT,
    pending_company_number INT,
    terminal_number INT,
    vehicle_type_number INT,
    total_purchase_number INT,
    total_purchase_amount DECIMAL(15,2),
    total_reviews INT,
    coupon_usage_percentage INT,
    past_bus_number INT,
    upcoming_bus_number INT,
    past_plane_number INT,
    upcoming_plane_number INT,
    past_train_number INT,
    upcoming_train_number INT,
    company_with_max_revenue VARCHAR(256),
    company_with_max_travel_number VARCHAR(256),
    company_with_max_rating VARCHAR(256),
    report_generator_id INT,
    PRIMARY KEY(report_id),
    FOREIGN KEY(report_generator_id) REFERENCES Administrator(id) ON DELETE SET NULL,
    FOREIGN KEY(company_with_max_revenue) REFERENCES Company(company_name) ON DELETE SET NULL,
    FOREIGN KEY(company_with_max_travel_number) REFERENCES Company(company_name) ON DELETE SET NULL,
    FOREIGN KEY(company_with_max_rating) REFERENCES Company(company_name) ON DELETE SET NULL,
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
(6, 'indirim30', 0.30, '2023-12-31', '2023-05-02', 'private' ),
(7, 'indirim40', 0.30, '2023-04-30', '2023-01-01', 'public' );

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

INSERT INTO Coupon_Traveler (coupon_id, user_id, used_status) VALUES
(1, 7, TRUE),
(1, 8, FALSE),
(1, 9, TRUE),
(1, 10, TRUE),
(3, 7, FALSE),
(5, 8, FALSE),
(5, 9, TRUE),
(6, 7, FALSE),
(6, 8, TRUE),
(6, 9, FALSE);

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
    active_status ENUM( 'active', 'inactive') DEFAULT 'active',
    PRIMARY KEY (terminal_id),
    UNIQUE (name)
);

INSERT INTO Terminal (terminal_id, name, city, type, active_status) VALUES
( 1, 'Ataturk Airport', 'Istanbul', 'plane', 'active'),
( 2, 'Sabiha Gokcen Airport', 'Istanbul', 'plane', 'active'),
( 3, 'Esenboga Airport', 'Ankara', 'plane', 'active'),
( 4, 'Adana Sakirpasa Airport', 'Adana', 'plane', 'active'),
( 5, 'Harem Bus Terminal', 'Istanbul', 'bus', 'active'),
( 6, 'Ankara Train Station', 'Ankara', 'train', 'active'),
( 7, 'Antalya Airport', 'Antalya', 'plane', 'active'),
( 8, 'Dalaman Airport', 'Mugla', 'plane', 'active'),
( 9, 'Sogutlucesme Train Station', 'Istanbul', 'train', 'active'),
( 10, 'Canakkale Bus Terminal', 'Canakkale', 'bus', 'active'),
( 11, 'Konya Airport', 'Konya', 'plane', 'active'),
( 12, 'Alsancak Train Station', 'Izmir', 'train', 'active'),
( 13, 'Bursa Bus Terminal', 'Bursa', 'bus', 'active'),
( 14, 'Gazipasa Airport', 'Antalya', 'plane', 'active'),
( 15, 'Haydarpasa Train Station', 'Istanbul', 'train', 'active'),
( 16, 'Denizli Bus Terminal', 'Denizli', 'bus', 'active'),
( 17, 'Kemer Train Station', 'Antalya', 'train', 'active'),
( 18, 'ASTI', 'ANKARA', 'bus', 'active');


CREATE TABLE Travel(
	travel_id INT AUTO_INCREMENT,
	travel_company_id INT NOT NULL,
	departure_terminal_id INT,
	arrival_terminal_id INT,
	depart_time DATETIME NOT NULL,
	arrive_time DATETIME NOT NULL,
	price	 DECIMAL(10,2) NOT NULL,
	business_price DECIMAL(10,2) DEFAULT 0,
	vehicle_type_id INT,
	PRIMARY KEY(travel_id),
	FOREIGN KEY(travel_company_id) REFERENCES Company(id)
        ON DELETE CASCADE,
	FOREIGN KEY(departure_terminal_id) REFERENCES Terminal(terminal_id)
		ON DELETE SET NULL,
	FOREIGN KEY(arrival_terminal_id) REFERENCES Terminal(terminal_id)
		ON DELETE SET NULL,
	FOREIGN KEY(vehicle_type_id) REFERENCES Vehicle_Type(id)
		ON DELETE SET NULL,
	CHECK (arrive_time > depart_time)
);
-- the type of terminal for departure and arrival must be same

INSERT INTO Travel (travel_id, travel_company_id, departure_terminal_id, arrival_terminal_id, depart_time, arrive_time, price, business_price, vehicle_type_id) VALUES
(1, 4, 1, 3, '2023-06-20 10:00:00', '2023-06-20 12:00:00', 1000.00, 1399.00, 3),
(2, 4, 3, 1, '2023-06-20 13:00:00', '2023-06-20 15:00:00', 1000.00, 1399.00, 3),
(3, 4, 3, 4, '2023-08-20 19:00:00', '2023-08-20 21:00:00', 900.00, 1299.00, 4),
(4, 4, 3, 4, '2023-04-12 18:00:00', '2023-04-12 20:00:00', 900.00, 1299.00, 3),
(5, 4, 5, 10, '2023-06-25 09:00:00', '2023-06-25 15:00:00', 300.00, NULL, 1),
(6, 4, 16, 13, '2023-06-25 09:00:00', '2023-06-25 16:00:00', 300.00, NULL, 2),
(7, 5, 1, 3, '2023-06-20 10:00:00', '2023-06-20 12:00:00', 1300.00, 1799.00, 3),
(8, 5, 3, 1, '2023-06-20 13:00:00', '2023-06-20 15:00:00', 1000.00, 1399.00, 3),
(9, 5, 3, 4, '2023-08-20 19:00:00', '2023-08-20 21:00:00', 1000.00, 1299.00, 4),
(10, 5, 3, 4, '2023-04-12 20:00:00', '2023-04-12 22:00:00', 900.00, 1299.00, 3),
(11, 5, 5, 18, '2023-06-06 09:00:00', '2023-06-25 15:00:00', 350.00, NULL, 2),
(12, 5, 16, 13, '2023-06-25 09:00:00', '2023-06-25 16:00:00', 350.00, NULL, 2),
(13, 5, 5, 18, '2023-06-25 09:00:00', '2023-06-25 13:00:00', 200.00, NULL, 2),
(14, 6, 1, 3, '2023-06-20 10:00:00', '2023-06-20 12:00:00', 1200.00, 1699.00, 3),
(15, 6, 3, 1, '2023-06-20 13:00:00', '2023-06-20 15:00:00', 900.00, 1199.00, 3),
(16, 6, 3, 4, '2023-08-20 19:00:00', '2023-08-20 21:00:00', 800.00, 1199.00, 4),
(17, 6, 3, 4, '2023-04-12 19:00:00', '2023-04-12 21:00:00', 800.00, 1199.00, 3),
(18, 6, 5, 10, '2023-06-25 09:00:00', '2023-06-25 15:00:00', 250.00, NULL, 1),
(19, 6, 16, 13, '2023-06-25 09:00:00', '2023-06-25 16:00:00', 250.00, NULL, 2),
(20, 6, 5, 18, '2023-06-06 09:00:00', '2023-06-25 13:00:00', 150.00, NULL, 2);

CREATE TABLE Booking(
	PNR VARCHAR(20),
	travel_id INT,
	seat_number INT NOT NULL,
	traveler_id INT,
    seat_type ENUM( 'business', 'regular', 'random' ) NOT NULL DEFAULT 'regular',
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
('PLANE120', 4, 53, 7, 'regular'),
('PLANE122', 4, 17, 9, 'regular'),
('PLANE123', 4, 4, 10, 'business'),
('PLANE130', 10, 6, 7, 'business'),
('PLANE132', 10, 21, 9, 'regular'),
('PLANE133', 10, 27, 10, 'regular'),
('PLANE134', 10, 24, 11, 'regular'),
('PLANE140', 17, 32, 7, 'regular'),
('PLANE142', 17, 29, 9, 'regular'),
('PLANE143', 17, 30, 10, 'regular'),
('PLANE144', 17, 30, 11, 'regular'),
('BUS101', 5, 12, 9, 'regular'),
('BUS103', 5, 20, 7, 'regular'),
('BUS104', 5, 23, 10, 'regular'),
('BUSFULL1', 18, 1, 7, 'regular'),
('BUSFULL2', 18, 1, 7, 'regular'),
('BUSFULL3', 18, 1, 7, 'regular'),
('BUSFULL4', 18, 1, 7, 'regular'),
('BUSFULL5', 18, 1, 7, 'regular'),
('BUSFULL6', 18, 1, 7, 'regular'),
('BUSFULL7', 18, 1, 7, 'regular'),
('BUSFULL8', 18, 1, 7, 'regular'),
('BUSFULL9', 18, 1, 7, 'regular'),
('BUSFULL10', 18, 1, 7, 'regular'),
('BUSFULL11', 18, 1, 7, 'regular'),
('BUSFULL12', 18, 1, 7, 'regular'),
('BUSFULL13', 18, 1, 7, 'regular'),
('BUSFULL14', 18, 1, 7, 'regular'),
('BUSFULL15', 18, 1, 7, 'regular'),
('BUSFULL16', 18, 1, 7, 'regular'),
('BUSFULL17', 18, 1, 7, 'regular'),
('BUSFULL18', 18, 1, 7, 'regular'),
('BUSFULL19', 18, 1, 7, 'regular'),
('BUSFULL20', 18, 1, 7, 'regular'),
('BUSFULL21', 18, 1, 7, 'regular'),
('BUSFULL22', 18, 1, 7, 'regular'),
('BUSFULL23', 18, 1, 7, 'regular'),
('BUSFULL24', 18, 1, 7, 'regular'),
('BUSFULL25', 18, 1, 7, 'regular'),
('BUSFULL26', 18, 1, 7, 'regular'),
('BUSFULL27', 18, 1, 7, 'regular'),
('BUSFULL28', 18, 1, 7, 'regular'),
('BUSFULL29', 18, 1, 7, 'regular'),
('BUSFULL30', 18, 1, 7, 'regular'),
('BUSFULL31', 18, 1, 7, 'regular'),
('BUSFULL32', 18, 1, 7, 'regular'),
('BUSFULL33', 18, 1, 7, 'regular'),
('BUSFULL34', 18, 1, 7, 'regular'),
('BUSFULL35', 18, 1, 7, 'regular'),
('BUSFULL36', 18, 1, 7, 'regular'),
('BUSFULL37', 18, 1, 7, 'regular'),
('BUSFULL38', 18, 1, 7, 'regular'),
('BUSFULL39', 18, 1, 7, 'regular'),
('BUSFULL40', 18, 1, 7, 'regular'),
('BUSFULL41', 18, 1, 7, 'regular'),
('BUSFULL42', 18, 1, 7, 'regular'),
('BUSFULL43', 18, 1, 7, 'regular'),
('BUSFULL44', 18, 1, 7, 'regular'),
('BUSFULL45', 18, 1, 7, 'regular'),
('BUSFULL46', 18, 1, 7, 'regular'),
('BUSFULL47', 18, 1, 7, 'regular'),
('BUSFULL48', 18, 1, 7, 'regular'),
('BUSFULL49', 18, 1, 7, 'regular'),
('BUSFULL50', 18, 1, 7, 'regular');

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
('PLANE120', '2023-05-01 21:00:00', 'creadit card', 900.00, NULL),
('PLANE122', '2023-05-01 21:00:00', 'creadit card', 900.00, NULL),
('PLANE123', '2023-05-01 21:00:00', 'creadit card', 1299.00, NULL),
('PLANE130', '2023-05-01 21:00:00', 'creadit card', 1299.00, NULL),
('PLANE132', '2023-05-01 21:00:00', 'creadit card', 900.00, NULL),
('PLANE133', '2023-05-01 21:00:00', 'creadit card', 900.00, NULL),
('PLANE134', '2023-05-01 20:00:00', 'creadit card', 900.00, NULL),
('PLANE140', '2023-05-01 21:00:00', 'creadit card', 800.00, NULL),
('PLANE142', '2023-05-01 21:00:00', 'creadit card', 800.00, NULL),
('PLANE143', '2023-05-01 21:00:00', 'creadit card', 800.00, NULL),
('PLANE144', '2023-05-01 20:00:00', 'creadit card', 800.00, NULL),
('BUS103', '2023-05-10 23:30:00', 'creadit card', 299.00, NULL),
('BUS104', '2023-05-10 21:30:00', 'creadit card', 270.00, 1);


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

INSERT INTO Review ( travel_id, traveler_id, comment, rating) VALUES
(4, 7, "I had an amazing travel experience with your company! The accommodations were top-notch, the tour guides were knowledgeable, and the itinerary was perfectly planned. Highly recommended!", 5),
(4, 8, "The travel arrangements were flawless. From the moment we landed, everything was taken care of. The hotels were fantastic, and the sightseeing tours were unforgettable. Thank you for a wonderful trip!", 5),
(4, 9, "I was blown away by the breathtaking landscapes and cultural experiences during the travel. The local cuisine was incredible, and the activities offered were diverse and exciting. Can't wait to travel with you again!", 5),
(4, 10, "While the destinations were beautiful, I found the accommodations to be average at best. The hotel rooms were small and lacked basic amenities. Improvement is needed in this area.", 3),
(10, 7, "The travel itinerary was too rushed, leaving little time to fully appreciate each location. It felt like we were constantly on the move. More time for relaxation and exploration would have been appreciated.", 4),
(10, 8, "I expected better organization during the trip. There were delays in transportation, and some of the tour guides seemed unprepared. It negatively impacted the overall experience.", 3),
(10, 9, "The transportation arrangements were a nightmare. We experienced multiple cancellations and delays, resulting in missed connections and a disrupted itinerary. It was a frustrating and exhausting travel experience.", 1),
(10, 10, "The customer service was appalling. Our concerns and complaints were dismissed or ignored, and there was no effort to rectify the issues we faced. It was a complete lack of professionalism and care.", 2),
(17, 7, "The pricing of the travel package seemed reasonable at first, but there were many hidden costs along the way. It would have been helpful to have a clearer breakdown of expenses upfront.", 3),
(17, 8, "The travel exceeded my expectations in every way. The attention to detail, the friendly staff, and the unique experiences made it a truly memorable journey. I would choose your company again without hesitation.", 5),
(17, 9, "I had an incredible travel experience with your company. The accommodations were top-notch, with comfortable rooms and friendly staff. The itinerary was well-planned, and we got to visit breathtaking destinations.", 4),
(17, 10, "The pricing of the travel package seemed reasonable at first, but there were many hidden costs along the way. It would have been helpful to have a clearer breakdown of expenses upfront.", 3);


/* 
********************
***** Views ******** 
********************
*/ 

CREATE VIEW company_traveler_info_view AS
SELECT TCK, name, surname, age, email, phone
FROM User JOIN Traveler ON User.id = Traveler.id;

/*
travle_with_vehicle_detail_view is for obtaining detail
information about both travel and vehicle
*/ 
CREATE VIEW travel_with_vehicle_detail_view AS
SELECT *
FROM Travel T
JOIN Vehicle_Type V ON V.id = T.vehicle_type_id;

/*
travel_detail_view is for obtaining detail
information about both travel, terminal and vehicle
*/ 
CREATE VIEW travel_detail_view AS
SELECT
T.travel_id AS travel_id,
T.travel_company_id AS travel_company_id,
T.depart_time AS depart_time,
T.arrive_time AS arrival_time,
T.price AS price,
T.business_price AS business_price,
Dep.name AS departure_terminal_name,
Dep.city AS departure_city,
Ar.name AS arrival_terminal_name,
Ar.city AS arrival_city,
V.model AS vehicle_model,
V.type AS vehicle_type
FROM Travel T
JOIN Terminal Dep ON T.departure_terminal_id = Dep.terminal_id
JOIN Terminal Ar ON T.arrival_terminal_id = Ar.terminal_id
JOIN Vehicle_Type V ON V.id = T.vehicle_type_id;

/*
companies_travels_detail_view is for obtaining detail
information about travel of a company
*/ 
CREATE VIEW companies_travels_detail_view AS
SELECT
C.id AS company_id,
C.company_name AS company_name,
TDW.travel_id AS travel_id,
TDW.depart_time AS depart_time,
TDW.arrival_time AS arrival_time,
TDW.price AS price,
TDW.business_price AS business_price,
TDW.departure_terminal_name AS departure_terminal_name,
TDW.departure_city AS departure_city,
TDW.arrival_terminal_name AS arrival_terminal_name,
TDW.arrival_city AS arrival_city,
TDW.vehicle_model AS vehicle_model,
TDW.vehicle_type AS vehicle_type
FROM Company C 
JOIN travel_detail_view TDW ON C.id = TDW.travel_company_id;

