SELECT callNumber
FROM Book
WHERE title = desiredTitle

SELECT bid
FROM Borrowing
WHERE callNumber = givenCnum

SELECT title, name
FROM Fine F, Borrowing BG, Book BK, Borrower BR
WHERE F.borid = BG.borid, BG.callNumber = BK.callNumber, BG.bid = BR.bid