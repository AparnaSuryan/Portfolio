SELECT 
    ss_customer_sk AS customer_id,
    COUNT(DISTINCT ss_ticket_number) AS total_orders,
    ROUND(SUM(ss_net_paid), 2) AS total_spent,
    ROUND(AVG(ss_net_paid), 2) AS avg_order_value,
    ROUND(SUM(ss_net_profit), 2) AS total_profit
FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE_SALES
GROUP BY ss_customer_sk
ORDER BY total_spent DESC
LIMIT 20;