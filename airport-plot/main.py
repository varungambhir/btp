import csv

airport_map = {}

with open("../../other-data/airports.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        airport_map[row[0]] = row[1:]

print airport_map["ORD"]

