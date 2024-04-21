create database if not exists WalmartSales;

-- Datawrangling --
create table if not exists Sales(
	invoice_id varchar(30) not null primary key,
    branch varchar(5) not null,
    city varchar(30) not null,
    customer_type varchar(30) not null,
    gender varchar(10) not null,
    product_line varchar(100) not null,
    unit_price decimal(10, 2) not null,
    quantity int not null,
    VAT float(6, 4) not null,
    total decimal(12, 4) not null,
    date datetime not null,
    time time not null,
    payment_method varchar(15) not null,
    cogs decimal(10, 2) not null,
    gross_margin_pct float(11, 9),
    gross_income decimal(12, 4) not null,
    rating float(2, 1)
);
Select * from walmartsales.sales;


-- --------------------------------------------------------- --
-- Feature Engineering --
-- Inserting time_of_day column --
Select time,
	(case
	when `time` between "00:00:00" and "12:00:00" then "Morning"
    when `time` between "12:00:01" and "16:00:00" then "Afternoon"
    else "Evening"
    end
	) As time_of_day
from sales;

Alter table sales add column time_of_day varchar(20);

update sales 
set time_of_day = (
	case
		when `time` between "00:00:00" and "12:00:00" then "Morning"
		when `time` between "12:00:01" and "16:00:00" then "Afternoon"
		else "Evening"
    end
);

-- day_name --
select date, dayname(date) as day_name from sales;

alter table sales add column day_name varchar(10);

update sales 
set day_name = dayname(date);

-- month_name --
select date, monthname(date) as month_name from sales;

alter table sales add column month_name varchar(10);

update sales 
set month_name = monthname(date);

select * from sales;
-- --------------------------------------------------------- --


-- --------------------------------------------------------- --

-- Exploratory Data Analysis --

-- --------------------------------------------------------- --
-- Generic --

-- Number of unique cities the data have --
select distinct city from sales;
-- Number of branch the city have --
select distinct branch from sales;
select distinct city, branch from sales;

-- --------------------------------------------------------- --
-- -----Product related analysis---- --
-- How many unique product lines does the data have? --

select count(distinct product_line) from sales; 

-- Most common payment method --
select payment_method, count(payment_method) as cnt from sales group by payment_method order by cnt desc;
-- Most selling product line --
select product_line, count(product_line) as cpl from sales group by product_line order by cpl desc; 
-- Total revenue by month --
select * from sales;

select month_name as month,
sum(total) as total_revenue
from sales group by month
order by total_revenue desc;

-- Month with largest COGS --
select month_name as month, 
sum(cogs) as cogs
from sales 
group by month
order by cogs desc;

-- Product line with largest revenue --
select product_line,
sum(total) as total_revenue
from sales
group by product_line 
order by total_revenue desc;

-- City with largest revenue --

select branch,
city,
sum(total) as total_revenue
from sales 
group by city, branch
order by total_revenue desc;

-- Product line with largest VAT --

select product_line,
sum(VAT) as VAT
from sales
group by product_line
order by VAT desc;

select product_line,
avg(VAT) as VAT
from sales
group by product_line
order by VAT desc;

-- which brand sold more product than average --
select branch,
sum(quantity) as total_quantity
from sales
group by branch
having sum(quantity) > (select avg(quantity));

-- what is the most common product line by gender --
select gender, product_line,
count(gender) as cg
from sales 
group by gender, product_line
order by cg desc;



-- what is the average rating of each product line --

select product_line,
round(avg(rating),2) as average_rating 
from sales 
group by product_line
order by average_rating desc;

-- --------------------------------------------------------- --



-- --------------------------------------------------------- --

-- -------------- Sales Analysis --------------------------- --
-- Number of sales made in each time of the day per weekday --
select
time_of_day,
count(*) as total_sales
from sales
group by time_of_day
order by total_sales desc;

select
time_of_day,
count(*) as total_sales
from sales
where day_name = "Wednesday"
group by time_of_day
order by total_sales desc;

-- Which customer type brings the most revenue --
select customer_type,
sum(total) as total_revenue
from sales
group by customer_type
order by total_revenue desc;

-- Which city has the largest tax percent/VAT --

select city,
avg(VAT) as VAT
from sales
group by city
order by VAT desc;

-- Which customer type pays the most VAT --

select customer_type,
avg(VAT) as VAT
from sales 
group by customer_type
order by VAT desc;


-- --------------------------------------------------------- --
-- --------------------------------------------------------- --
-- ------------------Customer------------------------------- --

-- How many unique customer type does the data have --

select distinct(customer_type)
from sales;

-- How many unique payment methods does the data have --

select distinct(payment_method)
from sales;

-- What is the most common customer type --

select customer_type,
count(customer_type) as cct
from sales
group by customer_type
order by cct desc;

-- What is the gender of most of the customer --

select gender,
count(invoice_id) as number_of_customers
from sales 
group by gender
order by number_of_customers desc;

-- what is the gender distribution per branch --

select branch,
gender,
count(invoice_id) as number_of_cust
from sales
group by gender, branch
order by branch;

-- which time of the day do customers give most ratings --
select time_of_day,
count(rating) as rating
from sales
group by time_of_day;

-- which time of the day do customers give better ratings --

select time_of_day,
avg(rating) as rating
from sales
group by time_of_day
order by rating desc;

-- which time of the day do customers give best ratings per branch --

select branch, time_of_day,
avg(rating) as rating
from sales
group by time_of_day, branch
order by branch, rating desc;

-- Which day of week has the best avg ratings --

select day_name,
avg(rating) as rating
from sales 
group by day_name
order by rating desc;

-- Which day of the week has the best average ratings per branch --

select branch, day_name,
avg(rating) as rating
from sales 
group by day_name, branch
order by rating desc;


-- --------------------------------------------------------- --