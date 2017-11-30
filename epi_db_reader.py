import json
import requests


LIMIT = 100  # items per request
START = 100  # start year
END = 200  # end year


def build_url(our_offset=0):
    not_before = 'year_not_before=' + str(START)
    not_after = 'year_not_after=' + str(END)
    url = 'http://edh-www.adw.uni-heidelberg.de/data/api/inscriptions/search?' + not_before + '&' + not_after
    return url + '&offset=' + str(our_offset) + '&limit=' + str(LIMIT)


def get_sub_results(url, item_from_dictionary):
    results = requests.get(url)
    results_dic = json.loads(results.text)
    return results_dic[item_from_dictionary]


def get_item_results(our_offset):
    url = build_url(our_offset)
    return get_sub_results(url, 'items')


def get_total_item_count():
    url = build_url()
    return get_sub_results(url, 'total')


def clean_inscription(inscr):
    return str.replace(inscr, '[', '').replace(']', '').replace('(', '').replace(')', '').replace('/', '') \
        .replace('{', '').replace('}', '').replace('\n', ' ').replace('"GR"', '').replace('"', '').replace('  ', ' ')\
        .replace(',', '').strip()


def write_to_csv(csv_file, country, province, findspot, type_of_inscription, date, inscription):
    csv_file.write(country + "," + province + "," + findspot + "," + type_of_inscription + "," + date + "," + inscription + '\n')


def get_date(a_date):
    return str(int(a_date))


def get_average_date(start, end):
    start = int(start)
    end = int(end)
    return str(int(start + (end - start) / 2))


def remove_commas(a_string):
    return a_string.replace(',', '')


def loop_over_items(items):
    count = 0
    errors = 0
    csv_file = open('files/epi_data.csv', 'a')

    for item in items:
        try:
            country = remove_commas(item['country'])
            province = remove_commas(item['province_label'])
            findspot = remove_commas(item['findspot'])
            #     'modern_region': 'Lazio',
            #     'findspot_modern': 'Roma',
            type_of_inscription = remove_commas(item['type_of_inscription'])
            date = get_date(item['not_before'])
            inscription = clean_inscription(item['transcription'])

            write_to_csv(csv_file, country, province, findspot, type_of_inscription, date, inscription)
            count += 1
        except KeyError as err:
            # so one of our keys is missing, disregard this inscription
            errors += 1

    print('successful: ' + str(count) + ', with unavailable data: ' + str(errors))
    csv_file.close()


offset = 0
total_raw = get_total_item_count()
total = int(total_raw / 100) * 100

print("Total number of items (rounded down): " + str(total))

while offset < total:
    print('now at inscription ' + str(offset))
    loop_over_items(get_item_results(offset))
    offset += LIMIT
