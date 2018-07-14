import pandas as pd
import os
import csv

## CONSTANTS
# Directory where TMY data lives
DIRECTORY = '../../../tmy_data/'
# A file in the directory to access df columns
DUMMYFILE = '690150TYA.csv'

## CATCHER / PRE-SETUP DATA STRUCTURES
# Dictionary which will have keys:epw station name, values:dataframe
DF_DICT = {}
# List that will be used to house a list of dicts (k: station name as string, v: df)
PLOT_SERIES_LIST = []
# List that will be used to house the values (df) in PLOT_SERIES_LIST as lists
PLOT_SERIES_TOLIST = []
# List that will be used to house the final list data readable by the dash plot function
DASH_PLOT_DATA = []

# Function that takes a csv file and iterates 1 time to read the first row and appends the needed data to a list
def extract_city_state(csv_file):
	head = []
	with open(csv_file, "rt") as f:
		# Read in the first line, split it on end line character, then split the first element on the comma
		head = f.readline().split('\n')[0].split(',')
	output_string = ""
	# range(1, 3) used so that only the city and state are extracted
	for i in range(1, 3):
		output_string += head[i] + ", "
	output_string = output_string[:-2]
	return output_string

## DATA SETUP AND USER PROMPT/VALIDATION FUNCTIONS AND LOOPS
# Function to make a df
def make_df(file=str):
	return pd.read_csv(DIRECTORY + file, skiprows=1)

# Function that prints a message as a banner
def banner_print(message=str):
	print("")
	print("#"*30, " ", message, " ", "#"*30)
	print("")

# Show indexed list of parameters
def show_indexed_list(list_to_show, string_parameter):
	banner_print("Here are the %s:" %string_parameter)
	for index, i in enumerate(list_to_show):
		# The + 1 prints indices starting at 1 instead of 0
		print(index + 1, ": ", i)
	print(" ")

# User input function with validation
def user_input_and_val(input_string, check_object):
	while True:
		try:
			user_input = int(input("Enter %s: " %input_string))
			if user_input < 1 or user_input > len(check_object):
				print("Please enter a positive integer between 1 and %s" %len(check_object))
				continue
			break
		except ValueError:
			print("Invalid choice. Enter a positive integer only")
	return user_input


def main():
	# Create dummy df
	test_df = make_df(DUMMYFILE)

	# Set up x-axis date time list
	date_time = [str(i) + " " + str(j) for i, j in zip(test_df['Date (MM/DD/YYYY)'].tolist(), test_df['Time (HH:MM)'].tolist())]

	# Create a list of climate file parameters
	plot_parameters = list(test_df.columns)

	# Read all files as df and store each in a dict where:
		# key = station name (string)
		# value = df
	for roots, dirs, files in os.walk(DIRECTORY):
		for file in files:
			DF_DICT[extract_city_state(DIRECTORY + file)] = make_df(file)

	# Create a correspoding list of the df_dict keys
	DF_LIST = list(DF_DICT.keys())

	# Tell user how many stations are available
	banner_print("There are %s stations available to plot." %len(DF_LIST))
	# Get station quantity to plot from user
	station_qty = user_input_and_val("number of stations to display on plot:", DF_DICT)
	# Show indexed list of parameters to user
	show_indexed_list(plot_parameters, "available plot parameters")
	# Get plot parameter from user
	# The - 1 takes the screen index that starts at 1 and resets it to list indices that start at 0
	plot_parameter_index = user_input_and_val("the index of the parameter to plot:", plot_parameters) - 1
	chosen_parameter = plot_parameters[plot_parameter_index]

	## LOOP TO GET 
	# Loop [user station qty] times
	for i in range(1, station_qty + 1):
		# Show indexed list of stations
		show_indexed_list(DF_LIST, "stations")
		# Get user station selection | The - 1 takes the screen index that starts at 1 and resets it to list indices that start at 0
		user_selection_i = user_input_and_val("index of station %s to add to plot:" %i, DF_LIST) - 1
		# Add series from selected station df to plot series list
		chosen_df = DF_DICT[DF_LIST[user_selection_i]]
		PLOT_SERIES_LIST.append({DF_LIST[user_selection_i] : chosen_df[chosen_parameter]})
		# Remove the user selected item from the list
		DF_LIST.pop(user_selection_i)

	# Each element in the list of dicts
	for i in list(PLOT_SERIES_LIST):
		# Each listified element (listified because 'i' is a dict whose values df's)    
		for j in list(i.values()):
			# The listified values still have indices. Append them to the catcher list object using .tolist()
			PLOT_SERIES_TOLIST.append(j.tolist())

	for i, j in zip(PLOT_SERIES_TOLIST, PLOT_SERIES_LIST):
		# Plot data is element in list based list
		# Series name is the key in each dict element of the df based list
		DASH_PLOT_DATA.append({'x': date_time, 'y': i, 'type': 'line', 'name': list(j.keys())[0]})

	return DASH_PLOT_DATA, chosen_parameter