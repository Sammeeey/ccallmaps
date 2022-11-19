# readRegions.py - reads 'plz' column from 'zuordnung_plz_ort.csv' - helper script to initially get plz's (was only relevant once - relevant list of PLZ's now in plzList.py - however may be used/extended later)
import csv

plzList = []

# --- read plz's from csv file  https://docs.python.org/3/library/csv.html#csv.DictReader
with open('zuordnung_plz_ort.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # append if it's not a duplicate
        if row['plz'] not in plzList:
            plzList.append(row['plz'])
        # result: list in same order as in original csv

print(plzList)
print(len(plzList)) # 8170


# # removing duplicate elements from the list: https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
# l = [1, 2, 4, 2, 1, 4, 5]
# print("Original List: ", l)
# res = [*set(plzList)]
# print("List after removing duplicate elements: ", res) # result: list in same order as in original csv
# print(len(res)) # 8170