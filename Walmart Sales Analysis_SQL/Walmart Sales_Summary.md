# Feature Engineering:

In the feature engineering part of this project, new columns (time_of_day, day_name, month_name) were added to an existing table (Sales) based on the values from the time and date columns. This process involved the following steps:

            Definition of New Columns:
                  New columns (time_of_day, day_name, month_name) were defined as part of the Sales table schema to store derived values based on existing data.
            Utilization of CASE Statements:
                  CASE statements were utilized within SELECT queries to conditionally assign values to the new columns (time_of_day, day_name, month_name) based on specified criteria.
            Population of New Columns with UPDATE Queries:
                  UPDATE queries were used to populate the newly added columns (time_of_day, day_name, month_name) in the Sales table with the values derived from the existing time and date columns.
                  The UPDATE statements utilized CASE expressions to conditionally set values for each row in the table based on specific time or date ranges.

# Exploratory Data Analysis (EDA):

Conducted various EDA queries to analyze sales data:

      Unique cities and branches in the dataset.
      Count of unique product lines and most common payment methods.
      Total revenue, COGS (Cost of Goods Sold), and VAT (Value Added Tax) analysis by month, product line, city, and branch.
      Analysis of customer types, gender distribution, and average ratings across different dimensions (time of day, day of week, branch, etc.).

Sales Analysis:

Analyzed sales data based on time of day, customer type, city, and payment methods to identify trends and insights:

      Total sales volume and revenue by time of day.
      Revenue contribution and VAT analysis by city and customer type.
      Ratings analysis based on time of day, day of week, and branch.

Customer Analysis:

Investigated customer-related metrics such as customer types, gender distribution, and customer ratings:

      Identification of unique customer types and payment methods.
      Analysis of customer demographics (gender distribution) and their rating behavior based on different dimensions (time of day, day of week, branch).

