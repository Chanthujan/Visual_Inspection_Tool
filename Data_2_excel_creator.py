import csv

#optional code
"""This is the code used to merge the Geonet earthquake information with the earthquake S-wave and P-wave picks excel sheet from the catalogue (order 2)"""

def find_matching_row(csv_file1, csv_file2, column_index1, column_index2):
    matching_rows = []
    with open(csv_file1, 'r') as file1:
        reader1 = csv.reader(file1)
        for row1 in reader1:
            #print(row1[column_index1])
            value1 = row1[column_index1].split('/')[1]
            with open(csv_file2, 'r') as file2:
                reader2 = csv.reader(file2)
                for row2 in reader2:
                    if row2[column_index2] == value1:
                        matching_rows.append((row1, row2))
    return matching_rows


def update_csv_with_third_column(csv_file1, csv_file2, column_index1, column_index2, column_index3):
    matching_rows = find_matching_row(csv_file1, csv_file2, column_index1, column_index2)

    with open(csv_file1, 'r') as file1:
        rows = list(csv.reader(file1))
        for row1, row2 in matching_rows:
            row_number = rows.index(row1)
            row1[5] = row2[column_index3]  #row1[column_index1] = row2[column_index3]
            rows[row_number] = row1

    with open(csv_file1, 'w', newline='') as file1:
        writer = csv.writer(file1)
        writer.writerows(rows)

# Example usage

column_index1 = 0  # Column index in the first CSV file to check for a match
column_index2 = 0  # Column index in the second CSV file to check for a match
column_index3 = 6  # Column index in the second CSV file to get the value from

update_csv_with_third_column("tables/eventTable/DATA.csv","catalogue_2013_2022/QuakeSearch.csv" , column_index1, column_index2, column_index3)

#for every line in test1.csv file get the value in the first column and assign it to a string
with open('tables/eventTable/DATA.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    lines = list(csv.reader(csv_file))

    for line in csv_reader:
        #skip the first line
        if str(line[0]) == 'EarthquakeID/0':#no /0 before
            print(line[0])
            continue
        #print(str(line[0]))
        earthquake_ID = line[0].split('/')[1]
        #check the earthquake ID is in first column of catalogue_2013_2022/test1EQ.csv file and print the row number in the file's first column
        with open('catalogue_2013_2022/QuakeSearch.csv', 'r') as csv_file_2:
            reader = csv.reader(csv_file_2)
            for row in reader:
                if len(row) >= 2 and row[0] == earthquake_ID:
                    #print("Earthquake ID: " + earthquake_ID + " is in row " + str(reader.line_num) + "and the magnitude of the earthquake is:" + row[6])
                    line.extend(row[6])
                lines.append(row[6]) 

with open('tables/eventTable/DATA.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(lines)
 



