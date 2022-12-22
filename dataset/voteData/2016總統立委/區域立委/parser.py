import csv

# map {party code: party name}
party = {}
with open('elpaty.csv', newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        party[row[0]] = row[1]
print(party)

# elbase.csv mix all cities and townships/urban areas
# we filter out all electoral district
filter_district = []
with open('elbase_T1.csv', newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        if '選區' in row[5]:
            filter_district.append(row)
print(filter_district)

# get the electoral district name of one row in elctks.csv
def match_district(row):
    if len(row) >= 5:
        return next((x[5] for x in filter_district if row[:5] == x[:5]), None)


# map {electoral district name, {canditate no: {'name': name of canditate, 'party': party name of canditate}...]}}
canditates = {}
parsed_canditates = []
with open('elcand_T1.csv', newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        district = match_district(row)
        city = district[:district.index('第')]
        if district not in canditates:
            canditates[district] = {}
        canditates[district][row[5]] = {'name': row[6], 'party': party[row[7]]}
        parsed_canditates.append(
            [city, district, row[5], row[6], party[row[7]], 'male' if row[8] == '1' else 'female', int(row[10]), row[-5], row[-4], row[-3] == 'Y', row[-2] == '*'])
print(canditates)

# parsed_canditates to csv file
with open('../../cleaned/legislator/2016/candidate.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['city', 'electoral_district', 'no', 'candidate', 'candidate_party',
                    'gender', 'age', 'homeplace', 'education_level', 'incumbent', 'elected'])
    for row in parsed_canditates:
        writer.writerow(row)

tks_by_district = []
with open('elctks_T1.csv', newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        district = match_district(row)
        if row[5] == '0' and district:
            city = district[:district.index('第')]
            tks_by_district.append([city, district, canditates[district][row[6]]['name'],
                                    canditates[district][row[6]]['party'], int(row[7]), float(row[8]), row[9] == '*'])
print(tks_by_district)

with open('../../cleaned/legislator/2016/by_district.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['city', 'electoral_district', 'candidate', 'candidate_party',
                    'ticket', 'ticket_percentage', 'elected'])
    for row in tks_by_district:
        writer.writerow(row)
