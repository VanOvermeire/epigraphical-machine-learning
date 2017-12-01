import json
import requests
from helpers import cleaners, writers

# constants
START = 100  # start year
END = 200  # end year
LIMIT = 100  # items per request


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


def loop_over_items(items):
    count = 0
    errors = 0
    csv_file = open('files/epi_data.csv', 'a')

    for item in items:
        try:
            country = cleaners.remove_commas(item['country'])
            province = cleaners.remove_commas(item['province_label'])
            findspot = cleaners.remove_commas(item['findspot'])
            type_of_inscription = cleaners.remove_commas(item['type_of_inscription'])
            date = cleaners.get_date(item['not_before'])
            inscription = cleaners.clean_inscription(item['transcription'])

            writers.write_to_csv(csv_file, country, province, findspot, type_of_inscription, date, inscription)
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
