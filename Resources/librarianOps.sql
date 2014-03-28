SELECT title 
FROM book BK, borrowing BG
WHERE BG.callNumber = BK.callNumber
ORDER BY COUNT (BG.callNumber) dec