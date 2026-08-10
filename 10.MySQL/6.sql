use school;

create table students
(
Serial_Number int,	
First_Name varchar(30),	
Last_Name varchar(20),	
Gender varchar(30),	
Age int,	
Hometown varchar(30),	
Grade int,
primary key(Serial_Number)
);

select concat(First_Name,' ', Last_Name) from students;

select trim(First_Name) from students;

select substr(First_Name, 2, 5) as sub_firstname, First_Name from students;

select character_length(First_Name) as length, upper(First_Name) as uppercase, lower(First_Name) as lowercase from students;

select First_Name, ceiling(character_length(trim(First_Name))/2) as middle_element from students;