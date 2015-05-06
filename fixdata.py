# FixData
#  - Desc: Fixes data from CoreLogic/DataQuick's Property Pro
#  - Author: David McLaren
#  - Usage: python3 fixdata.py data.csv
from tempfile import NamedTemporaryFile
import shutil
import csv
import json
import argparse

# Global variables set by config file
_CITY = ""
_PARCEL_HYPHENS = True

def load_config():
	with open("config.json") as config_file:
		config = json.load(config_file)

		CITY = config["city"]
		PARCEL_HYPHENS = config["parcel_hypens"]


def read_in(filename):
	#tempfile = NamedTemporaryFile(delete=False)
	output = []

	with open(filename, newline='') as csv_file:
		output = [line.split() for line in csv_file]

	return output


def find_index(property_info, text="Parcel Number"):
	index = -1

	for i, attr in enumerate(property_info[0]):
		if attr is "Parcel Number":
			index = i
			return index

	return index


def fix_parcels(property_info):
	index = find_index(property_info)

	for line in property_info[1:]:
		for attr in line:
			temp = atr.strip('-')
			
			# DEBUG
			print(temp)

			line[index] = temp


def main():
	pass


if __name__ == '__main__':
	main()
