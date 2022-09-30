/*
SQL Script to generate Child Security's db
Includes tables and all related to the functionallity
*/

--We create the db with the charset configuration
CREATE DATABASE child_sec_db-character-set utf8

-- Create a table for users with all the data we're about to manage
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT NOT NULL,
  fecha_reg DATE NOT NULL,
  profile_pic TEXT NOT NULL
);

-- Create a table for gps location records with foreign key to the user associated with all the data we're about to manage
CREATE TABLE locations (
  id INTEGER PRIMARY KEY,
  gps_location TEXT NOT NULL,
  user_id TEXT NOT NULL FOREIGN KEY,
  wearable_id TEXT NOT NULL
);

-- Create a table for registered wearables with foreign key to the user associated with all the data we're about to manage
CREATE TABLE registered_wearables (
  id INTEGER PRIMARY KEY,
  wearable_activation_code TEXT NOT NULL,
  user_id TEXT NOT NULL FOREIGN KEY,
  active_status BOOLEAN NOT NULL
);

-- Select query to read the status value of the insert query
SELECT * FROM students WHERE gender = 'F';