import json
import requests
from helpers import cleaners, writers

# constants
START = 100  # start year
END = 200  # end year
LIMIT = 100  # items per request

FILE_NAME = 'files/epi_data.csv'  # file with resulting data

# attributes of each item that will be checked - if you change this, also change schema.json

FIELDS_TO_CHECK = dict()
FIELDS_TO_CHECK['date'] = ['not_before']
FIELDS_TO_CHECK['normal'] = ['country', 'province_label', 'findspot', 'type_of_inscription']
FIELDS_TO_CHECK['thorough_clean'] = ['transcription']


def build_url(our_offset=0):
    url = 'http://edh-www.adw.uni-heidelberg.de/data/api/inscriptions/search?'
    suffix = 'year_not_before=%s&year_not_after=%s&offset=%s&limit=%s' \
             % (str(START), str(END), str(our_offset), str(LIMIT))
    return url + suffix


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


def loop_over_items(items):
    count = 0
    errors = 0

    csv_file = open(FILE_NAME, 'a')

    for item in items:
        try:
            values = []

            for date in FIELDS_TO_CHECK['date']:
                values.append(cleaners.get_date(item[date]))

            for normal in FIELDS_TO_CHECK['normal']:
                values.append(cleaners.basic_clean(item[normal]))

            for thorough in FIELDS_TO_CHECK['thorough_clean']:
                values.append(cleaners.thorough_clean(item[thorough]))

            writers.write_to_csv(csv_file, values)
            count += 1
        except KeyError:
            # so one of our keys is missing, disregard this inscription
            errors += 1

    print('successful: ' + str(count) + ', with unavailable data: ' + str(errors))
    csv_file.close()


def process_all_inscriptions():
    offset = 0
    total_raw = get_total_item_count()
    total = int(total_raw / 100) * 100

    print("Total number of items (rounded down): " + str(total))

    while offset < total:
        print('now at inscription ' + str(offset))
        loop_over_items(get_item_results(offset))
        offset += LIMIT


process_all_inscriptions()
