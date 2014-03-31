INSERT INTO BorrowerType VALUES ('student',2);
    
INSERT INTO BorrowerType VALUES ('faculty',12);

INSERT INTO BorrowerType VALUES ('staff',6);

INSERT INTO Borrower (bid,password,name,address,phone,emailAddress,sinOrStNo,expiryDate,type) 
VALUES ('00000000','1234','Shibo Weng','1 Library Road','2509052422','sweng@lib.ubc.ca','000000001','June 4 2014','student');

INSERT INTO Borrower (bid,password,name,address,phone,emailAddress,sinOrStNo,expiryDate,type) VALUES ('00000001','1234','Evan Friday','2 Library Road','2509052422','efriday@lib.ubc.ca','000000002','June 4 2014','student');

INSERT INTO Borrower (bid,password,name,address,phone,emailAddress,sinOrStNo,expiryDate,type) VALUES ('00000003','1234','Wilson Wong','Library Road','2509052422','wwong@lib.ubc.ca','000000003','June 4 2014','faculty');

INSERT INTO Borrower (bid,password,name,address,phone,emailAddress,sinOrStNo,expiryDate,type) VALUES ('00000004','1234','Beyonce Knowles','Library Road','2509052422','bknowles@lib.ubc.ca','000000004','June 4 2014','staff');

INSERT INTO Borrower (bid,password,name,address,phone,emailAddress,sinOrStNo,expiryDate,type) VALUES ('00000005','1234','Johnny Depp','Library Road','2509052422','jdepp@lib.ubc.ca','000000005','June 4 2014','staff');

INSERT INTO Book,BookCopy (callNumber,ISBN,title,mainAuthor,publisher,year,copyNo) VALUES ('EF.100.101','1234567890001','Learning Python','Evan Friday','Compsci Ltd.',2014, 0,'in');

INSERT INTO BookCopy (callNumber,copyNo,status) VALUES ('EF.100.101',1,'in');

INSERT INTO BookCopy (callNumber,copyNo,status) VALUES ('EF.100.101',2,'in');

INSERT INTO Book,BookCopy (callNumber,ISBN,title,mainAuthor,publisher,year,copyNo) VALUES ('SW.1.102','1234567890002','Asian food for Lunches','Shibo Weng','Moms Publishing Agency',2013, 0);

INSERT INTO Book,BookCopy (callNumber,ISBN,title,mainAuthor,publisher,year,copyNo) VALUES ('WW.5.11','1234567890003','How to be a jinja ninja','Wilson Wong','Dynasty Pub',950, 0);

INSERT INTO Borrowing,BookCopy,(borid,bid,callNumber,copyNo,outDate,inDate,status) VALUES ('0','00000001','EF.100.101',0,'March 30th 2014','April 13th 2014','out');

INSERT INTO HoldRequest,Cart(bid,hid,callNumber,issuedDate) VALUES ('00000000','0','SW.1.102','March 30th 2014');
