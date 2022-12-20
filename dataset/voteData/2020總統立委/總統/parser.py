import csv

# map {party code: party name}
party = {}
with open('elpaty.csv', newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        party[row[0]] = row[1]
print(party)

# elbase.csv mix all cities and townships/urban areas
# we filter out all cities date here
filter_city = []
with open('elbase.csv', newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        if row[3] == '000' and row[0] != '00' and not ((row[0] == '09' or row[0] == '10') and row[1] == '000'):
            filter_city.append(row)
print(filter_city)

# get the city name of one row in elctks.csv


def match_city(row):
    if len(row) >= 5:
        return next((x[5] for x in filter_city if row[:5] == x[:5]), None)


# map {canditate code, {'name': name of canditate, 'party': party name of canditate}}
canditates = {}
parsed_canditates = []
with open('elcand.csv', newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        if row[-1] != 'Y':
            canditates[row[5]] = {'name': row[6], 'party': party[row[7]]}
            parsed_canditates.append(
                [row[5], row[6], party[row[7]], 'male' if row[8] == '1' else 'female', int(row[10]), row[-5], row[-4], row[-3] == 'Y', row[-2] == '*'])
print(canditates)

# parsed_canditates to csv file
with open('../../cleaned/president/2020/candidate.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['no', 'candidate', 'candidate_party',
                    'gender', 'age', 'homeplace', 'education_level', 'incumbent', 'elected'])
    for row in parsed_canditates:
        writer.writerow(row)

# elctks.csv mix all ticket data across all levels from cities, townships, urban areas
# we filter out all data on the level of nation or city
tks_by_nation = []
tks_by_city = []
with open('elctks.csv', newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        if row[:6] == ["00", "000", "00", "000", "0000", "0000"]:
            tks_by_nation.append([canditates[row[6]]['name'],
                                  canditates[row[6]]['party'], int(row[7]), float(row[8]), row[9] == '*'])
            continue
        city = match_city(row)
        if city:
            tks_by_city.append([city, canditates[row[6]]['name'],
                                canditates[row[6]]['party'], int(row[7]), float(row[8]), row[9] == '*'])
print(tks_by_city)
print(tks_by_nation)

# write tks_by_nation and tks_by_city to csv file
with open('../../cleaned/president/2020/by_nation.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['candidate', 'candidate_party',
                    'ticket', 'ticket_percentage', 'elected'])
    for row in tks_by_nation:
        writer.writerow(row)

with open('../../cleaned/president/2020/by_city.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['city', 'candidate', 'candidate_party',
                    'ticket', 'ticket_percentage', 'elected'])
    for row in tks_by_city:
        writer.writerow(row)
