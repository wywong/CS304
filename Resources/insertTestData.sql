INSERT INTO BorrowerType VALUES ('student',2);

INSERT INTO BorrowerType VALUES ('faculty',12);

INSERT INTO BorrowerType VALUES ('staff',6);

INSERT INTO Borrower VALUES ('00000000','1234','Shibo Weng','1 Library Road','2509052422','sweng@lib.ubc.ca','000000001','2014-06-04','student');

INSERT INTO Borrower VALUES ('00000001','1234','Evan Friday','2 Library Road','2509052422','efriday@lib.ubc.ca','000000002','2013-09-06','student');

INSERT INTO Borrower VALUES ('00000002','1234','Evan Monday','2 Library Road','2509052422','em@lib.ubc.ca','000000002','2013-09-06','student');

INSERT INTO Borrower VALUES ('00000003','1234','Evan Tuesday','2 Library Road','2509052422','et@lib.ubc.ca','000000006','2013-09-06','student');

INSERT INTO Borrower VALUES ('00000004','1234','Evan Wednesday','2 Library Road','2509052422','ew@lib.ubc.ca','000000007','2013-09-06','student');

INSERT INTO Borrower VALUES ('00000005','1234','Evan Thursday','2 Library Road','2509052422','etr@lib.ubc.ca','000000008','2013-09-06','student');

INSERT INTO Borrower VALUES ('00000006','1234','Evan Saturday','2 Library Road','2509052422','esat@lib.ubc.ca','000000009','2013-09-06','student');

INSERT INTO Borrower VALUES ('00000007','1234','Evan Sunday','2 Library Road','2509052422','esun@lib.ubc.ca','000000010','2013-09-06','student');

INSERT INTO Borrower VALUES ('00000008','1234','Evan Everyday','2 Library Road','2509052422','ever@lib.ubc.ca','000000011','2013-09-06','student');

INSERT INTO Borrower VALUES ('00000009','1234','Wilson Wong','Library Road','2509052422','wwong@lib.ubc.ca','000000003','2012-12-12','faculty');

INSERT INTO Borrower VALUES ('00000010','1234','Wilson Wang','Library Road','2509052422','wwang@lib.ubc.ca','000000012','2012-12-12','faculty');

INSERT INTO Borrower VALUES ('00000011','1234','Wilson Weng','Library Road','2509052422','wweng@lib.ubc.ca','000000013','2012-12-12','faculty');

INSERT INTO Borrower VALUES ('00000012','1234','Beyonce Knowles','Library Road','2509052422','bknowles@lib.ubc.ca','000000004','2014-06-11','staff');

INSERT INTO Borrower VALUES ('00000013','1234','Katy Block Parry','Library Road','2509052422','kbp@lib.ubc.ca','000000014','2014-06-11','staff');

INSERT INTO Borrower VALUES ('00000014','1234','Scarlett Johanson','Library Road','2509052422','jh@lib.ubc.ca','000000015','2014-06-11','staff');

INSERT INTO Borrower VALUES ('00000015','1234','Johnny Depp','Library Road','2509052422','jdepp@lib.ubc.ca','000000005','2000-01-08','staff');

INSERT INTO Book VALUES ('EF.100.101','1234567890001','Learning Python','Evan Friday','Compsci Ltd.',2014);

INSERT INTO HasAuthor VALUES ('EF.100.101','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('EF.100.101', 0,'in');

INSERT INTO BookCopy VALUES ('EF.100.101',1,'in');

INSERT INTO BookCopy VALUES ('EF.100.101',2,'in');

INSERT INTO HasSubject VALUES ('EF.100.101','Tutorial');

INSERT INTO Book VALUES ('SW.1.102','1234567890002','Asian food for Lunches','Shibo Weng','Moms Publishing Agency', 2013);

INSERT INTO HasAuthor VALUES ('SW.1.102','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('SW.1.102', 0, 'in');

INSERT INTO HasSubject VALUES ('SW.1.102','Tutorial');

INSERT INTO Book VALUES ('WW.5.11','1234567890003','How to be a jinja ninja','Wilson Wong','Dynasty Pub', 1980);

INSERT INTO HasAuthor VALUES ('WW.5.11','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('WW.5.11', 0, 'in');

INSERT INTO HasSubject VALUES ('WW.5.11','Tutorial');

INSERT INTO Book VALUES ('SMW.25.321','145324635756462','How to get rid of squirrel','S.M. Weng','W.W. Enterprise', 1922);

INSERT INTO HasAuthor VALUES ('SMW.25.321','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('SMW.25.321', 0, 'in');

INSERT INTO BookCopy VALUES ('SMW.25.321', 1, 'in');

INSERT INTO BookCopy VALUES ('SMW.25.321', 2, 'in');

INSERT INTO BookCopy VALUES ('SMW.25.321', 3, 'in');0

INSERT INTO HasSubject VALUES ('SMW.25.321','Tutorial');

INSERT INTO Book VALUES ('CD.45.098','125062783959823','Demon Tale','Cory Dong','YOLO SWEG PUB', 1922);

INSERT INTO HasAuthor VALUES ('CD.45.098','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('CD.45.098', 0, 'in');


INSERT INTO Fine (amount, issuedDate, paidDate, borid) VALUES (100,'2012-01-31','0000-00-00',1);

INSERT INTO HasSubject VALUES ('CD.45.098','Fiction, Horror, Suspense');

INSERT INTO Book VALUES ('FG.235.331','34576654355678765','Greek Methology Analysis','Flora Gay','Standford Publishing', 1922);

INSERT INTO HasAuthor VALUES ('FG.235.331','O.B. Sack');

INSERT INTO BookCopy VALUES ('FG.235.331', 0, 'in');


INSERT INTO Fine (amount, issuedDate, paidDate, borid) VALUES (101,'2012-01-31','2012-02-31',2);

INSERT INTO BookCopy VALUES ('FG.235.331', 2, 'in');


INSERT INTO BookCopy VALUES ('FG.235.331', 1, 'in');


INSERT INTO HasSubject VALUES ('FG.235.331','Non-Fiction, History, Scholar');

INSERT INTO Book VALUES ('EH.825.321','954567876545677','Secret of the MIA','Evan Howard','Yub''s publishing', 1982);

INSERT INTO HasAuthor VALUES ('EH.825.321','O.U.B.');

INSERT INTO BookCopy VALUES ('EH.825.321', 1, 'in');


INSERT INTO BookCopy VALUES ('EH.825.321', 3, 'in');

INSERT INTO BookCopy VALUES ('EH.825.321', 2, 'in');


INSERT INTO Fine (amount, issuedDate, paidDate, borid) VALUES (103,'2012-01-31','2012-02-31',3);

INSERT INTO BookCopy VALUES ('EH.825.321', 0, 'in');


INSERT INTO HasSubject VALUES ('EH.825.321','Non-Fiction, History, Suspense');

INSERT INTO Book VALUES ('JKR.235.3781','457898765678','Wilson''s Master Plan','J.K.R.','KING PUB.', 1967);

INSERT INTO HasAuthor VALUES ('JKR.235.3781','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('JKR.235.3781', 1, 'in');

INSERT INTO BookCopy VALUES ('JKR.235.3781', 0, 'in');


INSERT INTO HasSubject VALUES ('JKR.235.3781','Fiction, Humor, Suspense');

INSERT INTO Book VALUES ('WG.58.351','985457876','Woman''s Backdoor','E. Gordan','P.E.R. Publishing', 1978);

INSERT INTO HasAuthor VALUES ('WG.58.351','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('WG.58.351', 1, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 0, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 2, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 3, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 4, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 5, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 6, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 7, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 8, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 9, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 10, 'in');


INSERT INTO BookCopy VALUES ('WG.58.351', 11, 'in');


INSERT INTO HasSubject VALUES ('WG.58.351','Fiction, Adult, Humor');

INSERT INTO Book VALUES ('DG.487.339','987654567876','History of Trolls','Dan Gin','Dongle Printing', 1948);

INSERT INTO HasAuthor VALUES ('DG.487.339','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('DG.487.339', 0, 'in');


INSERT INTO HasSubject VALUES ('DG.487.339','Non-fiction, History, Humor, Scholar');

INSERT INTO Book VALUES ('QE.85.361','954345678754345','The Shaking Car','Quennie Eng','Oklahoma Printing', 2013);

INSERT INTO HasAuthor VALUES ('QE.85.361','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('QE.85.361', 0, 'in');

INSERT INTO HasSubject VALUES ('QE.85.361','Adult, Horror, Ficion');

INSERT INTO Book VALUES ('KK.45.391','87654347876545','The Root of Fried Chicken','Ku Klutch','Peiking Publishing', 1999);

INSERT INTO HasAuthor VALUES ('KK.45.391','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('KK.45.391', 0, 'in');


INSERT INTO HasSubject VALUES ('KK.45.391','Non-fiction, Food, History');

INSERT INTO Book VALUES ('PP.33.324','8465456764564','Build a Putty World','Peter Putt','Evan''s Publishig', 2011);

INSERT INTO HasAuthor VALUES ('PP.33.324','O.B. Sack, O.U.B.');

INSERT INTO BookCopy VALUES ('PP.33.324', 0, 'in');

INSERT INTO HasSubject VALUES ('PP.33.324','Non-fiction, Tutorial, Crafting');

INSERT INTO Book VALUES ('OG.334.324','846175424564','Build a Putty World','Owen Gateman','Evan''s Publishig', 2011);

INSERT INTO HasAuthor VALUES ('OG.334.324','O.B. Sack, E.B.');

INSERT INTO HasSubject VALUES ('KK.45.391','Non-fiction, Food, History');

INSERT INTO Book VALUES ('TY.333.123','846132714344','Cow World','T. Young','Evan''s Publishig', 2011);

INSERT INTO HasAuthor VALUES ('TY.333.123','O.B. Sack, E.B.');

INSERT INTO HasSubject VALUES ('TY.333.123','Non-fiction, Food, History');

INSERT INTO BookCopy VALUES ('TY.333.123', 0, 'in');


INSERT INTO Book VALUES ('WB.313.234','84652156214','Duck Face Studied','Warner Bowen','Evan''s Publishig', 2011);

INSERT INTO HasAuthor VALUES ('WB.313.234','O.B. Sack, K.B.');

INSERT INTO HasSubject VALUES ('WB.313.234','Non-fiction, Culture, History');

INSERT INTO BookCopy VALUES ('WB.313.234', 0, 'in');


INSERT INTO Book VALUES ('QY.323.389','8466575612314','The Rooster','Qare Young','Evan''s Publishig', 2011);

INSERT INTO HasAuthor VALUES ('QY.323.389','O.B. Sack, K.B.');

INSERT INTO HasSubject VALUES ('QY.323.389','Non-fiction, Food, History');

INSERT INTO BookCopy VALUES ('QY.323.389', 0, 'in');


INSERT INTO Book VALUES ('QQ.393.444','8465654215154','Slayer of the West','Q. Qiu','Evan''s Publishig', 2011);

INSERT INTO HasAuthor VALUES ('QQ.393.444','O.B. Sack, K.B.');

INSERT INTO HasSubject VALUES ('QQ.393.444','Non-fiction, History');

INSERT INTO BookCopy VALUES ('QQ.393.444', 0, 'in');


INSERT INTO Book VALUES ('JK.222.364','8984566455694','Sun Striker','Johnson Kwan','Evan''s Publishig', 2011);

INSERT INTO HasAuthor VALUES ('JK.222.364','O.B. Sack, K.B.');

INSERT INTO HasSubject VALUES ('JK.222.364','Fiction, Adventure');

INSERT INTO BookCopy VALUES ('JK.222.364', 0, 'in');


