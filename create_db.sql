
CREATE database budgetdb;
use budgetdb;
create table budget (sno int not null auto_increment primary key, exp_date date, expense int, reason varchar(50));"