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

INSERT INTO BookCopy VALUES ('EF.100.101', 0,'in');

INSERT INTO BookCopy VALUES ('EF.100.101',1,'in');

INSERT INTO BookCopy VALUES ('EF.100.101',2,'in');

INSERT INTO HasSubject VALUES ('EF.100.101','Tutorial');

INSERT INTO Book VALUES ('SW.1.102','1234567890002','Asian food for Lunches','Shibo Weng','Moms Publishing Agency', 2013);

INSERT INTO BookCopy VALUES ('SW.1.102', 0, 'in');

INSERT INTO HasSubject VALUES ('SW.1.102','Tutorial');

INSERT INTO Book VALUES ('WW.5.11','1234567890003','How to be a jinja ninja','Wilson Wong','Dynasty Pub', 1980);

INSERT INTO BookCopy VALUES ('WW.5.11', 0, 'in');

INSERT INTO HasSubject VALUES ('WW.5.11','Tutorial');

INSERT INTO Book VALUES ('SMW.25.321','145324635756462','How to get rid of squirrel','S.M. Weng','W.W. Enterprise', 1922);

INSERT INTO BookCopy VALUES ('SMW.25.321', 0, 'in');

INSERT INTO BookCopy VALUES ('SMW.25.321', 1, 'in');

INSERT INTO BookCopy VALUES ('SMW.25.321', 2, 'in');

INSERT INTO BookCopy VALUES ('SMW.25.321', 3, 'in');

INSERT INTO HasSubject VALUES ('SMW.25.321','Tutorial');

INSERT INTO Book VALUES ('CD.45.098','125062783959823','Demon Tale','Cory Dong','YOLO SWEG PUB', 1922);

INSERT INTO BookCopy VALUES ('CD.45.098', 0, 'in');

INSERT INTO Borrowing VALUES ('00000009','CD.45.098',0,'2012-01-01', '2012-01-31');

INSERT INTO Fine VALUES (100,'2012-01-31','0000-00-00',1);

INSERT INTO HasSubject VALUES ('CD.45.098','Fiction, Horror, Suspence');

INSERT INTO Book VALUES ('FG.235.331','34576654355678765','Greek Methology Analysis','Flora Gay','Standford Publishing', 1922);

INSERT INTO BookCopy VALUES ('FG.235.331', 0, 'in');

INSERT INTO Borrowing VALUES ('00000004','FG.235.331',0,'2012-01-02', '2012-01-31');

INSERT INTO Fine VALUES (101,'2012-01-31','2012-02-31',2);

INSERT INTO BookCopy VALUES ('FG.235.331', 2, 'on hold');

INSERT INTO HoldRequest VALUES ('00000001', '00000009', 'FG.235.331', '2001-01-08');

INSERT INTO BookCopy VALUES ('FG.235.331', 1, 'on hold');

INSERT INTO HoldRequest VALUES ('00000002', '00000008', 'FG.235.331', '2001-01-08');

INSERT INTO HasSubject VALUES ('FG.235.331','Non-Fiction, History, Scholar');

INSERT INTO Book VALUES ('EH.825.321','954567876545677','Secret of the MIA','Evan Howard','Yub''s publishing', 1800);

INSERT INTO BookCopy VALUES ('EH.825.321', 1, 'on hold');

INSERT INTO HoldRequest VALUES ('00000003', '00000007', 'EH.825.321', '2001-01-08');

INSERT INTO BookCopy VALUES ('EH.825.321', 3, 'in');

INSERT INTO BookCopy VALUES ('EH.825.321', 2, 'in');

INSERT INTO Borrowing VALUES ('00000002','EH.825.321',2,'2012-01-03', '2012-01-31');

INSERT INTO Fine VALUES (103,'2012-01-31','2012-02-31',3);

INSERT INTO BookCopy VALUES ('EH.825.321', 0, 'on hold');

INSERT INTO HoldRequest VALUES ('00000004', '00000006', 'EH.825.321', '2001-01-08');

INSERT INTO HasSubject VALUES ('EH.825.321','Non-Fiction, History, Suspence');

INSERT INTO Book VALUES ('JKR.235.3781','457898765678','Wilson''s Master Plan','J.K.R.','KING PUB.', 1967);

INSERT INTO BookCopy VALUES ('JKR.235.3781', 1, 'in');

INSERT INTO BookCopy VALUES ('JKR.235.3781', 0, 'on hold');

INSERT INTO HoldRequest VALUES ('00000005', '00000005', 'JKR.235.3781', '2001-01-08');

INSERT INTO HasSubject VALUES ('JKR.235.3781','Fiction, Humor, Suspence');

INSERT INTO Book VALUES ('WG.58.351','985457876','Woman''s Backdoor','E. Gordan','P.E.R. Publishing', 1978);

INSERT INTO BookCopy VALUES ('WG.58.351', 1, 'out');

INSERT INTO Borrowing VALUES ('00000001','WG.58.351',1,'2012-01-04', '0000-00-00');

INSERT INTO BookCopy VALUES ('WG.58.351', 0, 'out');

INSERT INTO Borrowing VALUES ('00000005','WG.58.351',0,'2012-01-11', '0000-00-00');

INSERT INTO BookCopy VALUES ('WG.58.351', 2, 'out');

INSERT INTO Borrowing VALUES ('00000006','WG.58.351',2,'2012-01-13', '0000-00-00');

INSERT INTO BookCopy VALUES ('WG.58.351', 3, 'out');

INSERT INTO Borrowing VALUES ('00000002','WG.58.351',3,'2012-01-12', '0000-00-00');

INSERT INTO BookCopy VALUES ('WG.58.351', 4, 'out');

INSERT INTO Borrowing VALUES ('00000003','WG.58.351',4,'2012-01-14', '0000-00-00');

INSERT INTO BookCopy VALUES ('WG.58.351', 5, 'on hold');

INSERT INTO HoldRequest VALUES ('00000006', '00000004', 'WG.58.351', '2001-01-08');

INSERT INTO BookCopy VALUES ('WG.58.351', 6, 'on hold');

INSERT INTO HoldRequest VALUES ('00000007', '00000006', 'WG.58.351', '2001-01-08');

INSERT INTO BookCopy VALUES ('WG.58.351', 7, 'on hold');

INSERT INTO HoldRequest VALUES ('00000008', '00000007', 'WG.58.351', '2001-01-08');

INSERT INTO BookCopy VALUES ('WG.58.351', 8, 'on hold');

INSERT INTO HoldRequest VALUES ('00000009', '00000008', 'WG.58.351', '2001-01-08');

INSERT INTO BookCopy VALUES ('WG.58.351', 9, 'on hold');

INSERT INTO HoldRequest VALUES ('00000010', '00000009', 'WG.58.351', '2001-01-08');

INSERT INTO BookCopy VALUES ('WG.58.351', 10, 'on hold');

INSERT INTO HoldRequest VALUES ('00000011', '00000010', 'WG.58.351', '2001-01-08');

INSERT INTO BookCopy VALUES ('WG.58.351', 11, 'on hold');

INSERT INTO HoldRequest VALUES ('00000012', '00000005', 'WG.58.351', '2001-01-10');

INSERT INTO HasSubject VALUES ('WG.58.351','Fiction, Adult, Humor');

INSERT INTO Book VALUES ('DG.487.339','987654567876','History of Trolls','Dan Gin','Dongle Printing', 1948);

INSERT INTO BookCopy VALUES ('DG.487.339', 0, 'out');

INSERT INTO Borrowing VALUES ('00000007','DG.487.339',0,'2012-01-17', '0000-00-00');

INSERT INTO HasSubject VALUES ('DG.487.339','Non-fiction, History, Humor, Scholar');

INSERT INTO Book VALUES ('QE.85.361','954345678754345','The Shaking Car','Quennie Eng','Oklahoma Printing', 2013);

INSERT INTO BookCopy VALUES ('QE.85.361', 0, 'in');

INSERT INTO HasSubject VALUES ('KK.45.391','Adult, Horror, Ficion');

INSERT INTO Book VALUES ('KK.45.391','87654347876545','The Root of Fried Chicken','Ku Klutch','Peiking Publishing', 1599);

INSERT INTO BookCopy VALUES ('KK.45.391', 0, 'on hold');

INSERT INTO HoldRequest VALUES ('00000013', '00000005', 'KK.45.391', '2001-01-09');

INSERT INTO HasSubject VALUES ('KK.45.391','Non-fiction, Food, History');

INSERT INTO Book VALUES ('PP.33.324','8465456764564','Build a Putty World','Peter Putt','Evan''s Publishig', 1007);

INSERT INTO BookCopy VALUES ('PP.33.324', 0, 'in');

INSERT INTO HasSubject VALUES ('PP.33.324','Non-fiction, Tutorial, Crafting');



