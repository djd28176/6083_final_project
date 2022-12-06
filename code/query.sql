


/*
Query Tenants by First and Last Name
*/
SELECT * 
FROM tenants 
WHERE first_name = '{tenant_first}' 
AND last_name = '{tenant_last}';

/*
Query Tenants by SSN
*/
SELECt * 
FROM tenants 
WHERE ssn = '{tenant_ssn}';

/*
Check the Car's Owner whether is a tenant
*/
SELECT T.first_name, T.last_name, T.contact_number
FROM Tenants T, Cars C 
WHERE T.ssn = C.ssn
AND C.plate_number = '{plate_number}'

/*
Find tenants name and contact number who live in the specfic apartment,
Sort results by tenant's first name, with ties broken by tenant's last name.
*/
select T.first_name, T.last_name, T.contact_number, A.apartment_id
from Tenants T, Apartments A, Contracts C
where T.ssn = C.tenant_SSN
AND C.apartment_id = A.apartment_id
AND A.apartment_id = '201'
ORDER BY T.first_name, T.last_name;

/*
Find all the female employees who is on active duty and works more than 1 year 
Sort results by employees first name, with ties broken by employees last name.
*/

Select CurrentEmployees.first_name, CurrentEmployees.last_name, CurrentEmployees.workingDay
FROM(
    select E.first_name, E.last_name, (CURRENT_DATE - E.work_from) AS workingDay
    FROM Employees E
    WHERE E.work_to IS NULL
    AND E.gender = 'F'
) AS CurrentEmployees
WHERE CurrentEmployees.workingDay >= 365
ORDER BY CurrentEmployees.first_name, CurrentEmployees.last_name;


/*
Find number fo tenants who lives in the same building, Sort results by building name.
*/
select B.building_id ,count(B.building_id) AS Num_people
from Contracts C, Buildings B, Apartments A
WHERE C.apartment_id = A.apartment_id
AND A.building_id = B.building_id
Group BY B.building_id
Order BY B.building_name;


/*
Find total payment for specfic tenant by input tenant's SSN
*/
SELECT T.first_name, T.last_name, SUM(P.payment_amount) AS total_payment, Fee_table.total_fee
FROM Payments P, Tenants T, Contracts C,
( 
    SELECT P.contract_id, SUM(L.late_fee) AS total_fee
    FROM Late_Fees L, Paid P
    WHERE L.payment_id = P.payment_id
    GROUP BY contract_id
) AS Fee_table
WHERE T.SSN = C.tenant_ssn
AND P.contract_id = C.contract_id
AND Fee_table.contract_id = P.contract_id
AND T.SSN = '67657546875'
GROUP BY T.SSN, Fee_table.total_fee;


/*
Find all tenants who has a Car and lives in Buiding 2, 
Sort results by tenant's first name, with ties broken by tenant's last name and then by plate_number.
*/

SELECT T.first_name, T.last_name, Cars.plate_number
FROM Tenants T, Cars, Contracts C,
(
    Select C.contract_id
    From Contracts C, Buildings B, Apartments A
    WHERE C.apartment_id = A.apartment_id
    AND A.building_id = B.building_id
    AND B.building_id = '2'
) AS B2Contracts
WHERE T.SSN = C.tenant_ssn
AND C.contract_id = B2Contracts.contract_id
AND T.SSN = Cars.SSN
ORDER BY T.first_name, T.last_name, Cars.plate_number;

/*
Find number of empty apartments in each building,
Sort results by building name.
*/
SELECT B.building_name, (B.number_of_apartments - ApartmentsLeft.rented_room) AS empty_apartments
FROM Buildings B,
(
    Select A.building_id, count(*) AS rented_room
    From Contracts C, Apartments A
    WHERE C.apartment_id = A.apartment_id
    AND C.end_date > CURRENT_DATE
    GROUP BY A.building_id
) AS ApartmentsLeft
WHERE B.building_id = ApartmentsLeft.building_id
ORDER BY B.building_name;

/* 
List pairs of tenants from the Tenants table s.t. one of them has car and the other did not,
Sort results by Tenant_has_car, with ties broken by Tenant_has_no_car.
*/

Select (T1.first_name , T1.last_name) as Tenant_has_car, (T2.first_name , T2.last_name) as Tenant_has_no_car 
FROM Tenants T1, Tenants T2, Cars C,
(
    Select (T.first_name, T.last_name) as Nocar_tenant,T.SSN
    FROM Tenants T
    EXCEPT
    SELECT (T.first_name, T.last_name) as Has_car, T.SSN
    FROM Tenants T, Cars C
    WHERE T.SSN = C.SSN
) AS NoCar
WHERE T1.SSN = C.SSN
AND T2.SSN = NoCar.SSN
GROUP BY Tenant_has_car,Tenant_has_no_car
ORDER BY Tenant_has_car,Tenant_has_no_car;