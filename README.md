Random Data Generator with Python
Bu Python programı, rastgele kişi bilgisi oluşturmak için kullanılır. Oluşturulan kişi bilgileri, belirtilen bir CSV dosyasından alınan ilk isim, soyisim ve cinsiyet bilgileri kullanılarak rastgele oluşturulur. Her bir kişiye benzersiz kimlik numarası, telefon numarası ve doğum tarihi atanır. Ayrıca, rastgele bir şehir ve ilçe/semt çifti de her kişiye eklenir.

Nasıl Kullanılır
Python'un kurulu olduğundan ve gerekli kütüphanelerin yüklü olduğundan emin olun (kütüphaneler: random, csv, datetime, timedelta, pandas).

persons.csv adlı bir CSV dosyası oluşturun ve içine en azından şunları içeren kişi bilgilerini ekleyin:

fnames (ilk isim)
lnames (soyisim)
gender (cinsiyet)
cities_town.csv adlı bir CSV dosyası oluşturun ve içine en azından şunları içeren şehir-ilçe/semt çiftlerini ekleyin:

city (şehir)
town (ilçe/semt)
main fonksiyonunu çalıştırarak rastgele kişi bilgileri oluşturun ve random_persons.csv adlı bir CSV dosyasına kaydedin.

Oluşturulan kişi bilgilerini random_persons.csv dosyasında bulabilirsiniz.

# Açıklama
generate_random_birthdate(): Rastgele bir doğum tarihi oluşturur.

generate_random_identity_number(existing_numbers): Rastgele bir kimlik numarası oluşturur ve benzersiz olduğundan emin olur.

generate_random_phone_number(existing_numbers): Rastgele bir telefon numarası oluşturur ve benzersiz olduğundan emin olur.

read_person_info_from_file(file_name): Kişi bilgilerini bir CSV dosyasından okur.

create_random_person(existing_numbers, person_info_list, city_town_pairs): Rastgele bir kişi bilgisi oluşturur.

main(): Ana işlemi yürütür, kişi bilgilerini oluşturur ve random_persons.csv dosyasına kaydeder.
