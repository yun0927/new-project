import csv

def convert_time_to_sec(t):
    minutes, seconds = t.split(":")
    return round(int(minutes)*60 + float(seconds), 2)

with open("add_data.csv", newline='', encoding='utf-8') as infile, open("add_data_fixed.csv", "w", newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['time_sec']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        row['time_sec'] = convert_time_to_sec(row['time'])
        writer.writerow(row)
