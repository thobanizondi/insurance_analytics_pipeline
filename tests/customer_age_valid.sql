-- Test: Customer age must be between 18 and 75
-- If this query returns rows, the test FAILS

SELECT
    CustomerKey,
    CustomerName,
    Age
FROM {{ ref('dim_customer') }}
WHERE Age < 18 OR Age > 75