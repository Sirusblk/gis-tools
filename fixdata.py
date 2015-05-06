# FixData
#  - Desc: Fixes data from CoreLogic/DataQuick's Property Pro
#  - Author: David McLaren
#  - Usage: python3 fixdata.py data.csv
import csv
import json
import argparse

# Global variables set by config file
_CITY = ""
_PARCEL_HYPHENS = True

# Loads the config file and sets global variables
def load_config():
	with open("config.json") as config_file:
		config = json.load(config_file)

		_CITY = config["city"]
		_PARCEL_HYPHENS = config["parcel_hyphens"]


# Reads file in, returns list of each row from .csv file
def read_in(filename):
	output = []

	with open(filename, newline='') as csv_file:
		output = [line.split(',') for line in csv_file]

	return output


def find_index(property_info, text="Parcel Number"):
	for i, attr in enumerate(property_info[0]):
		if attr == "\"Parcel Number\"":
			index = i
			return index

	return -1


# Fixes structure of Parcels to 3-3-2, some are listed as 3-2-3
def fix_parcels(property_info):
	index = find_index(property_info)

	for line in property_info[1:]:
		attr = line[index]
		temp = attr.replace('-','')
		line[index] = temp[:4] + '-' + temp[4:7] + '-' + temp[7:]

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

	load_config()
	csv_data = read_in(args.filename)
	csv_data = fix_parcels(csv_data)

	write_out(csv_data, args.filename)


if __name__ == '__main__':
	main()
