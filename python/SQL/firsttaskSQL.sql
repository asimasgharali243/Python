-- Step 1: Create database
CREATE DATABASE IF NOT EXISTS my_school;
USE my_school;


-- Step 2: Create students table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY, 
    first_name VARCHAR(50) NOT NULL,          
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,                  
    age INT CHECK (age >= 5),                   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- Step 3: Insert 200 students automatically using a procedure
DELIMITER //
CREATE PROCEDURE insert_students()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 200 DO
        INSERT INTO students (first_name, last_name, email, age)
        VALUES (
            CONCAT('First', i),                      -- First name: First1, First2...
            CONCAT('Last', i),                       -- Last name: Last1, Last2...
            CONCAT('student', i, '@school.com'),     -- Unique email
            FLOOR(10 + (RAND() * 15))                -- Random age between 10 and 25
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

-- Step 4: Run the procedure
CALL insert_students();

-- Step 5: Sample queries
SELECT * FROM students LIMIT 10;  -- first 10 students
SELECT COUNT(*) AS total_students FROM students; -- should show 200
SELECT age, COUNT(*) FROM students GROUP BY age ORDER BY age; -- age distribution
SELECT * FROM students;


SELECT first_name, email FROM students;


SELECT * FROM students LIMIT 5;


-- select with condition
SELECT * FROM students WHERE age > 18;

-- select with sorting
SELECT * FROM students ORDER BY age DESC;

-- select distinct values (no duplicates)
SELECT DISTINCT age FROM students;

SELECT DISTINCT age FROM students;

SELECT * FROM students WHERE age > 18;
SELECT * FROM students WHERE first_name = 'Ali';
SELECT * FROM students WHERE email IS NULL;   -- find students with no email

SELECT * FROM students ORDER BY age ASC;   -- ascending
SELECT * FROM students ORDER BY age DESC;  -- descending


SELECT * FROM students LIMIT 5;        -- show first 5
SELECT * FROM students LIMIT 5 OFFSET 5; -- skip 5, then show next 5

ALTER TABLE students ADD COLUMN phone VARCHAR(15);

ALTER TABLE students DROP COLUMN phone;
ALTER TABLE students DROP CHECK students_chk_1;
ALTER TABLE students RENAME COLUMN age TO student_age;

ALTER TABLE students MODIFY COLUMN student_age SMALLINT;

SET SQL_SAFE_UPDATES = 0;

DELETE FROM students WHERE student_age < 10;
SELECT * from students;
create table teacher(id int AUTO_INCREMENT PRIMARY KEY,Name varchar(100) not null,age int not null,phno varchar(100));
DELIMITER //
CREATE PROCEDURE insert_teachers()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 200 DO
        INSERT INTO teacher (Name, age, phno)
        VALUES (
            CONCAT('Teacher ', i),
            FLOOR(25 + (RAND() * 25)),   -- Random age between 25–50
            CONCAT('0300123', LPAD(i, 4, '0')) -- phone like 03001230001
        );
        SET i = i + 1;
    END WHILE;
END;
//
DELIMITER ;

-- Call procedure to insert 200 records
CALL insert_teachers();

SELECT * from teacher;
SELECT Name,phno from teacher;
SELECT * from teacher where age>30;
SELECT Name from teacher where age=40;
DELETE from teacher where phno='0000';
ALTER TABLE teacher RENAME COLUMN Name TO FullName;
ALTER TABLE teacher ADD COLUMN Address VARCHAR(100); 
SELECT * from teacher;
ALTER TABLE teacher MODIFY COLUMN phno VARCHAR(50);