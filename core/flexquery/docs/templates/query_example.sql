-- Example FlexQuery SQL query
-- Parameters can be referenced using :parameter_name syntax

SELECT 
    *
FROM 
    your_table
WHERE 
    date_column BETWEEN :start_date AND :end_date
    AND status = :status
LIMIT 100;