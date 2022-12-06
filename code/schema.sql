drop table if exists Buildings cascade;
drop table if exists Apartments cascade;
drop table if exists Employees cascade;
drop table if exists works_at cascade;
drop table if exists Tenants cascade;
drop table if exists Contracts cascade;
drop table if exists Cars cascade;
drop table if exists Payments cascade;
drop table if exists Paid cascade;
drop table if exists Late_Fees cascade;



create table Buildings(
    building_id 		    integer primary key,
    building_name 		    varchar(128),
    number_of_apartments 	integer
);

create table Apartments(
    apartment_id        integer primary key,
    number_of_bedrooms  integer,
    sqrt_feet           float,
    price               float,
    building_id 		integer not null,
    foreign key (building_id) references Buildings(building_id)
);

create table Employees (
    employee_id 		integer primary key,
    first_name 			varchar(128),
    last_name 			varchar(128),
    gender 			    varchar(1),
    work_from           date,
    work_to             date
);
create table works_at(
    building_id         integer,
    employee_id         integer,
    primary key(building_id, employee_id),
    foreign key(employee_id) references Employees(employee_id),
    foreign key(building_id) references Buildings(building_id)
);

create table Tenants (
    SSN 			    varchar(11) primary key,
    first_name 			varchar(128),
    last_name 			varchar(128),
    gender	 		    varchar(1),
    contact_number 		varchar(10),
    email 			    varchar(128)
);

create table Contracts (
    contract_id 		integer primary key,
    employee_id 		integer not null,
    tenant_SSN 			varchar(11) not null unique,
    apartment_id 		integer not null unique,
    start_date 			date not null,
    end_date 			date not null,
    deposit 			float,
    foreign key (employee_id) references Employees(employee_id),
    foreign key (tenant_SSN) references Tenants(SSN)
);

create table Cars(
    SSN			        varchar(11) not null,
    plate_number 		varchar(128),
    model 			    varchar(128),
    make 			    varchar(128),
    primary key(SSN,plate_number),
    foreign key (SSN) references Tenants(SSN) on delete cascade
);

create table Payments(
    payment_id 		    integer primary key,
    contract_id 		integer,
    payment_amount 		float,
    payment_date 		date,
    foreign key (contract_id) references Contracts(contract_id)
);


create table Paid(
    contract_id 		integer,
    payment_id 		    integer,
    primary key (contract_id,payment_id),
    foreign key (contract_id) references Contracts(contract_id),
    foreign key (payment_id) references Payments(payment_id)
);

create table Late_Fees(
    late_id 			integer,
    late_fee			float,
    payment_id 		    integer not null,
    primary key(late_id,payment_id),
    foreign key (payment_id) references Payments(payment_id) on delete cascade
);

