

def get_date(a_date):
    return str(int(a_date))


def get_average_date(start, end):
    start = int(start)
    end = int(end)
    return str(int(start + (end - start) / 2))


# definitely have to remove commas that would mess up the CSV
def basic_clean(a_string):
    return a_string.replace(',', '')


# for things like inscriptions, which have a lot of special characters that might mess up analysis
def thorough_clean(inscr):
    return str.replace(inscr, '[', '').replace(']', '').replace('(', '').replace(')', '').replace('/', '') \
        .replace('{', '').replace('}', '').replace('\n', ' ').replace('"GR"', '').replace('"', '').replace('  ', ' ') \
        .replace(',', '').strip()
