import csv
import pymysql


if __name__ == '__main__':

    # Conexión a la base de datos
    connection = pymysql.connect(host='localhost', user='root', password='', database='pract1')

    # Creación del objeto cursor
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM edinburgh")
    rowsEdinburgh = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM santiago")
    rowsSantiago = cursor.fetchone()


    if (rowsEdinburgh[0] > 0):
        print("La taula edinburgh ja esta plena")
    else:
        # Apertura de l'arxiu edinburgh.csv
        with open('edinburgh.csv', newline='', encoding='utf-8') as file:
            reader_csv = csv.reader(file, delimiter=',')
            next(reader_csv)

            for row in reader_csv:
                query = "INSERT INTO edinburgh (id, host_id, host_name, host_location, host_response_time, host_has_profile_pic, host_identity_verified, latitude, longitude, neighbourhood, neighbourhood_cleansed, property_type, room_type, accommodates, bathrooms_text, bedrooms, amenities, price, minimum_nights, maximum_nights, minimum_nights_avg_ntm, maximum_nights_avg_ntm, has_availability, availability_30, availability_60, availability_90, availability_365, number_of_reviews, review_scores_rating, review_scores_accuracy, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value, reviews_per_month) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                row[25] = '1' if row[25] == 't' else '0'
                row[26] = '1' if row[26] == 't' else '0'
                row[50] = '1' if row[50] == 't' else '0'

                row[40] = row[40][1:]
                # TODO les rows 30 i 31 (latitude i longitude) i les rows de l'score (60-67) es llegeixen en format decimal i no pas en int. S'ha de mirar

                cursor.execute(query, (
                    row[0], row[9], row[11], row[13], row[15], row[25], row[26], row[30], row[31], row[27], row[28], row[32],
                    row[33], row[34], row[36], row[37], row[39], row[40], row[41], row[42], row[47], row[48], row[50],
                    row[51], row[52], row[53], row[54], row[56], row[61], row[62], row[63], row[64], row[65],
                    row[66], row[67], row[74]))

                print("edinburgh")

    if (rowsSantiago[0] > 0):
        print("taula santiago ja esta plena")
    else:
        with open('santiago.csv', newline='', encoding='utf-8') as file:
            reader_csv = csv.reader(file, delimiter=',')
            next(reader_csv)

            for row in reader_csv:
                query = "INSERT INTO santiago (id, host_id, host_name, host_location, host_response_time, host_has_profile_pic, host_identity_verified, latitude, longitude, neighbourhood, neighbourhood_cleansed, property_type, room_type, accommodates, bathrooms_text, bedrooms, amenities, price, minimum_nights, maximum_nights, minimum_nights_avg_ntm, maximum_nights_avg_ntm, has_availability, availability_30, availability_60, availability_90, availability_365, number_of_reviews, review_scores_rating, review_scores_accuracy, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value, reviews_per_month) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                row[25] = '1' if row[25] == 't' else '0'
                row[26] = '1' if row[26] == 't' else '0'
                row[50] = '1' if row[50] == 't' else '0'

                row[40] = row[40][1:]
                # TODO les rows 30 i 31 (latitude i longitude) i les rows de l'score (60-67) es llegeixen en format decimal i no pas en int. S'ha de mirar

                cursor.execute(query, (
                    row[0], row[9], row[11], row[13], row[15], row[25], row[26], row[30], row[31], row[27],
                    row[28], row[32],
                    row[33], row[34], row[36], row[37], row[39], row[40], row[41], row[42], row[47], row[48],
                    row[50],
                    row[51], row[52], row[53], row[54], row[56], row[61], row[62], row[63], row[64], row[65],
                    row[66], row[67], row[74]))

                print("santiago")

    #Estudi de les variables individualitzades amb R

    #Estudi mitjana de preus per nit dels allotjaments d’edinburgh
    cursor.execute("SELECT AVG(price) FROM edinburgh")

    price = cursor.fetchone()
    print("La mitjana de preus per nit a edinburgh es:",  price[0], "\n")

    # Estudi tipus d'habitacions més habituals. Es dur a terme un recompte de cada tipus diferent de valor VARCHAR
    #i s'agrupa pel camp room_type. Posteriorment es classifica aquesta agrupació de forma descendent depenent
    #del comptatge de cadascuna i s'usa la clàusula LIMIT 1 per seleccionar el valor més habitual
    cursor.execute(
        "SELECT room_type, COUNT(*) as quantity FROM edinburgh GROUP BY room_type ORDER BY quantity DESC LIMIT 1")

    result = cursor.fetchone()
    print("El tipus d'habitacio mes habitual es:", result[0], "amb un total de", result[1], "comptatges\n")

    #Estudi del nombre de propietaris que tenen mes de 60 allotjaments.
    #cursor.execute("SELECT host_name, COUNT(*) as quantity FROM edinburgh GROUP BY host_name HAVING quantity > 60")
    #results = cursor.fetchall()

    #for result in results:
    #   print("El propietari", result[0], "te", result[1], "allotjaments")


    #TODO estudi cagat per la row de l'score. Python l'obte amb float quan hauria de ser int.
    #Estudi de la relacio entre millors valorats amb resposta rapida dels hosts.
    #cursor.execute("SELECT host_name, host_response_time, review_scores_value FROM edinburgh")
    #results = cursor.fetchall()
    #for result in results:
    #    print("El propietari", result[0], "te un temps de resposta de", result[1], "i una review de", result[2])

    #Estudi per saber si hi ha un propietari amb 2 allotjaments (1 a edinburgh i l'altre a santiago)
    cursor.execute("SELECT DISTINCT edinburgh.id FROM edinburgh INNER JOIN santiago ON edinburgh.id = santiago.id")
    results = cursor.fetchall()
    for result in results:
        print("El propietari amb id", result[0], "te 2 allotjaments. 1 a ediburgh i l'altre a santiago")


    # Estudi per saber quins preus per nit són més elevats de mitjana, si a santiago o a edinburgh
    cursor.execute("SELECT CASE WHEN AVG(e.price) > AVG(s.price) THEN AVG(e.price) ELSE AVG(s.price) END AS max_avg_price FROM edinburgh e, santiago s")
    priceEdinburgh = cursor.fetchone()
    print("Preu per nit mitjà a edinburgh", priceEdinburgh)


    # Confirmació de la transacció
    connection.commit()

    # Tancament cursor i la connexió
    cursor.close()
    connection.close()