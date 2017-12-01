

def write_to_csv(csv_file, country, province, findspot, type_of_inscription, date, inscription):
    csv_file.write(country + "," + province + "," + findspot + "," + type_of_inscription + "," + date + "," + inscription + '\n')
