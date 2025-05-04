
CREATE DATABASE CollegeResourceSystem;

USE CollegeResourceSystem;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'HOD', 'Faculty') NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    resource_name VARCHAR(100) NOT NULL,
    resource_type ENUM('Classroom', 'Laboratory', 'Auditorium', 'Projector', 'Other') NOT NULL,
    capacity INT,
    department VARCHAR(50) NOT NULL,
    status ENUM('Available', 'Maintenance', 'Unavailable') NOT NULL
);

CREATE TABLE resource_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    time_slot VARCHAR(50) NOT NULL,
    purpose TEXT NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') NOT NULL,
    approved_resource VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (username, password, role, name, department, email) VALUES
('admin', 'admin123', 'Admin', 'Sunita Yadav', NULL, 'sunita.yadav@sksomaiya.edu'),
('hod.cs', 'hod123', 'HOD', 'Dr. Shrinivas Acharya', 'Computer Science', 'shrinivas.acharya@sksomaiya.edu'),
('hod.phy', 'hod123', 'HOD', 'Dr. Monali Deshpande', 'Physics', 'monali.deshpande@sksomaiya.edu'),
('faculty1', 'faculty123', 'Faculty', 'Prof. Alka Desai', 'Computer Science', 'alka.desai@sksomaiya.edu'),
('faculty2', 'faculty123', 'Faculty', 'Prof. Kulsum Tripathi', 'Computer Science', 'kulsum.tripathi@sksomaiya.edu'),
('faculty3', 'faculty123', 'Faculty', 'Prof. Ashmita Jadhav', 'Physics', 'ashmita.jadhav@sksomaiya.edu'),
('faculty4', 'faculty123', 'Faculty', 'Prof. Komal Kharat', 'Physics', 'komal.kharat@sksomaiya.edu'),
('faculty5', 'faculty123', 'Faculty', 'Prof. Rajesh Patil', 'Computer Science', 'rajesh.patil@sksomaiya.edu'),
('faculty6', 'faculty123', 'Faculty', 'Prof. Priya Sharma', 'Mathematics', 'priya.sharma@sksomaiya.edu'),
('faculty7', 'faculty123', 'Faculty', 'Prof. Amit Singh', 'Electronics', 'amit.singh@sksomaiya.edu');

INSERT INTO resources (resource_name, resource_type, capacity, department, status) VALUES
('CS Lab 101', 'Laboratory', 30, 'Computer Science', 'Available'),
('CS Lab 102', 'Laboratory', 25, 'Computer Science', 'Available'),
('CS Seminar Hall', 'Auditorium', 100, 'Computer Science', 'Available'),
('CS Projector 1', 'Projector', NULL, 'Computer Science', 'Available'),
('Physics Lab A', 'Laboratory', 20, 'Physics', 'Available'),
('Physics Lab B', 'Laboratory', 25, 'Physics', 'Maintenance'),
('Physics Lecture Hall', 'Classroom', 60, 'Physics', 'Available'),
('Main Auditorium', 'Auditorium', 200, 'General', 'Available'),
('Seminar Hall 1', 'Auditorium', 50, 'General', 'Available'),
('Projector 101', 'Projector', NULL, 'General', 'Available'),
('Chemistry Lab', 'Laboratory', 30, 'Chemistry', 'Available'),
('Maths Lab', 'Laboratory', 20, 'Mathematics', 'Available'),
('Maths Classroom', 'Classroom', 40, 'Mathematics', 'Available'),
('Electronics Lab', 'Laboratory', 25, 'Electronics', 'Available'),
('Robotics Lab', 'Laboratory', 15, 'Electronics', 'Available');

INSERT INTO resource_requests (user_id, resource_type, date, time_slot, purpose, status, approved_resource) VALUES
(4, 'Laboratory', '2023-11-15', '09:00-11:00', 'Data Structures Lab Session', 'Approved', 'CS Lab 101'),
(5, 'Classroom', '2023-11-16', '11:00-13:00', 'Theory of Computation Lecture', 'Approved', 'CS Seminar Hall'),
(6, 'Laboratory', '2023-11-17', '14:00-16:00', 'Quantum Physics Practical', 'Approved', 'Physics Lab A'),
(7, 'Projector', '2023-11-18', '16:00-18:00', 'Guest Lecture Presentation', 'Approved', 'Projector 101'),
(4, 'Laboratory', '2023-11-20', '09:00-11:00', 'Algorithm Design Lab', 'Pending', NULL),
(5, 'Auditorium', '2023-11-21', '14:00-16:00', 'Student Symposium', 'Pending', NULL),
(6, 'Laboratory', '2023-11-22', '11:00-13:00', 'Optics Experiment', 'Pending', NULL),
(7, 'Laboratory', '2023-11-10', '09:00-11:00', 'Faculty Meeting', 'Rejected', NULL),
(4, 'Auditorium', '2023-11-11', '14:00-16:00', 'Workshop', 'Rejected', NULL);
