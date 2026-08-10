use churn;
select * from churn_data;
create view churn_male as select * from churn_data where Gender='Male';
select * from churn_male;
