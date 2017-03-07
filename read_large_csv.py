import csv


def get_row(filename, delimiter=',', rows=-1, header=True):
    """
    Iterates over each row of a CSV file without loading the entire file to memory
    :param filename: CSV file name
    :param delimiter: the delimiter which separates each field
    :param rows: amount of rows to read, not considering header (if it exists). If <0, reads all file
    :param header: if True, skip the first row (ie, file has a header); if False, do not.
    :return: an untouched row of the CSV file
    :rtype: str
    """

    reader = csv.reader(open(filename, 'r'), delimiter=delimiter)

    # skip header
    if header:
        reader.next()

    count = 0
    for row in reader:

        if rows > 0 and count >= rows:
            return

        yield row
        count += 1

