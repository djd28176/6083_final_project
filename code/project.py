import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

"# Apartment Management System"


@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


"## Read tables"

sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
try:
    # all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    all_table_names = ['Buildings', 'Apartments', 'Employees', 'works_at', 'Tenants', 'Contracts', 'Cars', 'Payments', 'Paid', 'Late_Fees']
    table_name = st.selectbox("Choose a table", all_table_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if table_name:
    f"Display the table"

    sql_table = f"SELECT * FROM {table_name};"
    try:
        df = query_db(sql_table)
        st.dataframe(df)
    except:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )

"## Query Tenants by First and Last Name"

tenant_first = st.text_input('First Name')
tenant_last = st.text_input('Last Name')
if tenant_first and tenant_last:
    sql_tenant = f"SELECT * FROM tenants WHERE first_name = '{tenant_first}' AND last_name = '{tenant_last}';"
    try:
        df = query_db(sql_tenant)
        st.dataframe(df)
    except:
        st.write(f"Sorry! '{tenant_first}' '{tenant_last}' does not exist in the datasystem.")

"## Query Tenants by SSN"
tenant_ssn = st.text_input('Social Secuirty Number')
if tenant_ssn:
    sql_tenant_ssn = f"SELECt * FROM tenants WHERE ssn = '{tenant_ssn}';"
    try:
        tenant_info = query_db(sql_tenant_ssn).loc[0]
        t_first, t_last, t_number, t_email = (
            tenant_info["first_name"],
            tenant_info["last_name"],
            tenant_info["contact_number"],
            tenant_info["email"]
        )
        st.write(
            f"{tenant_ssn}: {t_first} {t_last}'s contact number is {t_number} and email address is {t_email}."
        )
    except:
        st.write(f"Sorry! {tenant_ssn} does not exist in the datasystem.")

"## Check the Car's Owner Whether Is A Tenant: "
plate_number = st.text_input('Plate Number')
if plate_number:
    sql_plate = f"""
        SELECT T.first_name, T.last_name, T.contact_number
        FROM Tenants T, Cars C 
        WHERE T.ssn = C.ssn
        AND C.plate_number = '{plate_number}';
    """
    try:
        car_info = query_db(sql_plate).loc[0]

        car_owner_first, car_owner_last, owner_number = (car_info["first_name"], car_info["last_name"], car_info["contact_number"])
        st.write(f"{plate_number} belongs to {car_owner_first} {car_owner_last}, the phone number is {owner_number}.")
    except:
        st.write(f"{plate_number} does not belong to any of our tenants.")

"""## Find tenants name and contact number who live in the specfic apartment. Sort results by tenant's first name, with ties broken by tenant's last name."""

apart_id = st.text_input("Apartment ID:")
if apart_id:
    sql_find_tenant_apart_id = f"""
        select T.first_name, T.last_name, T.contact_number, A.apartment_id
        from Tenants T, Apartments A, Contracts C
        where T.ssn = C.tenant_SSN
        AND C.apartment_id = A.apartment_id
        AND A.apartment_id = {apart_id}
        ORDER BY T.first_name, T.last_name;"""
    try:
        ap_info = query_db(sql_find_tenant_apart_id).loc[0]
        ap_first, ap_last, ap_number = (ap_info["first_name"], ap_info["last_name"], ap_info["contact_number"])
        st.write(f"{apart_id}'s tenant is {ap_first} {ap_last}, the phone number is {ap_number}.")
    except:
        st.write(f"No one lives in {apart_id} yet.")

"""## Find all the female employees who is on active duty and works more than 1 year. Sort results by employees first name, with ties broken by employees last name."""
year = st.text_input("Input 365 as one year:")
if year:
    sql_year = f"""
        Select CurrentEmployees.first_name, CurrentEmployees.last_name, CurrentEmployees.workingDay
        FROM(
            select E.first_name, E.last_name, (CURRENT_DATE - E.work_from) AS workingDay
            FROM Employees E
            WHERE E.work_to IS NULL
            AND E.gender = 'F'
        ) AS CurrentEmployees
        WHERE CurrentEmployees.workingDay >= {year}
        ORDER BY CurrentEmployees.first_name, CurrentEmployees.last_name;
    """
    try:
        year_df = query_db(sql_year)
        st.dataframe(year_df)
    except:
        st.write(f"No employee works more than {year} days.")

        
"## Find number fo tenants who lives in the same building, Sort results by building name."
yes_or_no = st.text_input("Type Yes if you want to run this query: ")
# yes_or_no = st.selectbox("Choose Yes or No",choose)
if yes_or_no.lower() == "yes":
    sql_yes = """
        select B.building_id ,count(B.building_id) AS Num_people
        from Contracts C, Buildings B, Apartments A
        WHERE C.apartment_id = A.apartment_id
        AND A.building_id = B.building_id
        Group BY B.building_id
        Order BY B.building_name;
    """
    try:
        yes_df = query_db(sql_yes)
        st.dataframe(yes_df)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

"## Find total payment for specfic tenant by input tenant's SSN"
t_ssn = st.text_input("Tenant's SSN: ")
if t_ssn:
    sql_payment = f"""
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
        AND T.SSN = '{t_ssn}'
        GROUP BY T.SSN, Fee_table.total_fee;
    """
    try:
        payment_info = query_db(sql_payment).loc[0]
        p_first, p_last,p_amount, p_late = (payment_info["first_name"], 
        payment_info["last_name"], 
        payment_info["total_payment"], 
        payment_info["total_fee"])
        st.write(f"{p_first} {p_last} has contributed to our company \${p_amount} with \${p_late} late fee!")
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

"""## Find all tenants who has a Car and lives in a specific Buiding. Sort results by tenant's first name with ties broken by tenant's last name and then by plate_number."""
t_building = st.text_input("Target Building: ")
if t_building:
    sql_car = f"""
        SELECT T.first_name, T.last_name, Cars.plate_number
        FROM Tenants T, Cars, Contracts C,
        (
            Select C.contract_id
            From Contracts C, Buildings B, Apartments A
            WHERE C.apartment_id = A.apartment_id
            AND A.building_id = B.building_id
            AND B.building_id = '{t_building}'
        ) AS B2Contracts
        WHERE T.SSN = C.tenant_ssn
        AND C.contract_id = B2Contracts.contract_id
        AND T.SSN = Cars.SSN
        ORDER BY T.first_name, T.last_name, Cars.plate_number;
    """
    try:
        car_df = query_db(sql_car)
        st.dataframe(car_df)
    except:
        st.write(f"No one has car in Building {t_building}")

"## Find number of empty apartments in each building Sort results by building name."  
choose = ["Yes","No"]      
whether = st.selectbox("Choose Yes or No",choose)
if whether.lower() == "no":
    st.write("You choose not to look for this query.")
if whether.lower() == "yes":
    sql_empty = """
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
    """
    try:
        df_empty = query_db(sql_empty)
        st.dataframe(df_empty)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")


"## List pairs of tenants from the Tenants table s.t. one of them has car and the other did not."
triggerlist = ["Show","Hide"]
trigger = st.selectbox("Choose Show or Hide", triggerlist)
if trigger.lower() == "hide":
    st.write("You choose not to look for this query.")
if trigger.lower() == "show":
    sql_pair = f"""
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
        ORDER BY Tenant_has_car,Tenant_has_no_car;"""
    try:
        df_pair = query_db(sql_pair)
        st.dataframe(df_pair)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")
        
"## Thank you for using our database system!"