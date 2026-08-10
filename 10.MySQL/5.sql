create database Aura; 

use Aura;         

-- Student --> id, name, age, gender, location
create table Students
(
student_id int unique,
student_name varchar(60) not null unique,
student_age int,
student_gender varchar(1),
student_location varchar(50)
);
