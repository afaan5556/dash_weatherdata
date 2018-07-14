# dash_weatherdata
This script uses the dash visualization library to plot a user selected weather data parameter

## Data Required
* epw or TMY files

## Variables
* `DIRECTORY`: Path to where the TMY or epw files are located
* `DUMMYFILE`: The name of any one of the target TMY or epw files
* Other variables used to set up needed data structures

## Use
Place the script in in a directory relative to the folder that contains the source TMY or epw data files per the `DIRECTORY` folder.

Run and follow the prompts to select:
1. The number of stations to compare
2. The weather parameter of interest
3. The stations of interest

The resulting visualization will run on localserver: `http://127.0.0.1:8050/`