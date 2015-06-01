# FixData
#  - Desc: Fixes data from CoreLogic/DataQuick's Property Pro
#  - Author: David McLaren
#  - Usage: python3 fixdata.py data.csv
import csv
import json
import argparse
import configparser

# Read in Config settings
CONFIG = configparser.ConfigParser()
CONFIG.read('config.cfg')

# Reads file in, returns list of each row from .csv file
def read_in(filename):
    output = []

    with open(filename, newline='') as csv_file:
        output = [line.split(',') for line in csv_file]

    return output


def find_index(property_info, text):
    for i, attr in enumerate(property_info[0]):
        if attr == "\""+text+"\"":
            index = i
            return index

    return -1


# Fixes structure of Parcels to 3-3-2, some are listed as 3-2-3
def fix_parcels(property_info):
    index = find_index(property_info, "Parcel Number")

    # Skip initial header row
    for line in property_info[1:]:
        attr = line[index]
        temp = attr.replace('-','')
        line[index] = temp[:4] + '-' + temp[4:7] + '-' + temp[7:]

    return property_info


# Adds column with summerized address field
def add_site_address_col(property_info, directionals=True, unit_numbers=True):
    num_index = find_index(property_info, "Site Address Street Number")
    name_index = find_index(property_info, "Site Address Street Name")
    dir_index = find_index(property_info, "Site Address Pre Directional")
    unit_index = find_index(property_info, "Site Address Unit Number")
    record_index = max(num_index, name_index, dir_index)

    property_info[0].insert(record_index, "\"SiteAddress\"")

    for line in property_info[1:]:
        record = ""

        # Add Street Number
        if num_index != -1:
            record += line[num_index].replace('\"','')
        else:
            print("[ERROR] Could not find column with Street Address Street Numbers")

        # Add Predirectional
        if (directionals == True):
            if (dir_index != -1):
                if line[dir_index].replace('\"','').rstrip() != "":
                    record = record + ' ' + line[dir_index].replace('\"','').rstrip()
            else:
                print("[ERROR] Could not find column of street directions")

        # Add Street Name
        if name_index != -1:
            if (line[name_index].replace('\"','').rstrip() != "") and (line[name_index] != "0"):
                record = record + ' ' + line[name_index].replace('\"','').rstrip()
        else:
            print("[ERROR] Could not find column with Street Address Names")

        # Add Unit Number
        if (unit_numbers == True):
            if (unit_index != -1):
                if line[unit_index].replace('\"','').rstrip() != "":
                    record = record + ' ' + line[unit_index].replace('\"','').rstrip()
            else:
                print("[ERROR] Could not find column with Unit Numbers")

        # Append concatenated address record
        record = '\"' + record + '\"'
        line.insert(record_index, record)

    return property_info


# Writes data out to new .csv file
def write_out(property_info, filename):
    filename = filename[:-4] + "_mod.csv"

    with open(filename, 'w') as csv_file:
        for line in property_info:
            csv_file.write(','.join(line))


def main():
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Filename of .csv file to read from.")

    args = parser.parse_args()

    csv_data = read_in(args.filename)
    csv_data = fix_parcels(csv_data)
    csv_data = add_site_address_col(csv_data)

    write_out(csv_data, args.filename)


if __name__ == '__main__':
    main()
