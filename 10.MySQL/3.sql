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

 select * from Students;
 
 insert into Students values(1, 'Arin Sharma', 22, 'M', 'Uttar Pradesh');
 
 insert into Students values(2, 'Advik Verma', 21, 'M', 'Uttarakhand');
 
 insert into Students values(3, 'Rishita Bhatt', 22, 'F', 'Gujarat');

 create table department
 (
 department_id int not null,
 department_name varchar(25),
 department_address varchar(50),
 Primary Key(department_id)
 );
 
select * from department;
 
create table employee
 (
 employee_id int,
 employee_name varchar(50),
 department_id int not null,
 department_address varchar(50),
 primary key(employee_id),
 foreign key(department_id) references department(department_id)
 );
 
select * from employee;

show tables;

create table result
(
student_id int not null,
student_name varchar(50),
student_gender varchar(10),
student_marks int,
primary key(student_id)
);

select * from result;

insert into result values(1, 'Rishita Bhatt', 'Female', 99);