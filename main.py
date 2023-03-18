import csv
import pymysql
import json

if __name__ == '__main__':

    connection = pymysql.connect(host='localhost', user='root', password='')
    connection.cursor().execute("CREATE DATABASE IF NOT EXISTS pract1;")

    connection = pymysql.connect(host='localhost', user='root', password='', database='pract1')
    cursor = connection.cursor()

    #TOT EL QUE FA REFERÈNCIA A LA CREACIO I INSERCIÓ DE LA TAULA HOST

    query = "CREATE TABLE IF NOT EXISTS hosts (" \
            "host_id BIGINT PRIMARY KEY," \
            "host_name TEXT," \
            "host_location TEXT," \
            "host_response_time TEXT," \
            "host_has_profile_pic BOOLEAN," \
            "host_identity_verified BOOLEAN);"

    cursor.execute(query)

    cursor.execute("SELECT COUNT(*) FROM hosts")
    rowsHosts = cursor.fetchone()

    if rowsHosts[0] > 0:
        print("la taula hosts ja esta plena")
    else:
        for city in ["edinburgh", "santiago"]:
            with open(city+'.csv', newline='', encoding='utf-8') as file:
                reader_csv = csv.reader(file, delimiter=',')
                next(reader_csv)

                for row in reader_csv:
                    query = "INSERT INTO hosts (host_id, host_name, host_location, host_response_time, host_has_profile_pic, host_identity_verified) " \
                            "VALUES (%s, %s, %s, %s, %s, %s)"

                    row[25] = '1' if row[25] == 't' else '0'
                    row[26] = '1' if row[26] == 't' else '0'

                    try:
                        cursor.execute(query, (
                            row[9], row[11], row[13], row[15], row[25], row[26]))
                    except:
                        continue

    print("dades insertades a hosts correctament")

    #TOT EL QUE FA REFERÈNCIA A LA CREACIÓ I INSERCIÓ DE LA TAULA EDINBURGH

    query = "CREATE TABLE IF NOT EXISTS edinburgh (" \
                "id BIGINT PRIMARY KEY," \
                "property_type TEXT," \
                "room_type TEXT," \
                "accommodates INT," \
                "bathrooms_text TEXT," \
                "bedrooms INT," \
                "price DECIMAL(10,2)," \
                "minimum_nights INT," \
                "maximum_nights INT," \
                "minimum_nights_avg_ntm FLOAT," \
                "maximum_nights_avg_ntm FLOAT," \
                "host_id BIGINT," \
                "FOREIGN KEY (host_id) REFERENCES hosts(host_id))"

    cursor.execute(query)

    cursor.execute("SELECT COUNT(*) FROM edinburgh")
    rowsEdinburgh = cursor.fetchone()

    if rowsEdinburgh[0] > 0:
        print("La taula edinburgh ja esta plena")
    else:
        # Apertura de l'arxiu edinburgh.csv
        with open('edinburgh.csv', newline='', encoding='utf-8') as file:
            reader_csv = csv.reader(file, delimiter=',')
            next(reader_csv)

            for row in reader_csv:
                query = "INSERT INTO edinburgh (id, property_type, room_type, accommodates, bathrooms_text, bedrooms, price, minimum_nights, maximum_nights, minimum_nights_avg_ntm, maximum_nights_avg_ntm, host_id) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                #row[25] = '1' if row[25] == 't' else '0'
                #row[26] = '1' if row[26] == 't' else '0'
                #row[50] = '1' if row[50] == 't' else '0'

                row[40] = row[40][1:]

                cursor.execute(query, (
                    row[0], row[32], row[33], row[34], row[36], row[37], row[40], row[41], row[42], row[47], row[48], row[9]))

        print("dades insertades a edinburgh correctament")

    # TOT EL QUE FA REFERÈNCIA A LA CREACIÓ I INSERCIÓ DE LA TAULA SANTIAGO

    query = "CREATE TABLE IF NOT EXISTS santiago LIKE edinburgh;"
    cursor.execute(query)

    cursor.execute("SELECT COUNT(*) FROM santiago")
    rowsSantiago = cursor.fetchone()

    if rowsSantiago[0] > 0:
        print("taula santiago ja esta plena")
    else:
        with open('santiago.csv', newline='', encoding='utf-8') as file:
            reader_csv = csv.reader(file, delimiter=',')
            next(reader_csv)

            for row in reader_csv:
                query = "INSERT INTO santiago (id, property_type, room_type, accommodates, bathrooms_text, bedrooms, price, minimum_nights, maximum_nights, minimum_nights_avg_ntm, maximum_nights_avg_ntm, host_id) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                #row[25] = '1' if row[25] == 't' else '0'
                #row[26] = '1' if row[26] == 't' else '0'
                #row[50] = '1' if row[50] == 't' else '0'

                row[40] = row[40][1:]

                cursor.execute(query, (
                    row[0], row[32], row[33], row[34], row[36], row[37], row[40], row[41], row[42], row[47], row[48], row[9]))

        print("dades insertades a santiago correctament")

    # TOT EL QUE FA REFERÈNCIA A LA CREACIÓ I INSERCIÓ DE LA TAULA LISTING_AMENITIES

    for city in ["edinburgh", "santiago"]:
        query = "CREATE TABLE IF NOT EXISTS listing_amenities_"+city+" (" \
                "id_amenity INT AUTO_INCREMENT PRIMARY KEY," \
                "id_listing BIGINT," \
                "amenity_name TEXT," \
                "FOREIGN KEY (id_listing) REFERENCES "+city+" (id))"

        cursor.execute(query)

        cursor.execute("SELECT COUNT(*) FROM listing_amenities_"+city)
        rowsAmenities = cursor.fetchone()

        if rowsAmenities[0] > 0:
            print("la taula listing_amenities_"+city+" ja esta plena")
        else:
            with open(city + '.csv', newline='', encoding='utf-8') as file:
                reader_csv = csv.reader(file, delimiter=',')
                next(reader_csv)

                for row in reader_csv:
                    json_object = json.loads(row[39])
                    for amenity in json_object:
                        query = "INSERT INTO listing_amenities_" + city + " (id_listing, amenity_name) " \
                            "VALUES (%s, %s)"

                        cursor.execute(query, (
                            row[0], amenity))

            print("dades insertades a listing_amenities_" + city + " correctament")

    # TOT EL QUE FA REFERÈNCIA A LA CREACIÓ I INSERCIÓ DE LA TAULA GEOLOCATION

    for city in ["edinburgh", "santiago"]:
        query = "CREATE TABLE IF NOT EXISTS geolocation_" + city + " (" \
                "id_geolocation INT AUTO_INCREMENT PRIMARY KEY," \
                "id_listing BIGINT," \
                "latitude FLOAT," \
                "longitude FLOAT," \
                "neighbourhood TEXT," \
                "FOREIGN KEY (id_listing) REFERENCES " + city + " (id))"

        cursor.execute(query)

        cursor.execute("SELECT COUNT(*) FROM geolocation_" + city)
        rowsGeolocation = cursor.fetchone()

        if rowsGeolocation[0] > 0:
            print("la taula geolocation_"+city+" ja esta plena")

        else:
            with open(city + '.csv', newline='', encoding='utf-8') as file:
                reader_csv = csv.reader(file, delimiter=',')
                next(reader_csv)

                for row in reader_csv:
                    query = "INSERT INTO geolocation_" + city + " (id_listing, latitude, longitude, neighbourhood ) " \
                            "VALUES (%s, %s, %s, %s)"

                    cursor.execute(query, (
                        row[0], row[30], row[31], row[27]))

            print("dades insertades a geolocation_" + city + "correctament")

    # TOT EL QUE FA REFERÈNCIA A LA CREACIÓ I INSERCIÓ DE LA TAULA AVAILABILITIES

    for city in ["edinburgh", "santiago"]:
        query = "CREATE TABLE IF NOT EXISTS availability_" + city + " (" \
                "id_availability INT AUTO_INCREMENT PRIMARY KEY," \
                "id_listing BIGINT," \
                "has_availability BOOLEAN," \
                "availability_30 INT," \
                "availability_60 INT," \
                "availability_90 INT," \
                "availability_365 INT," \
                "FOREIGN KEY (id_listing) REFERENCES " + city + " (id))"

        cursor.execute(query)

        cursor.execute("SELECT COUNT(*) FROM availability_" + city)
        rowsGeolocation = cursor.fetchone()

        if rowsGeolocation[0] > 0:
            print("la taula availability_" + city + " ja esta plena")

        else:
            with open(city + '.csv', newline='', encoding='utf-8') as file:
                reader_csv = csv.reader(file, delimiter=',')
                next(reader_csv)

                for row in reader_csv:
                    query = "INSERT INTO availability_" + city + "(id_listing, has_availability, availability_30, availability_60, availability_90, availability_365) " \
                                                                "VALUES (%s, %s, %s, %s, %s, %s)"

                    cursor.execute(query, (
                        row[0], row[50], row[51], row[52], row[53], row[54]))

            print("dades insertades a availability_" + city + " correctament")

        # TOT EL QUE FA REFERÈNCIA A LA CREACIÓ I INSERCIÓ DE LA TAULA REVIEWS

    for city in ["edinburgh", "santiago"]:
        query = "CREATE TABLE IF NOT EXISTS reviews_" + city + " (" \
                "id_reviews INT AUTO_INCREMENT PRIMARY KEY," \
                "id_listing BIGINT," \
                "number_of_reviews FLOAT," \
                "review_scores_rating FLOAT," \
                "review_scores_accuracy FLOAT," \
                "review_scores_cleanliness FLOAT," \
                "review_scores_checkin FLOAT," \
                "review_scores_communication FLOAT," \
                "review_scores_location FLOAT," \
                "review_scores_value FLOAT," \
                "FOREIGN KEY (id_listing) REFERENCES " + city + " (id))"

        cursor.execute(query)

        cursor.execute("SELECT COUNT(*) FROM reviews_" + city)
        rowsGeolocation = cursor.fetchone()

        if rowsGeolocation[0] > 0:
            print("la taula reviews_" + city + " ja esta plena")

        else:
            with open(city + '.csv', newline='', encoding='utf-8') as file:
                reader_csv = csv.reader(file, delimiter=',')
                next(reader_csv)

                for row in reader_csv:
                    query = "INSERT INTO reviews_" + city + "(id_listing, number_of_reviews, review_scores_rating, review_scores_accuracy, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value) " \
                                                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    cursor.execute(query, (
                        row[0], row[56], row[61], row[62], row[63], row[64], row[65], row[66], row[67]))

        print("dades insertades a reviews_" + city + " correctament")


    #Estudi de les variables individualitzades amb R

    #Estudi mitjana de preus per nit dels allotjaments d’edinburgh
    cursor.execute("SELECT AVG(price) FROM edinburgh")

    price = cursor.fetchone()
    print("\n\nLa mitjana de preus per nit a edinburgh es:",  price[0], "\n")

    # Estudi tipus d'habitacions més habituals. És dur a terme un recompte de cada tipus diferent de valor VARCHAR
    #i s'agrupa pel camp room_type. Posteriorment es classifica aquesta agrupació de forma descendent depenent
    #del comptatge de cadascuna i s'usa la clàusula LIMIT 1 per seleccionar el valor més habitual
    cursor.execute(
        "SELECT room_type, COUNT(*) as quantity FROM edinburgh GROUP BY room_type ORDER BY quantity DESC LIMIT 1")

    result = cursor.fetchone()
    print("El tipus d'habitacio mes habitual a Edinburgh es:", result[0], "amb un total de", result[1], "comptatges\n")

    #Estudi del nombre de propietaris que tenen mes de 60 allotjaments.
    cursor.execute("SELECT host_name, COUNT(*) as quantity FROM hosts GROUP BY host_name HAVING quantity > 60")
    results = cursor.fetchall()
    for result in results:
        print("El propietari", result[0], "te", result[1], "allotjaments")


    #Estudi de la relacio entre millors valorats amb resposta rapida dels hosts.
    # cursor.execute("SELECT host_name, host_response_time, review_scores_value FROM edinburgh GROUP BY host_id AVG(review_scores_value)")
    # results = cursor.fetchall()
    # for result in results:
    #      print("El propietari", result[0], "te un temps de resposta de", result[1], "i una review de", result[2])

    #Estudi per saber si hi ha un propietari amb 2 allotjaments (1 a edinburgh i l'altre a santiago)
    cursor.execute("SELECT DISTINCT h.host_id FROM hosts h JOIN edinburgh e ON h.host_id = e.host_id JOIN santiago s ON h.host_id = s.host_id")
    results = cursor.fetchall()
    for result in results:
        print("El propietari amb id", result[0], "te 2 allotjaments. 1 a ediburgh i l'altre a santiago")


    # Estudi per saber quins preus per nit són més elevats de mitjana, si a santiago o a edinburgh
    # cursor.execute("SELECT CASE WHEN AVG(e.price) > AVG(s.price) THEN AVG(e.price) ELSE AVG(s.price) END AS max_avg_price FROM edinburgh e, santiago s")
    # priceEdinburgh = cursor.fetchone()
    # print("Preu per nit mitjà a edinburgh", priceEdinburgh)


    # Confirmació de la transacció
    connection.commit()

    # Tancament cursor i la connexió
    cursor.close()
    connection.close()
