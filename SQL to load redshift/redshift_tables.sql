
CREATE TABLE dim_airline(
    airline_id INT,
    airline_name VARCHAR(50)
);

CREATE TABLE dim_airport(
    airport_code VARCHAR(10),
    airport_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50)
);

CREATE TABLE dim_date(
    date_id INT,
    year INT,
    month INT,
    day INT
);

CREATE TABLE fact_flights(
    flight_id INT,
    airline_id INT,
    origin_airport VARCHAR(10),
    destination_airport VARCHAR(10),
    departure_delay INT,
    arrival_delay INT,
    distance INT,
    flight_date DATE
);
