

def get_date(a_date):
    return str(int(a_date))


def get_average_date(start, end):
    start = int(start)
    end = int(end)
    return str(int(start + (end - start) / 2))


def remove_commas(a_string):
    return a_string.replace(',', '')


def clean_inscription(inscr):
    return str.replace(inscr, '[', '').replace(']', '').replace('(', '').replace(')', '').replace('/', '') \
        .replace('{', '').replace('}', '').replace('\n', ' ').replace('"GR"', '').replace('"', '').replace('  ', ' ') \
        .replace(',', '').strip()
