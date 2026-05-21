CREATE DATABASE wordpress;
CREATE USER "wordpress"@"%" IDENTIFIED BY "PressMyWord!";
GRANT ALL PRIVILEGES ON wordpress.* TO "wordpress"@"%";
FLUSH PRIVILEGES;