create database Optivest;

use Optivest;

create table employee
(
first_name varchar(30),
last_name varchar(20),
title varchar(30),
age int,
salary int
);

select * from employee;

alter table employee add gender varchar(5);

select * from employee;

alter table employee drop column title;

select * from employee;

drop table employee;

select * from employee;