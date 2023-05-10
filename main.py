import csv
import pymysql
import json

if __name__ == '__main__':

    connection = pymysql.connect(host='localhost', user='root', password='')
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS pract1")
    cursor.execute("CREATE DATABASE IF NOT EXISTS pract1")

    connection = pymysql.connect(host='localhost', user='root', password='', database='pract1')
    cursor = connection.cursor()

    city_list = ["edinburgh", "santiago"]

    # TABLE host
    query = "CREATE TABLE host (" \
                "id BIGINT PRIMARY KEY," \
                "host_name TEXT," \
                "host_location TEXT," \
                "host_response_time TEXT," \
                "host_has_profile_pic BOOLEAN," \
                "host_identity_verified BOOLEAN" \
            ")"
    cursor.execute(query)

    # TABLE listing
    query = "CREATE TABLE listing (" \
                "id BIGINT PRIMARY KEY," \
                "host_id BIGINT," \
                "property_type TEXT," \
                "room_type TEXT," \
                "accommodates INT," \
                "bathrooms_text TEXT," \
                "bedrooms INT," \
                "price NUMERIC," \
                "minimum_nights INT," \
                "maximum_nights INT," \
                "minimum_nights_avg_ntm FLOAT," \
                "maximum_nights_avg_ntm FLOAT," \
                "FOREIGN KEY (host_id) REFERENCES host (id)" \
            ")"
    cursor.execute(query)

    # TABLE geolocation
    query = "CREATE TABLE geolocation (" \
                "id INT AUTO_INCREMENT PRIMARY KEY," \
                "id_listing BIGINT," \
                "municipality TEXT," \
                "latitude FLOAT," \
                "longitude FLOAT," \
                "neighbourhood TEXT," \
                "neighbourhood_cleansed TEXT," \
                "FOREIGN KEY (id_listing) REFERENCES listing (id)" \
            ")"
    cursor.execute(query)

    # TABLE amenity
    query = "CREATE TABLE amenity (" \
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," \
                "name TEXT UNIQUE" \
            ")"
    cursor.execute(query)

    # TABLE listing_amenity_junction
    query = "CREATE TABLE listing_amenity_junction (" \
                "id_listing BIGINT," \
                "id_amenity BIGINT," \
                "PRIMARY KEY (id_listing, id_amenity)," \
                "FOREIGN KEY (id_listing) REFERENCES listing (id)," \
                "FOREIGN KEY (id_amenity) REFERENCES amenity (id)" \
            ")"
    cursor.execute(query)

    # TABLE availability
    query = "CREATE TABLE availability (" \
                "id_availability INT AUTO_INCREMENT PRIMARY KEY," \
                "id_listing BIGINT," \
                "has_availability BOOLEAN," \
                "availability_30 INT," \
                "availability_60 INT," \
                "availability_90 INT," \
                "availability_365 INT," \
                "FOREIGN KEY (id_listing) REFERENCES listing (id)" \
            ")"
    cursor.execute(query)

    # TABLE reviews
    query = "CREATE TABLE reviews (" \
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
                "FOREIGN KEY (id_listing) REFERENCES listing (id)" \
            ")"
    cursor.execute(query)

    for city in city_list:
        with open(f"csv/{city}.csv", newline='', encoding='utf-8') as file:
            reader_csv = csv.reader(file, delimiter=',')
            next(reader_csv)
            for row in reader_csv:

                # TABLE host
                query = "INSERT IGNORE INTO host (id, host_name, host_location, host_response_time, host_has_profile_pic, host_identity_verified) VALUES (%s, %s, %s, %s, %s, %s)"
                row[25] = '1' if row[25] == 't' else '0'
                row[26] = '1' if row[26] == 't' else '0'
                cursor.execute(query, (row[9], row[11], row[13], row[15], row[25], row[26]))

                # TABLE listing
                query = "INSERT INTO listing (id, host_id, property_type, room_type, accommodates, bathrooms_text, bedrooms, price, minimum_nights, maximum_nights, minimum_nights_avg_ntm, maximum_nights_avg_ntm) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                row[40] = row[40][1:]
                cursor.execute(query, (row[0], row[9], row[32], row[33], row[34], row[36], row[37], row[40].replace("$", "").replace(",", ""), row[41], row[42], row[47], row[48]))

                # TABLE geolocation
                query = "INSERT INTO geolocation (id_listing, municipality, latitude, longitude, neighbourhood, neighbourhood_cleansed) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (row[0], city, row[30], row[31], row[27], row[28]))

                # TABLE amenity, listing_amenity_junction
                json_object = json.loads(row[39])
                for amenity in json_object:
                    # Insert into amenity
                    query = "INSERT IGNORE INTO amenity (name) VALUES (%s)"
                    cursor.execute(query, amenity)
                    # Insert into listing_amenity_junction
                    escapedStr = amenity.replace("'", "\\'")
                    query = fr"SELECT id FROM amenity WHERE name = '{escapedStr}'"
                    cursor.execute(query)
                    id_amenity = cursor.fetchone()[0]
                    query = "INSERT INTO listing_amenity_junction (id_listing, id_amenity) VALUES (%s, %s)"
                    cursor.execute(query, (row[0], id_amenity))

                # TABLE availability
                query = "INSERT INTO availability (id_listing, has_availability, availability_30, availability_60, availability_90, availability_365) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (row[0], row[50], row[51], row[52], row[53], row[54]))

                # TABLE reviews
                query = "INSERT INTO reviews (id_listing, number_of_reviews, review_scores_rating, review_scores_accuracy, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (row[0], row[56], row[61], row[62], row[63], row[64], row[65], row[66], row[67]))

    connection.commit()
    cursor.close()
    connection.close()
