{{ config(materialized='view', alias='dim_Customer') }}

SELECT
    Customer_Id         AS Customer_Key,
    Customer_Name       AS Customer_Name,
    Age                 AS Age,
    Age_Band            AS Age_Band,
    Gender              AS Gender,
    Province            AS Province,
    Employment_Status   AS Employment_Status,
    Credit_Score        AS Credit_Score,
    Credit_Band         AS Credit_Band,
    Joined_Date         AS Joined_Date

FROM {{ source('dbo', 'stg_Customers') }}