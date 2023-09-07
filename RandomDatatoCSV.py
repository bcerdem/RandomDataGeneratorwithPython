import random
import csv
from datetime import datetime, timedelta
import pandas as pd

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

def read_person_info_from_file(file_name):
    person_info_list = []
    with open(file_name, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            first_name = row['fnames']
            last_name = row['lnames']
            person_info_list.append({'FNAME': first_name, 'LNAME': last_name, 'GENDER': row['gender']})
    return person_info_list

def create_random_person(existing_numbers, person_info_list, city_town_pairs):
    person_info = random.choice(person_info_list)
    gender = person_info['GENDER']
    first_name = person_info['FNAME']
    last_name = person_info['LNAME']
    phone_number = generate_random_phone_number(existing_numbers)
    birth_date = generate_random_birthdate()
    id_number = generate_random_identity_number(existing_numbers)
    selected_city_town = random.choice(city_town_pairs)
    city, town = selected_city_town['city'], selected_city_town['town']

    person_info = {
        "FNAME": first_name,
        "LNAME": last_name,
        "GENDER": gender,
        "TELNO": phone_number,
        "BIRTHDATE": birth_date,
        "IDNUMBER": id_number,
        "CITY": city,
        "TOWN": town
    }

    return person_info

def main():
    person_info_list = read_person_info_from_file("databases\persons.csv")

    existing_numbers = set()
    cities_towns = []

    with open('databases\cities_town.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            city, town = row['city'], row['town']
            cities_towns.append({'city': city, 'town': town})

    generated_persons = []

    for _ in range(10000):
        person_info = create_random_person(existing_numbers, person_info_list, cities_towns)
        generated_persons.append(person_info)

    df = pd.DataFrame(generated_persons)
    df.to_csv('outputs\\random_persons.csv', index=False)

    print("CSV dosyası oluşturuldu: random_persons.csv")
    print(df)

if __name__ == "__main__":
    main()
