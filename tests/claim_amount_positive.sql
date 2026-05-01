-- Test: No claim should have a zero or negative amount
-- If this query returns rows, the test FAILS

SELECT
    ClaimId,
    ClaimAmount
FROM {{ ref('fact_insurance_claims') }}
WHERE ClaimAmount <= 0