import csv

def getstuff(filename, delimiter=',', rows=-1):
    with open(filename, "r") as csvfile:
        datareader = csv.reader(csvfile, delimiter=delimiter)
        datareader.next() # skip header
        count = 0
        for row in datareader:
            yield row
            count += 1
            if rows > 0 and count >= rows:
                return
