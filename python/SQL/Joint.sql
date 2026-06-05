CREATE DATABASE school_system;
USE school_system;

-- Create Students table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    instructor VARCHAR(50)
);

CREATE TABLE enrollments (
    enroll_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

INSERT INTO students (first_name, last_name, email) VALUES
('Ali', 'Khan', 'ali.khan@example.com'),
('Sara', 'Ahmed', 'sara.ahmed@example.com'),
('Usman', 'Rafiq', 'usman.rafiq@example.com'),
('Ayesha', 'Malik', 'ayesha.malik@example.com'),
('Bilal', 'Hassan', 'bilal.hassan@example.com'),
('Zain', 'Qureshi', 'zain.qureshi@example.com'),
('Hira', 'Fatima', 'hira.fatima@example.com'),
('Noman', 'Sheikh', 'noman.sheikh@example.com'),
('Fahad', 'Javed', 'fahad.javed@example.com'),
('Iqra', 'Naseer', 'iqra.naseer@example.com'),
('Hassan', 'Ali', 'hassan.ali@example.com'),
('Mariam', 'Iqbal', 'mariam.iqbal@example.com'),
('Imran', 'Khalid', 'imran.khalid@example.com'),
('Amna', 'Saeed', 'amna.saeed@example.com'),
('Rehan', 'Akbar', 'rehan.akbar@example.com'),
('Mehwish', 'Riaz', 'mehwish.riaz@example.com'),
('Kamran', 'Latif', 'kamran.latif@example.com'),
('Nida', 'Aslam', 'nida.aslam@example.com'),
('Yasir', 'Shahid', 'yasir.shahid@example.com'),
('Laiba', 'Farooq', 'laiba.farooq@example.com'),
('Taimoor', 'Irfan', 'taimoor.irfan@example.com'),
('Maryam', 'Tariq', 'maryam.tariq@example.com'),
('Hamza', 'Waheed', 'hamza.waheed@example.com'),
('Kiran', 'Jameel', 'kiran.jameel@example.com'),
('Rizwan', 'Yousaf', 'rizwan.yousaf@example.com'),
('Sana', 'Mirza', 'sana.mirza@example.com'),
('Hammad', 'Kamal', 'hammad.kamal@example.com'),
('Dua', 'Ali', 'dua.ali@example.com'),
('Adnan', 'Rauf', 'adnan.rauf@example.com'),
('Hafsa', 'Qadir', 'hafsa.qadir@example.com'),
('Furqan', 'Aziz', 'furqan.aziz@example.com'),
('Aiman', 'Butt', 'aiman.butt@example.com'),
('Rida', 'Sohail', 'rida.sohail@example.com'),
('Ahmad', 'Gul', 'ahmad.gul@example.com'),
('Arslan', 'Chaudhry', 'arslan.chaudhry@example.com'),
('Inaya', 'Younas', 'inaya.younas@example.com'),
('Talha', 'Ilyas', 'talha.ilyas@example.com'),
('Zoya', 'Rana', 'zoya.rana@example.com'),
('Omer', 'Sadiq', 'omer.sadiq@example.com'),
('Eman', 'Akram', 'eman.akram@example.com'),
('Junaid', 'Hassan', 'junaid.hassan@example.com'),
('Shiza', 'Farrukh', 'shiza.farrukh@example.com'),
('Saad', 'Mehmood', 'saad.mehmood@example.com'),
('Areeba', 'Tahir', 'areeba.tahir@example.com'),
('Moiz', 'Saleem', 'moiz.saleem@example.com'),
('Kashan', 'Ali', 'kashan.ali@example.com'),
('Mahnoor', 'Rehman', 'mahnoor.rehman@example.com'),
('Hina', 'Bashir', 'hina.bashir@example.com'),
('Danish', 'Rasheed', 'danish.rasheed@example.com'),
('Asad', 'Hussain', 'asad.hussain@example.com'),
('Saba', 'Khalid', 'saba.khalid@example.com');

INSERT INTO courses (course_name, instructor) VALUES
('Database Systems', 'Prof. Smith'),
('Web Development', 'Dr. Adams'),
('Machine Learning', 'Dr. Khan'),
('Operating Systems', 'Prof. Lee'),
('Computer Networks', 'Dr. Ahmed'),
('Data Structures', 'Prof. Ali'),
('Software Engineering', 'Dr. Kim'),
('Cyber Security', 'Dr. Brown'),
('Artificial Intelligence', 'Prof. Chen'),
('Mobile App Development', 'Dr. Parker');


INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES
(1, 1, '2025-01-10'),
(1, 2, '2025-02-01'),
(2, 3, '2025-01-12'),
(3, 2, '2025-02-15'),
(4, 5, '2025-03-05'),
(5, 1, '2025-02-20'),
(6, 4, '2025-03-10'),
(7, 6, '2025-01-25'),
(8, 3, '2025-02-13'),
(9, 7, '2025-02-23'),
(10, 2, '2025-03-01'),
(11, 8, '2025-01-29'),
(12, 9, '2025-02-05'),
(13, 10, '2025-03-15'),
(14, 1, '2025-02-07'),
(15, 2, '2025-03-20'),
(16, 3, '2025-01-30'),
(17, 4, '2025-02-17'),
(18, 5, '2025-03-10'),
(19, 6, '2025-02-25'),
(20, 7, '2025-03-11'),
(21, 8, '2025-01-26'),
(22, 9, '2025-02-18'),
(23, 10, '2025-03-07'),
(24, 1, '2025-01-21'),
(25, 2, '2025-02-09'),
(26, 3, '2025-03-03'),
(27, 4, '2025-02-14'),
(28, 5, '2025-03-18'),
(29, 6, '2025-01-31'),
(30, 7, '2025-02-22'),
(31, 8, '2025-03-09'),
(32, 9, '2025-01-28'),
(33, 10, '2025-02-06'),
(34, 1, '2025-03-16'),
(35, 2, '2025-01-19'),
(36, 3, '2025-02-12'),
(37, 4, '2025-03-02'),
(38, 5, '2025-02-26'),
(39, 6, '2025-01-24'),
(40, 7, '2025-03-13'),
(41, 8, '2025-02-04'),
(42, 9, '2025-03-08'),
(43, 10, '2025-01-27'),
(44, 1, '2025-02-02'),
(45, 2, '2025-03-12'),
(46, 3, '2025-01-23'),
(47, 4, '2025-02-08'),
(48, 5, '2025-03-14'),
(49, 6, '2025-01-20'),
(50, 7, '2025-02-19'),
(1, 8, '2025-03-04'),
(2, 9, '2025-01-22'),
(3, 10, '2025-02-24'),
(4, 1, '2025-03-17'),
(5, 2, '2025-01-18'),
(6, 3, '2025-02-11'),
(7, 4, '2025-03-06'),
(8, 5, '2025-01-29'),
(9, 6, '2025-02-10'),
(10, 7, '2025-03-19'),
-- ... repeat random pattern to reach 200 records
(11, 8, '2025-01-17'),
(12, 9, '2025-02-16'),
(13, 10, '2025-03-21'),
(14, 1, '2025-01-25'),
(15, 2, '2025-02-23'),
(16, 3, '2025-03-05'),
(17, 4, '2025-01-28'),
(18, 5, '2025-02-06'),
(19, 6, '2025-03-09'),
(20, 7, '2025-01-30'),
(21, 8, '2025-02-27'),
(22, 9, '2025-03-18'),
(23, 10, '2025-02-01'),
(24, 1, '2025-03-10'),
(25, 2, '2025-01-31'),
(26, 3, '2025-02-15'),
(27, 4, '2025-03-08'),
(28, 5, '2025-01-27'),
(29, 6, '2025-02-14'),
(30, 7, '2025-03-01'),
(31, 8, '2025-01-19'),
(32, 9, '2025-02-26'),
(33, 10, '2025-03-03'),
(34, 1, '2025-02-09'),
(35, 2, '2025-03-16'),
(36, 3, '2025-01-20'),
(37, 4, '2025-02-22'),
(38, 5, '2025-03-13'),
(39, 6, '2025-01-29'),
(40, 7, '2025-02-18'),
(41, 8, '2025-03-06'),
(42, 9, '2025-01-24'),
(43, 10, '2025-02-12'),
(44, 1, '2025-03-15'),
(45, 2, '2025-01-22'),
(46, 3, '2025-02-17'),
(47, 4, '2025-03-05'),
(48, 5, '2025-01-25'),
(49, 6, '2025-02-19'),
(50, 7, '2025-03-07');


CREATE TABLE attendance (
    student_id INT,
    course_id INT,
    attendance_date DATE,
    status VARCHAR(10),
    PRIMARY KEY (student_id, course_id, attendance_date),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

INSERT IGNORE INTO attendance (student_id, course_id, attendance_date, status)
SELECT 
    FLOOR(1 + RAND() * 10) AS student_id,
    FLOOR(1 + RAND() * 5) AS course_id,
    DATE_ADD('2025-03-01', INTERVAL FLOOR(RAND() * 30) DAY) AS attendance_date,
    CASE 
        WHEN RAND() < 0.8 THEN 'Present'
        ELSE 'Absent'
    END AS status
FROM
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION
     SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION
     SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION
     SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20) t1,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION
     SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t2;
     
SELECT * from attendance;     


SELECT s.first_name, s.last_name, c.course_name, e.enrollment_date
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id;

SELECT s.first_name, s.last_name, e.course_id
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id;


SELECT c.course_name, e.student_id
FROM enrollments e
RIGHT JOIN courses c ON e.course_id = c.course_id;

SELECT s.first_name, c.course_name
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
LEFT JOIN courses c ON e.course_id = c.course_id;

SELECT s.first_name, c.course_name
FROM students s
RIGHT JOIN enrollments e ON s.student_id = e.student_id
RIGHT JOIN courses c ON e.course_id = c.course_id;

SELECT s.first_name, c.course_name
FROM students s
CROSS JOIN courses c;

SELECT s1.first_name AS student1, s2.first_name AS student2, s1.last_name
FROM students s1
JOIN students s2
ON s1.last_name = s2.last_name AND s1.student_id != s2.student_id;
