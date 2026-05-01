{% macro get_risk_category(credit_score) %}
    CASE
        WHEN {{ credit_score }} >= 700 THEN 'Low Risk'
        WHEN {{ credit_score }} >= 500 THEN 'Medium Risk'
        ELSE 'High Risk'
    END
{% endmacro %}