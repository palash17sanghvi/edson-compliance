-- Phase 1: Relational Architecture

CREATE TABLE Locations (
    location_id SERIAL PRIMARY KEY,
    branch_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE User_Profiles (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    role VARCHAR(50) CHECK (role IN ('Admin', 'Manager', 'Program_Aide')) NOT NULL,
    assigned_location_id INT REFERENCES Locations(location_id)
);

CREATE TABLE Event_Organizers (
    organizer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    organization_name VARCHAR(150),
    email VARCHAR(150) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Bookings (
    booking_id SERIAL PRIMARY KEY,
    location_id INT REFERENCES Locations(location_id) NOT NULL,
    organizer_id INT REFERENCES Event_Organizers(organizer_id) NOT NULL,
    approved_by INT REFERENCES User_Profiles(user_id),
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Completed'))
);


ALTER TABLE Bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE Bookings FORCE ROW LEVEL SECURITY;

CREATE POLICY rbac_location_access ON Bookings
FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM User_Profiles 
        WHERE user_id = current_setting('app.current_user_id', true)::INT
        AND (assigned_location_id = Bookings.location_id OR assigned_location_id IS NULL)
    )
);