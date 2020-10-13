create type MedicalForm as ENUM ('powder', 'capsule', 'ampoule', 'pill');
create type SalePackage as ENUM ('флакон', 'тюбик');

create table Manufacturer (
  id serial PRIMARY KEY,
  name text not null
);

create TABLE Lab (
  id INT PRIMARY KEY, 
  name TEXT,
  chief TEXT
);

create TABLE Certification (
  number BIGINT PRIMARY KEY,
  valid_until DATE,
  lab_id INT REFERENCES Lab (id)
);

create TABLE ChemicalCompound (
  id Serial PRIMARY KEY, 
  name TEXT UNIQUE, 
  formula TEXT UNIQUE
);

create table Drug (
  id serial PRIMARY KEY,
  trade_name text,
  international_name text,
  medical_form MedicalForm,
  manufacturer_id INT references Manufacturer,
  main_chemicalcompound_id INT references ChemicalCompound,
  cert_number INT references Certification 
);

create table Distributor(
  id INT PRIMARY KEY,
  address text,
  bank_account INT UNIQUE ,
  contact_name TEXT,
  contact_phone TEXT
);

create table TransportPackage (
  id serial primary key,
  sale_package SalePackage,
  sale_package_count int,
  check (sale_package_count > 0)
);

create table Shipment (
  id serial,
  package_count int check (package_count > 0),
  package_weight_gr int check ( package_weight_gr > 0),
  sale_packages_in_package int check ( sale_packages_in_package > 0),
  sale_packaging_price int check (sale_packaging_price > 0)
);

create table Warehouse (
  id serial PRIMARY KEY,
  address TEXT
);

create table Pharmacy (
  id serial PRIMARY KEY,
  name TEXT,
  address TEXT, 
  number INT
);

create table PharmacyGood (
  pharmacy_id INT REFERENCES Pharmacy NOT NULL,
  drug_id INT REFERENCES Drug NOT NULL,
  price INT NOT NULL CHECK (price > 0), 
  quantity INT NOT NULL CHECK (quantity >= 0)
);

create table Task (
  id SERIAL PRIMARY KEY,
  car_id INT references Car NOT NULL,
  transport_package_count INT,
  drug_id INT REFERENCES Drug,
  pharmacy_id INT REFERENCES Pharmacy,
  warehouse_id INT REFERENCES Warehouse,
  date DATE
);

create table Pharmacy_Task (
  pharmacy_id INT REFERENCES Pharmacy NOT NULL,
  task_id INT REFERENCES Task NOT NULL
);

create table Car (
  id serial PRIMARY KEY,
  registration_number TEXT,
  last_maintainance_ DATE
);