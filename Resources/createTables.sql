CREATE TABLE IF NOT EXISTS BorrowerType (
  type varchar(10),
  bookTimeLimit varchar(10),
  PRIMARY KEY (type)
);

CREATE TABLE IF NOT EXISTS Borrower (
  bid char(8) NOT NULL,
  password varchar(16) NOT NULL,
  name varchar(40) NOT NULL,
  address varchar(40),
  phone char(10),
  emailAddress varchar(40),
  sinOrStNo varchar(20) NOT NULL,
  expiryDate varchar(10),
  type varchar(10),
  PRIMARY KEY (bid),
  FOREIGN KEY (type) REFERENCES BorrowerType(type)
);

