-- duckdb test
SELECT 
    EmployerPK,
    OneCode,
    employer.EmployerName,
    employer.FileDate
FROM employer
left join scheme on employer.OneCode = scheme.EmployerKey
WHERE 
    scheme.EmployerKey in :employer_key 
    and employer.FileDate in :file_date 

ORDER BY employer.EmployerName ASC
