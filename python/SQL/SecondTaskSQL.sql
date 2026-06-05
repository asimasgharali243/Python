create database if not EXISTS online_store;
use online_store;
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category ENUM('Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Groceries') NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE PROCEDURE insert_products()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 200 DO
        INSERT INTO products (product_name, category, price, stock_quantity)
        VALUES (
            CONCAT('Product ', i),
            ELT(FLOOR(1 + (RAND() * 5)), 'Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Groceries'),
            ROUND(RAND() * 500 + 10, 2),
            FLOOR(RAND() * 500)
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

-- Call procedure
CALL insert_products();

SELECT *,(SELECT count(*) from products) as total_record FROM products ; 

select * from products;
select product_name, price from products;
select * from products where price >500;
select * from products where category='Electronics';
select * from products WHERE price BETWEEN 100 and 500;
select * from products where product_name like 'S%';
select DISTINCT category from products;
select * from products ORDER BY price DESC;
select * from products ORDER BY price ASC LIMIT 3;
SELECT COUNT(*) from products;
SELECT DISTINCT category from products;
select COUNT(*) from products group by category; 
SELECT category, COUNT(*) AS total_products FROM products GROUP BY category HAVING category LIKE 'Clothing';
SELECT AVG(price) as avg_price from products;
select * from products ORDER BY price ASC LIMIT 1;
select * from products ORDER BY price DESC LIMIT 1;
select SUM(stock_quantity) from products where category='Electronics';
select SUM(stock_quantity) from products where category like 'Electronics';
SELECT SUM(stock_quantity) AS total_stock FROM products GROUP BY category HAVING category LIKE 'Electronics';
select * from products;
 
 UPDATE products
 SET stock_quantity=stock_quantity-5
 where product_name ='product 5';
 
DELETE from products 
where price <100;

select COUNT(*) from products;
alter table products ADD COLUMN Brand VARCHAR(100);
alter TABLE products RENAME COLUMN price to unit_price;
SELECT * from products;
alter TABLE products DROP COLUMN Brand;
select * from products