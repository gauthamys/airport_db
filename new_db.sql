drop database airport_db;
create database airport_db;

drop user atc;
drop user scheduler;
drop user luggage_team;
drop user transport;
drop user security;
drop user service;
drop user agency;

\c airport_db

CREATE TABLE Gates
(	GateNo INT NOT NULL,
	Gatelocation VARCHAR NOT NULL,
	PRIMARY KEY (GateNo)
 );

CREATE TABLE Crew
(	id INT NOT NULL,
	Fname VARCHAR(15) NOT NULL,
	Lname VARCHAR(15) NOT NULL,
	Age INT NOT NULL,
	SSN INT NOT NULL,
	Gender CHAR NOT NULL,
	GateNo INT NOT NULL,
	Dept VARCHAR(20) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (GateNo) REFERENCES GATES(GateNo)
	ON DELETE CASCADE
 );

CREATE TABLE Hangar
(	h_id INT NOT NULL,
	h_loc VARCHAR NOT NULL,
	PRIMARY KEY (h_id)
 );

CREATE TABLE Airline
(	Airline_id INT NOT NULL,
	AName VARCHAR(20) NOT NULL,
	PRIMARY KEY (Airline_id)
 );

CREATE TABLE Flight
(	Flight_id INT NOT NULL,
	No_of_Seats INT NOT NULL,
	Destination VARCHAR(20),
	Airline_id INT NOT NULL,
	GateNo INT NOT NULL,
	Boarding_Date DATE NOT NULL,
	Boarding_time VARCHAR(8) NOT NULL,
	PRIMARY KEY (Flight_id),
	FOREIGN KEY (Airline_id) REFERENCES AIRLINE(Airline_id)
	ON DELETE CASCADE,
	FOREIGN KEY (GateNo) REFERENCES GATES(GateNo)
	ON DELETE CASCADE	
 );


CREATE TABLE Passenger
(	SSN INT NOT NULL,
	Firstnm VARCHAR(15) NOT NULL,
	Lastnm VARCHAR(15) NOT NULL,
	Phone INT NOT NULL, 
	Email VARCHAR(20),
	Gender CHAR NOT NULL,
	Age INT NOT NULL,
	Class VARCHAR(19) NOT NULL,
	Seat_No VARCHAR(8),
	Flight_id INT NOT NULL,
	PRIMARY KEY (SSN),
	FOREIGN KEY (Flight_id) REFERENCES FLIGHT(Flight_id)
	ON DELETE CASCADE
 );


CREATE TABLE Luggage
(	l_id INT NOT NULL,
	Pass_SSN INT NOT NULL,
	picked BOOLEAN NOT NULL,
	PRIMARY KEY (l_id),
	FOREIGN KEY (Pass_SSN) REFERENCES PASSENGER(SSN) 
	ON DELETE CASCADE
 );

CREATE TABLE Runway
(	R_id INT NOT NULL,
	Length INT NOT NULL,
	PRIMARY KEY (R_id)
 );


CREATE TABLE Pilot
(	Pid INT NOT NULL,
	Fname VARCHAR(15) NOT NULL,
	Lname VARCHAR(15) NOT NULL,
	Age INT NOT NULL,
	PSSN INT NOT NULL,
	Gender CHAR(2) NOT NULL,
	Salary DECIMAL(10,2),
	Status VARCHAR, 
	Airline_id INT,
	Flight_id INT,
	PRIMARY KEY (Pid,PSSN),
	FOREIGN KEY (Airline_id) REFERENCES AIRLINE(Airline_id)
	ON DELETE CASCADE,
	FOREIGN KEY (Flight_id) REFERENCES FLIGHT(Flight_id)
	ON DELETE CASCADE
 );

CREATE TABLE Plane
(	Tail_id INT NOT NULL,
	Manufacturer VARCHAR(15) NOT NULL,
	Serviced_last DATE,
	h_id INT NOT NULL,
	Airline_id INT NOT NULL,
	PRIMARY KEY (Tail_id),
	FOREIGN KEY (Airline_id) REFERENCES AIRLINE(Airline_id)
	ON DELETE CASCADE,
	FOREIGN KEY (h_id) REFERENCES HANGAR(h_id)
	ON DELETE CASCADE
 );

CREATE TABLE Runs_on
(	Runway_id INT NOT NULL,
	Flight_id INT NOT NULL,
	PRIMARY KEY (Runway_id,Flight_id),
	FOREIGN KEY (Flight_id) REFERENCES FLIGHT(Flight_id)
	ON DELETE CASCADE,
	FOREIGN KEY (Runway_id) REFERENCES RUNWAY(R_id)
	ON DELETE CASCADE
 );
CREATE TABLE Managed_by
(	id INT NOT NULL,
	Gate_No INT NOT NULL,
	PRIMARY KEY (id,Gate_No),
	FOREIGN KEY (id) REFERENCES CREW(id)
	ON DELETE CASCADE,
	FOREIGN KEY (Gate_No) REFERENCES GATES(GateNo)
	ON DELETE CASCADE
 );

create user security with password 'security';
grant select on passenger to security;

create user agency with password 'agency';
grant insert, select on flight to agency;

create user atc with password 'atc';
grant select, insert, update on flight, runway, runs_on, airline to atc;

create user scheduler with password 'scheduler';
grant select, insert, update on flight to scheduler;
grant select on airline, runs_on to scheduler;

create user luggage_team with password 'luggage_team';
grant select, update, insert on luggage to luggage_team;
grant select (ssn, flight_id, firstnm, lastnm, phone, email) on passenger to luggage_team;

create user transport with password 'transport';
grant select (gateno) on flight to transport;
grant select on gates to transport;

create user service with password 'service';
grant update (h_id) on plane to service;
grant select on hangar to service;

grant select on flight, airline to all users;

INSERT INTO Gates values(1,'46.64061,83.10566');
INSERT INTO Gates values(2,'-84.86056,-23.70278');
INSERT INTO Gates values(3,'52.66045,-123.43637');
INSERT INTO Gates values(4,'-12.47648,83.10566');
INSERT INTO Gates values(5,'46.64061,-12.47648');
INSERT INTO Gates values(6,'46.64031,83.20566');
INSERT INTO Gates values(7,'46.64011,83.20566');
INSERT INTO Gates values(8,'46.64061,83.30566');

INSERT INTO Crew values(1,'Aditi', 'Kim', 39, 1234,'F',1, 'Ground');
INSERT INTO Crew values(2,'Prajakta', 'Son', 48, 2341,'F',2, 'Service');
INSERT INTO Crew values(3,'Shobha', 'Apartment', 34, 1234,'F',1, 'Security Team');
INSERT INTO Crew values(4,'Duc', 'Duong', 45, 3421,'M',1, 'Operations');
INSERT INTO Crew values(5,'Shalini', 'Park', 31, 3214,'F',3, 'Ground');
INSERT INTO Crew values(6,'Reemya', 'Pim', 34, 6969,'F',4, 'Ground');
INSERT INTO Crew values(7,'Sachuth', 'Mos', 21, 4444,'M',5, 'Service');
INSERT INTO Crew values(8,'Aditi', 'Jagannath', 29, 4532,'F',8, 'Ground');
INSERT INTO Crew values(9,'India', 'Flower', 34, 1234,'F',6, 'Security Team');
INSERT INTO Crew values(10,'Mary', 'Jean', 24, 2234,'F',2, 'Security Team');
INSERT INTO Crew values(11,'Peter', 'Prabhakar', 34, 1134,'F',3, 'Operations');
INSERT INTO Crew values(12,'Tony', 'Satark', 34, 1236,'F',1, 'Service');
INSERT INTO Crew values(13,'Bruce', 'Bannerji', 34, 1224,'F',8, 'Service');
INSERT INTO Crew values(14,'Suas', 'Peddol', 34, 1233,'F',6, 'Ground');
INSERT INTO Crew values(15,'Jay', 'Vroon', 34, 1264,'F',3, 'Security Team');

INSERT INTO Hangar values(1,'leftgate');
INSERT INTO Hangar values(2,'leftgate');
INSERT INTO Hangar values(3,'rightgate');
INSERT INTO Hangar values(4,'rightgate');
INSERT INTO Hangar values(5,'rightgate');
INSERT INTO Hangar values(6,'central');
INSERT INTO Hangar values(7,'central');
INSERT INTO Hangar values(8,'central');
INSERT INTO Hangar values(9,'rightgate');
INSERT INTO Hangar values(10,'rightgate');
INSERT INTO Hangar values(11,'central');
INSERT INTO Hangar values(12,'central');
INSERT INTO Hangar values(13,'leftgate');
INSERT INTO Hangar values(14,'leftgate');
INSERT INTO Hangar values(15,'leftgate');

INSERT INTO Airline values(1,'JetAirways');
INSERT INTO Airline values(2,'Indigo');
INSERT INTO Airline values(3,'AirIndia');
INSERT INTO Airline values(4,'Lufthansa');
INSERT INTO Airline values(5,'Kingfisher');
INSERT INTO Airline values(6, 'AirCanada');
INSERT INTO Airline values(7,'AirUK');
INSERT INTO Airline values(8,'AirCanada');
INSERT INTO Airline values(9,'AirFrance');
INSERT INTO Airline values(10,'Vistara');
INSERT INTO Airline values(11,'TruJet');
INSERT INTO Airline values(12,'Alliance Air');
INSERT INTO Airline values(13,'Go Air');
INSERT INTO Airline values(14,'Qatar Airways');
INSERT INTO Airline values(15, 'SpiceJet');

INSERT INTO Flight values(123456789, 60, 'Pondicherry', 1, 1, '01-01-2022','23:00:00');
INSERT INTO Flight values(112211221, 120, 'Delhi', 1, 2, '9-12-2021', '00:00:00');
INSERT INTO Flight values(221122112, 80, 'Mumbai', 2, 1, '8-12-2021', '9:30:00');
INSERT INTO Flight values(334433443, 90, 'San Francisco', 2, 2, '2-2-2022', '2:00:00');
INSERT INTO Flight values(556655665, 100, 'Asgard', 7, 7, '26-11-2021', '16:00:00');
INSERT INTO Flight values(778877887, 70, 'New York', 8, 8, '27-11-2021', '4:00:00');
INSERT INTO Flight values(987654321, 50, 'Kolkata', 4, 1, '28-11-2021', '17:00:00');
INSERT INTO Flight values(111111111, 60, 'Indore', 1, 1, '26-11-2021', '23:00:00');
INSERT INTO Flight values(222222222, 70, 'Rome', 3, 2, '27-11-2021', '20:00:00');
INSERT INTO Flight values(333333333, 80, 'Bengaluru', 8, 6, '31-12-2021', '17:00:00');
INSERT INTO Flight values(444444444, 90, 'Chennai', 5, 4, '28-12-2021', '3:00:00');
INSERT INTO Flight values(555555555, 80, 'Dubai', 6, 5, '9-12-2021', '14:00:00');

INSERT INTO Passenger values(11111111, 'Gokul','Raj',99112345,'gokul@gmail.com','M',22,'First',12,123456789);
INSERT INTO Passenger values(11111112, 'Gauri','Ram',99112345,'gauri@gmail.com','F',23,'Business',4,112211221);
INSERT INTO Passenger values(11111113, 'Manju','CN',99122343,'manju@gmail.com','M',22,'Coach',34,123456789);
INSERT INTO Passenger values(11111114, 'Marshall','Mathews',91234521,'gokul@gmail.com','M',22,'Coach',12,555555555);
INSERT INTO Passenger values(11111115, 'Jake','Peralta',99114523,'peralta@gmail.com','M',22,'First',60,444444444);
INSERT INTO Passenger values(11111116, 'Saloni','Srinivas',9114521,'salsri@gmail.com','F',22,'Business',70,123456789);
INSERT INTO Passenger values(11111117, 'Shyam','Raj',99112321,'shyam@gmail.com','M',22,'First',12,123456789);
INSERT INTO Passenger values(11111118, 'Malhar','Raj',99134521,'malraj@gmail.com','F',67,'Coach',12,222222222);
INSERT INTO Passenger values(11111119, 'Jim','Halpert',91232345,'jimhal@gmail.com','M',32,'First',12,333333333);
INSERT INTO Passenger values(21111111, 'Pam','Halpert',91234522,'pamhal@gmail.com','F',30,'First',13,333333333);
INSERT INTO Passenger values(31111111, 'Andy','Bernard',98793001,'andybern@gmail.com','M',45,'First',14,333333333);
INSERT INTO Passenger values(41111111, 'Stanley','Hudson',99134521,'stan@gmail.com','M',78,'First',15,333333333);
INSERT INTO Passenger values(51111111, 'Creed','Bratton',99234123,'creed@gmail.com','M',92,'First',16,333333333);
INSERT INTO Passenger values(61111111, 'Phyllis','Vance',92234521,'phyll@gmail.com','F',62,'First',17,333333333);


INSERT INTO Luggage values(1,11111111, TRUE);
INSERT INTO Luggage values(2,11111112, FALSE);
INSERT INTO Luggage values(3,11111113, FALSE);
INSERT INTO Luggage values(4,11111114, TRUE);
INSERT INTO Luggage values(5,11111115, TRUE);
INSERT INTO Luggage values(6,11111116, FALSE);
INSERT INTO Luggage values(7,11111117, TRUE);
INSERT INTO Luggage values(8,11111118, FALSE);
INSERT INTO Luggage values(10,11111119, TRUE);
INSERT INTO Luggage values(11,21111111, FALSE);
INSERT INTO Luggage values(12,31111111, FALSE);
INSERT INTO Luggage values(13,41111111, TRUE);
INSERT INTO Luggage values(14,51111111, FALSE);

INSERT INTO Runway values(1,5432);
INSERT INTO Runway values(2,4823);
INSERT INTO Runway values(3,4673);
INSERT INTO Runway values(4,4443);
INSERT INTO Runway values(5,4543);

INSERT INTO Pilot values(1,'John','Smith',35,16751501,'M',54000,'Captain',1,123456789);
INSERT INTO Pilot values(2,'Loren','Zecchi',34,16751502,'F',670000,'First Officer',1,334433443);
INSERT INTO Pilot values(3,'Lisa','Eumbery',46,16751503,'F',570000,'Captain',1,556655665);
INSERT INTO Pilot values(4,'Kunes','Coote',29,16751504,'M',560000,'First Officer',1,987654321);
INSERT INTO Pilot values(5,'Benji','Mckerie',31,16751505,'M',56000,'First Officer',1,222222222);
INSERT INTO Pilot values(6,'Oswald','Yancey',37,16751506,'M',1050000,'Captain',1,778877887);
INSERT INTO Pilot values(7,'ALexis','Lore',39,16751507,'F',90000,'Captain',1,222222222);

INSERT INTO Plane values(12345, 'Airbus', '2021-09-01', 1, 2);
INSERT INTO Plane values(10345, 'Boeing', '2021-06-10', 1, 2);
INSERT INTO Plane values(12845, 'Embraer', '2021-09-12', 1, 2);
INSERT INTO Plane values(11345, 'Airbus', '2021-02-24', 1, 2);
INSERT INTO Plane values(17645, 'Boeing', '2020-09-01', 1, 2);
INSERT INTO Plane values(12840, 'Bombardier', '2020-12-01', 1, 2);
INSERT INTO Plane values(10045, 'Embraer', '2021-06-07', 1, 2);
INSERT INTO Plane values(19915, 'Airbus', '2020-09-01', 1, 2);
INSERT INTO Plane values(13325, 'Boeing', '2021-05-11', 1, 2);

INSERT INTO Runs_on values(1,112211221);
INSERT INTO Runs_on values(2,221122112);
INSERT INTO Runs_on values(3,778877887);
INSERT INTO Runs_on values(4,334433443);
INSERT INTO Runs_on values(5,555555555);

INSERT INTO Managed_by values(2,1);
INSERT INTO Managed_by values(3,4);
INSERT INTO Managed_by values(1,5);
INSERT INTO Managed_by values(4,2);
INSERT INTO Managed_by values(6,3);
INSERT INTO Managed_by values(5,6);
INSERT INTO Managed_by values(7,7);
