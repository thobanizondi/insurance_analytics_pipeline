{{ config(materialized='view', alias='dim_Policy') }}

SELECT
    Policy_Id           AS Policy_Key,
    Policy_Id           AS Policy_Id,
    Policy_Type         AS Policy_Type,
    Coverage_Amount     AS Covarage_Amount,
    Premium_Amount      AS Premium_Amount,
    Start_Date          AS Start_Date,
    End_Date            AS End_Date,
    Policy_Status       AS Policy_Status

FROM {{ source('dbo', 'stg_Policies') }}