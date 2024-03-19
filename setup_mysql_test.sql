-- Creates a MYSQL server with:
--  Database hbnb_test_db.
--  User hbnb_test with password hbnb_test_pwd in localhost.
--  Grants all priviledges for hbnb_test on hbnb_test_db.
--  Grants SELECT priviledge for hbnb_test on perfomance.
--  Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
