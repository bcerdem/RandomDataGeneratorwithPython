import random
import csv
from datetime import datetime, timedelta

# İlaç ve tanı yüzdelerini hesaplayan fonksiyon
def calculate_medical_percentages(file_path):
    ilac_eslesmeleri = {}
    with open(file_path, 'r', encoding='utf-8') as dosya:
        satirlar = dosya.readlines()
        
    for satir in satirlar[1:]:  # Başlık satırını atla
        _, _, ilac_adi, tanı_kodu, icd10_adi = satir.strip().split('\t')
        
        if ilac_adi in ilac_eslesmeleri:
            ilac_eslesmeleri[ilac_adi]['EŞLEŞME SAYISI'] += 1
        else:
            ilac_eslesmeleri[ilac_adi] = {
                'EŞLEŞME SAYISI': 1,
                'TANI KODU': tanı_kodu,
                'ICD10 ADI': icd10_adi
            }
    
    toplam_eslesme = sum([veri['EŞLEŞME SAYISI'] for veri in ilac_eslesmeleri.values()])
    
    ilac_yuzdesel_oranlari = {
        ilac_adi: {
            'EŞLEŞME SAYISI': veri['EŞLEŞME SAYISI'],
            'TANI KODU': veri['TANI KODU'],
            'ICD10 ADI': veri['ICD10 ADI'],
            'YÜZDE': (veri['EŞLEŞME SAYISI'] / toplam_eslesme) * 100
        } for ilac_adi, veri in ilac_eslesmeleri.items()
    }
    
    return ilac_yuzdesel_oranlari

# Rasgele kişi bilgisi oluşturan kod
def generate_random_birthdate():
    start_date = datetime(1930, 1, 1)
    end_date = datetime(2023, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    birth_date = start_date + timedelta(days=random_days)
    return birth_date.strftime("%Y-%m-%d")

def generate_random_identity_number(existing_numbers):
    while True:
        first_digit = str(random.randint(1, 8))
        id_number = [first_digit]

        for _ in range(10):
            random_digit = random.randint(0, 9)
            id_number.append(str(random_digit))

        id_number = "".join(id_number)

        if id_number not in existing_numbers:
            existing_numbers.add(id_number)
            break

    return id_number

def generate_random_phone_number(existing_numbers):
    while True:
        phone_number = ["5"]
        second_digit = random.choice(["3", "4", "5"])
        phone_number.append(second_digit)

        for _ in range(8):
            random_digit = random.randint(0, 9)
            phone_number.append(str(random_digit))

        phone_number = "".join(phone_number)

        if phone_number not in existing_numbers:
            existing_numbers.add(phone_number)
            break

    return phone_number

def read_names_from_file(file_name):
    with open(file_name, "r", encoding="utf-8") as name_file:
        names = name_file.read().splitlines()
    return names

def create_random_person(existing_numbers, male_names, female_names, surnames, city_town_pairs, ilac_yuzdesel_oranlari):
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

    selected_city_town = random.choice(city_town_pairs)
    city = selected_city_town['city']
    town = selected_city_town['town']

    ilac_bilgileri = random.choices(list(ilac_yuzdesel_oranlari.keys()), weights=[x['YÜZDE'] for x in ilac_yuzdesel_oranlari.values()])[0]
    ilac_adi = ilac_bilgileri
    tanı_kodu = ilac_yuzdesel_oranlari[ilac_bilgileri]['TANI KODU']
    icd10_adi = ilac_yuzdesel_oranlari[ilac_bilgileri]['ICD10 ADI']

    person_info = {
        "İsim": first_name,
        "Soyisim": last_name,
        "Cinsiyet": gender,
        "Telefon": phone_number,
        "Doğum Tarihi": birth_date,
        "Kimlik Numarası": id_number,
        "City": city,
        "Town": town,
        "İlaç Adı": ilac_adi,
        "Tanı Kodu": tanı_kodu,
        "ICD10 ADI": icd10_adi
    }

    return person_info

def main():
    file_path = 'C:\Workspace\Labs\MyProjects\RandomDataGeneratorwithPython\databases\med_ıcd10'
    ilac_yuzdesel_oranlari = calculate_medical_percentages(file_path)

    male_names = read_names_from_file("C:/Workspace/Labs/MyProjects/RandomDataGeneratorwithPython/databases/male_names")
    female_names = read_names_from_file("C:/Workspace/Labs/MyProjects/RandomDataGeneratorwithPython/databases/female_names")
    surnames = read_names_from_file("C:/Workspace/Labs/MyProjects/RandomDataGeneratorwithPython/databases/surnames")

    existing_numbers = set()

    cities_towns = []

    with open('C:/Workspace/Labs/MyProjects/RandomDataGeneratorwithPython/databases/cities_towns.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            city = row['city']
            town = row['town']
            cities_towns.append({'city': city, 'town': town})

    person_info_dict = {}
    surname_city_mapping = {}

    for _ in range(10000):
        person_info = create_random_person(existing_numbers, male_names, female_names, surnames, cities_towns, ilac_yuzdesel_oranlari)
        person_info_dict[person_info['Kimlik Numarası']] = person_info

        surname = person_info['Soyisim']
        if surname not in surname_city_mapping:
            surname_city_mapping[surname] = []
        surname_city_mapping[surname].append(person_info['City'])

    for surname, cities in surname_city_mapping.items():
        if len(cities) > 1:
            common_city = random.choice(cities)
            for person_info in person_info_dict.values():
                if person_info['Soyisim'] == surname:
                    person_info['City'] = common_city

    sql_script_file = "C:/Workspace/Labs/MyProjects/RandomDataGeneratorwithPython/databases/insert_script.sql"

    with open(sql_script_file, "w", encoding="utf-8") as sql_script:
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
            TOWN NVARCHAR(50),
            ILAC_ADI NVARCHAR(100),
            TANI_KODU NVARCHAR(10),
            ICD10_ADI NVARCHAR(100)
        )\nGO\n'''
        sql_script.write(create_db_script)
        sql_script.write(use_db)
        sql_script.write(create_table_script)

        for person_info in person_info_dict.values():
            sql_script.write("INSERT INTO MyTableTest (FNAME,LNAME,GENDER,PHONENUMBER,BIRTHDATE,IDNUMBER,CITY,TOWN,ILAC_ADI,TANI_KODU,ICD10_ADI) VALUES (")
            sql_script.write(f"'{person_info['İsim']}', '{person_info['Soyisim']}', '{person_info['Cinsiyet']}', ")
            sql_script.write(
                f"'{person_info['Telefon']}', '{person_info['Doğum Tarihi']}', '{person_info['Kimlik Numarası']}', ")
            sql_script.write(f"'{person_info['City']}', '{person_info['Town']}', ")
            sql_script.write(f"'{person_info['İlaç Adı']}', '{person_info['Tanı Kodu']}', '{person_info['ICD10 ADI']}');\n")

    print("SQL scripti oluşturuldu: insert_script.sql")

if __name__ == "__main__":
    main()
