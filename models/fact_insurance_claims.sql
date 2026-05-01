{{ config(materialized='view', alias='fact_InsuranceClaims') }}

SELECT
    c.Claim_Id          AS Claim_Id,
    cu.Customer_Id      AS Customer_Key,
    p.Policy_Id         AS Policy_Key,
    c.Date_Key          AS Date_Key,
    c.Risk_Score        AS Risk_Key,
    c.Claim_Amount      AS Claim_Amount,
    p.Premium_Amount    AS Premium_Amount,
    c.Claim_Status      AS Claim_Status,
    c.Claim_Type        AS Claim_Type,
    c.Fraud_Flag        AS Fraud_Flag,
    c.Processing_Days   AS Processing_Days

FROM {{ source('dbo', 'stg_Claims') }} c
LEFT JOIN {{ source('dbo', 'stg_Policies') }}  p ON c.Policy_Id = p.Policy_Id
LEFT JOIN {{ source('dbo', 'stg_Customers') }} cu ON c.Customer_Id = cu.Customer_Id