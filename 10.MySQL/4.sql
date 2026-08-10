create database wanderaura;

use wanderaura;

set SQL_SAFE_UPDATES = 0;

create table customer
(
customer_id int unique not null,
customer_name varchar(50),
customer_age int not null,
customer_hometown varchar(50),
primary key(customer_id)
);

insert into customer values (1, 'Arin', 22, 'Prayagaj');
insert into customer values (2, 'Advik', 21, 'Dehradun');
insert into customer values (3, 'Vishal', 21, 'Dehradun');
insert into customer values (4, 'Vaishnavi', 21, 'Kurukshetra');
insert into customer values (5, 'Radhika', 21, 'Gangtok');
insert into customer values (6, 'Rishita', 22, 'Vadodara');

select * from customer;

update customer set customer_hometown = 'Noida' where customer_id = 5;

select * from customer;

alter table customer add column customer_designation varchar(50);

select * from customer;

update customer set customer_designation = 'Data Scientist' where customer_id = 1;
update customer set customer_designation = 'Advocate' where customer_id = 2;
update customer set customer_designation = 'Army' where customer_id = 3;
update customer set customer_designation = 'Teacher' where customer_id = 4;
update customer set customer_designation = 'Software Engineer' where customer_id = 5;
update customer set customer_designation = 'AI Engineer' where customer_id = 6;

select * from customer;

delete from customer where customer_designation = 'Teacher';

select * from customer;