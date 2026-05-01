-- Test: Fraud flag must only contain 'Yes' or 'No'
-- If this query returns rows, the test FAILS

SELECT
    ClaimId,
    FraudFlag
FROM {{ ref('fact_insurance_claims') }}
WHERE FraudFlag NOT IN ('Yes', 'No')