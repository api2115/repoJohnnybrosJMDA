SELECT COUNT(*) AS numberOfClients, SUM(amount) AS moneyPaid from payments
WHERE YEAR(paymentDate) = 2005 and MONTH(paymentDate) = 5;