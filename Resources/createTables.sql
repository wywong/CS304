CREATE TABLE IF NOT EXISTS BorrowerType (
  type varchar(7),
  bookTimeLimit int NOT NULL,
  PRIMARY KEY (type)
);

CREATE TABLE IF NOT EXISTS Borrower (
  bid char(8) NOT NULL,
  password varchar(16) NOT NULL,
  name varchar(40) NOT NULL,
  address varchar(40),
  phone char(10),
  emailAddress varchar(40) NOT NULL,
  sinOrStNo varchar(9) NOT NULL,
  expiryDate varchar(10),
  type varchar(7),
  PRIMARY KEY (bid),
  FOREIGN KEY (type) REFERENCES BorrowerType(type)
);

CREATE TABLE IF NOT EXISTS Book (
  callNumber varchar(40) NOT NULL,
  isbn varchar(40) NOT NULL,
  title varchar(40) NOT NULL,
  mainAuthor varchar(40) NOT NULL,
  publisher varchar(40) NOT NULL,
  year YEAR NOT NULL,
  PRIMARY KEY (callNumber)
);

CREATE TABLE IF NOT EXISTS HasAuthor (
  callNumber varchar(40) NOT NULL,
  name varchar(40) NOT NULL,
  PRIMARY KEY (callNumber),
  FOREIGN KEY (callNumber) REFERENCES Book(callNumber)
);

CREATE TABLE IF NOT EXISTS HasSubject (
  callNumber varchar(40) NOT NULL,
  subject varchar(40) NOT NULL,
  PRIMARY KEY (subject, callNumber),
  FOREIGN KEY (callNumber) REFERENCES Book(callNumber)
);

CREATE TABLE IF NOT EXISTS BookCopy (
  callNumber varchar(40) NOT NULL,
  copyNo int NOT NULL,
  status varchar(7) NOT NULL,
  PRIMARY KEY (copyNo, callNumber),
  FOREIGN KEY (callNumber) REFERENCES Book(callNumber)
);

CREATE TABLE IF NOT EXISTS HoldRequest (
  hid varchar(40) NOT NULL,
  bid char(8) NOT NULL,
  callNumber varchar(40) NOT NULL,
  issuedDate DATE NOT NULL,
  PRIMARY KEY (hid)
);

CREATE TABLE IF NOT EXISTS Borrowing (
  borid varchar(40) NOT NULL,
  bid char(8) NOT NULL,
  callNumber varchar(40) NOT NULL,
  copyNo int NOT NULL,
  outDate DATE NOT NULL,
  inDate DATE NOT NULL,
  PRIMARY KEY (borid)
);

CREATE TABLE IF NOT EXISTS Fine (
  fid varchar(40) NOT NULL,
  amount int NOT NULL,
  issuedDate DATE NOT NULL,
  paidDate DATE NOT NULL,
  borid varchar(40) NOT NULL,
  PRIMARY KEY (fid)
);
