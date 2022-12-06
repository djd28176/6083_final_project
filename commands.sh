# upload through scp
scp -r /Users/jindongdu/Documents/NYU/6083\ database\ systems/hx2163_jd4573_project    jd4573@jedi.poly.edu:~/hx2163_jd4573_project
# login jedi
ssh jd4573@jedi.poly.edu -L 8624:localhost:8624
# create table @jedi
psql -d jd4573_db -a -f hx2163_jd4573_project/code/schema.sql
psql -h localhost -U jd4573 jd4573_db
# import data @jedi
cat hx2163_jd4573_project/data/Buildings.csv | psql -U jd4573 -d jd4573_db -c "COPY Buildings from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/Apartments.csv | psql -U jd4573 -d jd4573_db -c "COPY Apartments from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/Employees.csv | psql -U jd4573 -d jd4573_db -c "COPY Employees from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/works_at.csv | psql -U jd4573 -d jd4573_db -c "COPY works_at from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/Tenants.csv | psql -U jd4573 -d jd4573_db -c "COPY Tenants from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/Contracts.csv | psql -U jd4573 -d jd4573_db -c "COPY Contracts from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/Cars.csv | psql -U jd4573 -d jd4573_db -c "COPY Cars from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/Payments.csv | psql -U jd4573 -d jd4573_db -c "COPY Payments from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/Paid.csv | psql -U jd4573 -d jd4573_db -c "COPY Paid from STDIN CSV HEADER"
cat hx2163_jd4573_project/data/Late_Fees.csv | psql -U jd4573 -d jd4573_db -c "COPY Late_Fees from STDIN CSV HEADER"
# port forwarding and run the streamlit app
# ssh jd4573@jedi.poly.edu -L 8624:localhost:8624
cd hx2163_jd4573_project/code/

streamlit run project.py --server.address=localhost --server.port=8624