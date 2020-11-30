insert into MedicalForm(name)
select unnest(ARRAY ['Таблетка', 'Капсула', 'Ампула', 'Порошок']);

insert into Manufacturer(name)
select unnest(ARRAY ['ЗдравФарм', 'Первая Линия', 'Иван Петрович', 'Омский Фарм Завод']);


insert into Lab(name, chief_lastname)
values ('Первая', 'Клочков'),
       ('Вторая', 'Суннари'),
       ('Третья', 'Егоров'),
       ('Четвертая', 'Третьяков');


insert into ChemicalCompound(id, name, formula)
values  (1, 'Ацетилсалициловая кислота', 'C9-H8-O4'),
		(2, 'Пропионовая кислота', 'C3-H6-O2'),
        (3, 'Спирт', 'C2-H5-(OH)'),
        (4, 'Литий', 'Li-OH'),
        (5, 'Морфин ', 'C17-H19-NO3');


insert into Pharmacy(name, address, number)
values ('Озерки', 'пр. Озер, 22', '1'),
       ('У угла', 'ул. Углова, 1', '2'),
       ('Всегда здоров', 'пр. Попова, 17', '3');


with Random as(
    select unnest(ARRAY[333, 47, 42]) as number
)
insert into Certification(number, valid_until, lab_id)
select number, ('2020-11-01'::DATE + random()*365*5 * INTERVAL '1 day')::DATE,
    (0.5 + random() * (select COUNT(*) From Lab))::int From Random;



with Banch as(
    select unnest(ARRAY['Аспирин', 'Нурофен', 'Анальгин', 'Нормотим', 'Опиум' ]) as local_name,
           unnest(ARRAY['Aspirin', 'Nurofen', 'Анальгин', 'Normotim', 'Opium']) as inn, 
		   unnest(ARRAY[333, 47, 42, 42, 333]) as cert
)
insert into Drug(trade_name, international_name, medical_form_id, manufacturer_id, main_chemicalcompound_id, cert_number)
select local_name, inn,
    (random() * (select COUNT(*) From MedicalForm) + 0.5)::int,
    (random() * (select COUNT(*) From Manufacturer) + 0.5)::int,
 	(random() * (select COUNT(*) From chemicalcompound) + 0.5)::int,
	cert
From Banch; 


insert into PharmacyGood(pharmacy_id, drug_id, price, quantity)
values (1, 123, 323, 9), 
       (2, 123, 350, 1), 
       (1, 125, 101, 4), 
       (2, 125, 141, 8), 
       (1, 126, 2700, 11), 
       (3, 126, 2700, 2),
       (1, 127, 1250, 4), 
       (3, 127, 1250, 7);




