#!/usr/bin/env python
import os
from pandas import DataFrame, read_csv
import pandas as pd 

path = 'C:\\Users\\willi\\Repositories\\BaeDataset\\Cases45-LeticiaAbarca\\'
# path = 'C:\\Users\\willi\\Repositories\\BaeDataset\\test\\'

variables_hash = {}
variables_list = []
files = []

# Accessing variable (question shortnning)
def saveVariableName(dictionary, variable):
	v = str(variable)
	if v in variables_hash:
		pass
	else:
		variables_hash[v] = {}
	return v

# Accessing total count
def saveTotalCount(dictionary, variable, val):
	if 'total' in variables_hash[variable]:
		if str(val) != 'nan':
			variables_hash[variable]['total'] += round(float(val), 2)
	else:
		variables_hash[variable]['total'] = 0.0
	return

# Accessing country's name
def saveCountry(dictionary, variable, val):
	v = str(val)
	if v in variables_hash[variable]:
		pass
	else:
		variables_hash[variable][v] = 0.0
	return v

# Acessing numerical value
def saveNumericalData(dictionary, variable, country, value):
	if str(value) != 'nan':
		dictionary[variable][country] += round(float(val), 2)
	return

# Build list of countries
def getCountries(variables_hash):
	countries_list = {}
	for variable, values in variables_hash.items():
		for country in values:
			if country != 'total':
				if country in countries_list:
					countries_list[country] += 1;
				else:
					countries_list[country] = 1;
	return countries_list

# Final matrix initializer
def initializeFinalMatrix(countries_list, variables_list):
	final_dict = {}
	for country, count in countries_list.items():
		if country not in final_dict:
			final_dict[country] = {}
			for varia in variables_list:
				if varia not in final_dict[country]:
					final_dict[country][varia] = 0.0
	return final_dict

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.xls' in file:
            files.append(os.path.join(r, file))

for f in files:
	df = pd.read_excel(f)
	columns = list(df)
	column_index = 0
	variable = 'none'
	for i in columns:
		row_index = 0
		country = 'none'
		for val in df[i]:
			if column_index == 0 and row_index == 0:
				# saving variable name
				variable = saveVariableName(variables_hash, val)
				variables_list.append(str(val))
			elif column_index == 1 and row_index >= 0:
				# saving total
				saveTotalCount(variables_hash, variable, val)
			elif column_index > 1:
				if row_index == 0:
					# saving country name
					country = saveCountry(variables_hash, variable, val)
				elif row_index > 0:
					# saving numerical data
					saveNumericalData(variables_hash, variable, country, val)
			row_index += 1
		column_index += 1

print("\n\n\n\n" + str(len(files)) + " files read.\n\n")

countries_list = getCountries(variables_hash)

final_dict = initializeFinalMatrix(countries_list, variables_list)

for country, variableList in final_dict.items():
	for variable, countryList in variables_hash.items():
		if country in variables_hash[variable]:
			final_dict[country][variable] = variables_hash[variable][country]

# f = open('unified_dataset.csv','w')

# header = 'Country'
# for var in variables_list:
# 	header += ', ' + var
# header += '\n'

# f.write(header)

# for country, variables in final_dict.items():
# 	data_line = country
# 	for var, val in variables.items():
# 		data_line += ', ' + str(val)
# 	data_line += '\n'
# 	f.write(data_line)

# f.close()

f = open('country_count.csv','w')

header = 'Country, Count\n'
f.write(header)

for country, count in countries_list.items():
	f.write(country + ', ' + str(count) + '\n')

f.close()
		