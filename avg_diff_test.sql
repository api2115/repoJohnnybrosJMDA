DROP VIEW IF EXISTS `orders_with_price`;

CREATE VIEW orders_with_price
AS
SELECT orders.orderNumber, orders.orderDate, orders.status,
orders.customerNumber as ordersCnumb, payments.customerNumber as paymentsCnumb,
payments.paymentDate, payments.amount from orders
inner JOIN payments on
orders.customerNumber=payments.customerNumber;

select * from orders_with_price;
