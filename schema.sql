-- лекарственная форма (это таблетка, капсула, ампула, порошок или что-то еще)
create type MedicalForm as ENUM ('powder', 'capsule', 'ampoule', 'pill');


-- Производитель имеет имя
create table Manufacturer (
  id serial PRIMARY KEY,
  name text not null
);

-- Таких лабораторий несколько, и вам интересно от каждой лишь её название и фамилия руководителя.
create TABLE Lab (
  id INT PRIMARY KEY, 
  name TEXT,
  chief TEXT
);

-- У сертификата есть номер, срок действия и указание на исследователькую лабораторию, проводившую испытания.
create TABLE Certification (
  number BIGINT PRIMARY KEY,
  valid_until DATE,
  lab_id INT REFERENCES Lab (id)
);

--Ещё у лекарства есть основное действующее средство – это некоторое химическое соединение, у которого есть название и химическая формула
create TABLE ChemicalCompound (
  id Serial PRIMARY KEY, 
  name TEXT UNIQUE, 
  formula TEXT UNIQUE
);

-- У каждого лекарства есть торговое название, международное непатен- тованное название, лекарственная форма и производитель.
create table Drug (
  id serial PRIMARY KEY,
  trade_name text,
  international_name text,
  medical_form MedicalForm,
  manufacturer_id INT references Manufacturer,
  main_chemicalcompound_id INT references ChemicalCompound,
  cert_number INT references Certification 
);

-- Юридическое лицо с адресом, номером банковского счета, фамилией и именем контактного лица и его телефоном.
create table Distributor(
  id INT PRIMARY KEY,
  address text,
  bank_account INT UNIQUE ,
  contact_name TEXT,
  contact_phone TEXT
);

-- «отпускной упаковкой» лекарства то, что покупает потребитель в аптеке – флакон, тюбик, коробочку, и т.д.
create type SalePackageType as ENUM ('флакон', 'тюбик', 'коробочка');

--  «перевозочной упаковкой» – более крупную тару, в которой помещается какое-то количество отпускных упаковок
create table TransportPackage {
  id serial primary key, 
  sale_package SalePackageType,
  sale_package_count int check (sale_package_count > 0),
  transport_package_weight int check (transport_package_weight > 0),
  drug_id INT REFERENCES Drug,
}


-- Добавить таблицу связку
create table Warehouse (
  id serial PRIMARY KEY,
  address TEXT
);

create table Shipment (
  id serial,
  date_arrived DATE,
  storekeeper_lastname TEXT,
  warehouse_id INT REFERENCES Warehouse
);

-- в каждой поставке есть несколько строчек из данной таблицы (находяться по shipment_id)
-- но у всех таких строчек из одной поставки должен быть различный drug_id
create table ShipmentOfDrug (
  id serial primary key,
  shipment_id INT REFERENCES Shipment,
  box_id int references TransportPackage,
  transport_package_count int check (transport_package_count > 0),
  price_sale_package double check (price_sale_package > 0) 
);


-- У вас есть некоторое количество розничных аптек. У каждой аптеки  имеется адрес и номер, известный покупателям (например, «Аптека за углом №7» по адресу 7-я линия, дом 18).
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


-- Запасы лекарств в аптеках пополняют несколько автомобилей, которые получают задания вида ”такого то числа взять с такого то склада столько то перевозочных упаковок такого-то лекарства для такой то аптеки, столько то для сякой-то, и т.д.”.
create table Task (
  id SERIAL PRIMARY KEY,
  car_id INT references Car NOT NULL,
  warehouse_id INT REFERENCES Warehouse,
  date DATE
);

create table Pharmacy_Task (
  pharmacy_id INT REFERENCES Pharmacy NOT NULL,
  task_id INT REFERENCES Task NOT NULL
);

-- За автомобилями вы тоже следите, и записываете, помимо их регистрационного номера, дату последнего техобслуживания.
create table Car (
  id serial PRIMARY KEY,
  registration_number TEXT,
  last_maintainance_ DATE
);

