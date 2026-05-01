{% snapshot claims_snapshot %}

{{
    config(
        target_schema='dbo',
        unique_key='Claim_Id',
        strategy='check',
        check_cols=['Claim_Status', 'Fraud_Flag'],
    )
}}

SELECT
    Claim_Id,
    Customer_Id,
    Policy_Id,
    Claim_Date,
    Claim_Amount,
    Claim_Type,
    Claim_Status,
    Fraud_Flag,
    Processing_Days,
    Stg_Loaded_At
FROM {{ source('dbo', 'stg_Claims') }}

{% endsnapshot %}