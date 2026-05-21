CREATE TABLE users (
  id int PRIMARY KEY AUTO_INCREMENT,
  username varchar(45) NOT NULL,
  password varchar(64) NOT NULL
);

CREATE TABLE zones (
  id int PRIMARY KEY AUTO_INCREMENT,
  name varchar(45)
);

CREATE TABLE chambers (
  id int PRIMARY KEY AUTO_INCREMENT,
  zone_id int NOT NULL,
  clearence_level bit(3),
  FOREIGN KEY (zone_id) REFERENCES zones (id)
);

CREATE TABLE roles (
  id int PRIMARY KEY AUTO_INCREMENT,
  role_name varchar(45),
  role_description varchar(64)
);

CREATE TABLE staff (
  id int PRIMARY KEY AUTO_INCREMENT,
  first_name varchar(45),
  last_name varchar(45),
  clearence_level bit(3),
  user_id int UNIQUE NOT NULL,
  role_id int,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (role_id) REFERENCES roles (id)
);

CREATE TABLE scp_subjects (
  id int PRIMARY KEY AUTO_INCREMENT,
  object_class varchar(15) NOT NULL,
  containment_procedures varchar(1024),
  description varchar(4096),
  chamber_id int,
  assigned_researcher_id int,
  FOREIGN KEY (chamber_id) REFERENCES chambers (id),
  FOREIGN KEY (assigned_researcher_id) REFERENCES staff (id)
);
