DROP VIEW IF EXISTS `ordersWithPrice`;

CREATE VIEW ordersWithPrice
AS
SELECT orderdetails.orderNumber, sum(orderdetails.quantityOrdered*orderdetails.priceEach) as total, 
orders.status
FROM orderdetails
INNER JOIN orders ON orders.orderNumber = orderdetails.orderNumber
WHERE orders.status = "Shipped"
GROUP BY orderdetails.orderNumber;

SELECT * FROM ordersWithPrice;
