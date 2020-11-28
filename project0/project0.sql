-- лекарственная форма (это таблетка, капсула, ампула, порошок или что-то еще)
create table MedicalForm (
  id int primary key,
  name text not null
);

-- Производитель имеет имя
create table Manufacturer (
  id serial PRIMARY KEY,
  name text not null
);

-- Таких лабораторий несколько, и вам интересно от каждой лишь её название и фамилия руководителя.
create TABLE Lab (
  id INT PRIMARY KEY,
  name TEXT check (length(name) >= 1),
  chief_lastname TEXT check (length(chief_lastname) >= 1)
);

-- Сертификат с номером, сроком действия и указанием на исследователькую лабораторию, проводившую испытания.
create TABLE Certification (
  number BIGINT PRIMARY KEY,
  valid_until DATE,
  lab_id INT REFERENCES Lab (id)
);

-- Основное действующее средство – это некоторое химическое соединение, у которого есть название и химическая формула.
create TABLE ChemicalCompound (
  id Serial PRIMARY KEY,
  name TEXT UNIQUE check (length(name) >= 1),
  formula TEXT UNIQUE
);

-- У каждого лекарства есть торговое название, международное непатентованное название, лекарственная форма, производитель, некоторое основное действующе вещество и сертификат.
create table Drug (
  id serial PRIMARY KEY,
  trade_name text,
  international_name text,
  medical_form int references MedicalForm,
  manufacturer_id INT references Manufacturer,
  main_chemicalcompound_id INT references ChemicalCompound,
  cert_number INT references Certification
);

-- Юридическое лицо с адресом, номером банковского счета, фамилией и именем контактного лица и его телефоном.
create table Distributor(
  id INT PRIMARY KEY,
  address text check (length(address) > 0),
  bank_account DECIMAL(21,0) UNIQUE check (bank_account < 1e+21) ,
  contact_name TEXT check(length(contact_name) > 1),
  contact_phone TEXT check (length(contact_phone) >= 10 and length(contact_phone) < 20)
);

-- Отпускная упаковка лекарства - это некоторая упаковка лекарства типа: флакон, тюбик, коробочку, и т.д.
create table SalePackage(
  id int primary key,
  name text not null
);

--  Перевозочная упаковка – это "ящик упаковок", которая имеет массу и опредленное число отпускных упаковок определенного лекарства и тип этих упаковок.
create table TransportPackage (
  id serial primary key,
  sale_package int references SalePackage,
  sale_package_count int check (sale_package_count > 0),
  weight int check (weight > 0),
  drug_id INT REFERENCES Drug
);

-- На складах хранятся определенное число различных перевозочных упаковок.
create table WarehousePackages (
  id serial primary key,
  package_count int check (package_count >= 0),
  warehouse_id int references Warehouse,
  transport_package_id int references TransportPackage
);

-- Каждый склад определяется своим адресом и номером.
create table Warehouse (
  id serial PRIMARY KEY,
  address TEXT
);

-- Кладовщик с определенной фамилией работает на складе.
create table Storekeeper (
  id serial PRIMARY KEY,
  lastname text,
  warehouse_id INT REFERENCES Warehouse
);

-- Поставка приезжает на склад, где работает определенный кладовщик в определенную дату.
create table Shipment (
  id serial PRIMARY KEY,
  date_arrived DATE,
  storekeeper_id INT REFERENCES Storekeeper,
  warehouse_id INT REFERENCES Warehouse
);

-- Каждая поставка - это доставка определенного количества перевозочных упаковок определенного лекаства с определенной ценой за упаковку на определенный склад.
create table ShipmentPackages (
  id serial primary key,
  shipment_id INT REFERENCES Shipment,
  transport_package_id int REFERENCES TransportPackage,
  transport_package_count int check (transport_package_count > 0),
  price_sale_package double precision check (price_sale_package > 0)
);

-- Апетка, находящаяся по адресу с номером, известный покупателям, а также с названием.
create table Pharmacy (
  id serial PRIMARY KEY,
  name TEXT UNIQUE,
  address TEXT ,
  number INT check (number >= 0) -- номер апетки
);

-- Определяет текущее состояние аптеки и цены. Комбинированный ключ спасет от ситуации, когда у нас в одной аптеке 2 одинаковых лекарства.
create table PharmacyGood (
  pharmacy_id INT REFERENCES Pharmacy NOT NULL, --id апетки
  drug_id INT REFERENCES Drug NOT NULL, -- id лекарства
  price INT NOT NULL CHECK (price > 0), -- цена лекарства
  quantity INT NOT NULL CHECK (quantity >= 0), -- кол-во
  primary key (pharmacy_id, drug_id)
);

insert into Pharmacy (id, name, address, number) values (1, 'Аптека у Ашота', 'Дембелева 2', 1);
insert into Lab (id, name, chief_lastname) values (1, 'Лаба по химии', 'Менделеев');
insert into Certification (number, valid_until, lab_id) values (1, '1999-01-08', 1);
insert into Drug (id, trade_name, international_name, medical_form, manufacturer_id, main_chemicalcompound_id, cert_number) values (1, 'Ациллококцинум', 'Сахар', 'таблетки', 'РашнКорпорэйшн', 'сахар', 1);
insert into PharmacyGood (pharmacy_id, drug_id, price, quantity) values (1, 1, 99999, 100);

-- Автомобиль с регистрационным номером и датой последнего техобслуживания
create table Car (
  id serial PRIMARY KEY,
  registration_number TEXT check (length(registration_number) between 8 and 9),
  last_maintainance_ DATE
);

-- Задача пополнения лекарства в аптеках с автомобилем со склада в определенное время
create table Task (
  id SERIAL PRIMARY KEY,
  car_id INT references Car NOT NULL,
  warehouse_id INT REFERENCES Warehouse,
  warehouse_fetch_time timestamp
);

-- Список аптек в одной задаче
create table Pharmacy_Task (
  id serial primary key,
  pharmacy_id INT REFERENCES Pharmacy NOT NULL,
  task_id INT REFERENCES Task NOT NULL
);

-- Сколько каких перевозочных упаковок для каждо аптеки в задаче
create table PharmacyTaskPackages (
  drug_id int references Drug,
  pharmacy_task_id int references Pharmacy_Task,
  package_count int check (package_count > 0) not null
);

