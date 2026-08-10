use churn;

select * from churn_data where EstimatedSalary > (select avg(EstimatedSalary) from churn_data);

select EstimatedSalary from churn_data where CustomerId='15619304';

select * from churn_data where EstimatedSalary > (select EstimatedSalary from churn_data where CustomerId='15619304');

select CustomerId from churn_data where EstimatedSalary = (select max(EstimatedSalary) from churn_data);

select * from churn_data where CustomerId='15662021';

select max(EstimatedSalary) as Salary from churn_data where EstimatedSalary <> (select max(EstimatedSalary) from churn_data);