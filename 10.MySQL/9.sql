use churn;

select * from churn_data where Geography like 'F%';

select * from churn_data where Surname regexp '^A';

select count(*) from churn_data where Surname regexp '[arin]';