import random
import csv
from datetime import datetime, timedelta

# Rastgele doğum tarihi üreten bir fonksiyon
def generate_random_birthdate():
    start_date = datetime(1930, 1, 1)
    end_date = datetime(2023, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    birth_date = start_date + timedelta(days=random_days)
    return birth_date.strftime("%Y-%m-%d")

# Rastgele kimlik numarası üreten bir fonksiyon
def generate_random_identity_number(existing_numbers):
    while True:
        ilk_indeks = str(random.randint(1, 8))
        kimlik_numarasi = [ilk_indeks]

        for _ in range(10):
            rastgele_indeks = random.randint(0, 9)
            kimlik_numarasi.append(str(rastgele_indeks))

        kimlik_numarasi = "".join(kimlik_numarasi)

        if kimlik_numarasi not in existing_numbers:
            existing_numbers.add(kimlik_numarasi)
            break

    return kimlik_numarasi

# Rastgele telefon numarası üreten bir fonksiyon
def generate_random_phone_number(existing_numbers):
    while True:
        telefon_numarasi = ["5"]
        ikinci_indeks = random.choice(["3", "4", "5"])
        telefon_numarasi.append(ikinci_indeks)

        for _ in range(8):
            rastgele_indeks = random.randint(0, 9)
            telefon_numarasi.append(str(rastgele_indeks))

        telefon_numarasi = "".join(telefon_numarasi)

        if telefon_numarasi not in existing_numbers:
            existing_numbers.add(telefon_numarasi)
            break

    return telefon_numarasi

# İsimleri dosyadan okuyan bir fonksiyon
def read_names_from_file(file_name):
    with open(file_name, "r", encoding="utf-8") as name_file:
        names = name_file.read().splitlines()
    return names

# Kişiyi oluşturan bir fonksiyon
def create_random_person(existing_numbers, male_names, female_names, surnames, city_town_pairs):
    is_male = random.choice([True, False])
    if is_male:
        first_name = random.choice(male_names)
        gender = "E"
    else:
        first_name = random.choice(female_names)
        gender = "K"
    last_name = random.choice(surnames)

    phone_number = generate_random_phone_number(existing_numbers)
    birth_date = generate_random_birthdate()
    id_number = generate_random_identity_number(existing_numbers)

    # Rastgele bir şehir ve ilçe seç
    selected_city_town = random.choice(city_town_pairs)
    city = selected_city_town['city']
    town = selected_city_town['town']

    person_info = {
        "İsim": first_name,
        "Soyisim": last_name,
        "Cinsiyet": gender,
        "Telefon": phone_number,
        "Doğum Tarihi": birth_date,
        "Kimlik Numarası": id_number,
        "City": city,
        "Town": town
    }

    return person_info

# Dosyadan isimleri okuma
male_names = read_names_from_file("male_names")
female_names = read_names_from_file("female_names")
surnames = read_names_from_file("surnames")

existing_numbers = set()

# "cities_towns.csv" dosyasındaki il ve ilçe bilgilerini yükleyin
cities_towns = []

with open('cities_towns.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
        city = row['city']
        town = row['town']
        cities_towns.append({'city': city, 'town': town})

# Kişileri oluşturun ve bilgilerini bir sözlükte saklayın
person_info_dict = {}
surname_city_mapping = {}

for _ in range(1000):
    person_info = create_random_person(existing_numbers, male_names, female_names, surnames, cities_towns)
    person_info_dict[person_info['Kimlik Numarası']] = person_info

    # Soyisim ile şehir ilişkisini kaydet
    surname = person_info['Soyisim']
    if surname not in surname_city_mapping:
        surname_city_mapping[surname] = []
    surname_city_mapping[surname].append(person_info['City'])

# Soyisimleri aynı olanları aynı şehirde yap
for surname, cities in surname_city_mapping.items():
    if len(cities) > 1:
        common_city = random.choice(cities)
        for person_info in person_info_dict.values():
            if person_info['Soyisim'] == surname:
                person_info['City'] = common_city

# SQL scriptini oluşturmak için kullanılacak dosya adı
sql_script_dosya_adi = "insert_script.sql"

# SQL scriptini oluşturma
with open(sql_script_dosya_adi, "w", encoding="utf-8") as sql_script:
    create_db_script = "CREATE DATABASE MyDatabaseTest;\nGO\n"
    use_db = "USE MyDatabaseTest;\nGO\n"
    create_table_script = '''
    CREATE TABLE MyTableTest(
        ID INT PRIMARY KEY IDENTITY(1,1),
        FNAME NVARCHAR(50),
        LNAME NVARCHAR(50),
        GENDER NVARCHAR(1),
        PHONENUMBER NVARCHAR(10),
        BIRTHDATE DATE,
        IDNUMBER NVARCHAR(11),
        CITY NVARCHAR(50),
        TOWN NVARCHAR(50)
    )\nGO\n'''
    sql_script.write(create_db_script)
    sql_script.write(use_db)
    sql_script.write(create_table_script)

    for person_info in person_info_dict.values():
        sql_script.write("INSERT INTO MyTableTest (FNAME,LNAME,GENDER,PHONENUMBER,BIRTHDATE,IDNUMBER,CITY,TOWN) VALUES (")
        sql_script.write(f"'{person_info['İsim']}', '{person_info['Soyisim']}', '{person_info['Cinsiyet']}', ")
        sql_script.write(
            f"'{person_info['Telefon']}', '{person_info['Doğum Tarihi']}', '{person_info['Kimlik Numarası']}', ")
        sql_script.write(f"'{person_info['City']}', '{person_info['Town']}');\n")

print("SQL scripti oluşturuldu: insert_script.sql")
