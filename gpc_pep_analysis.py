#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 09:41:55 2023

@author: kelseyrichardson
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl 
mpl.rc('font',family='Arial')

# import raw data file
# *** NOTE: make sure the the raw data file is in the same folder as the code ***
input_name = input('Enter file name w/o extension: ')
file_name = input_name + '.arw'
raw = pd.read_csv(file_name,header=None,sep='\t')
# rename columns
raw.rename(columns={raw.columns[0]: 'Time',raw.columns[1]: 'Refractive Index'},inplace=True)
# drop time < 7 and > 12
raw = raw.drop(raw[raw['Time']<7].index)
raw = raw.drop(raw[raw['Time']>12].index)

# plot refractive index vs time
plt.scatter(raw['Time'],raw['Refractive Index'],c='#264653')
plt.tick_params(axis="y",direction="in")
plt.tick_params(axis="x",direction="in")
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.xlabel("Time",fontsize=16)
plt.ylabel("Refractive Index",fontsize=16)
plt.show()

# get user input for new time values
happy = input("Are you happy with the time interval [y/n]? ")
while happy == 'n':
    new_time_int = input("Enter new minimum and maximum time values, separated by a comma: ")
    time_min = float(new_time_int.split(',')[0])
    time_max = float(new_time_int.split(',')[1])
    # drop new times
    raw = raw.drop(raw[raw['Time']<time_min].index)
    raw = raw.drop(raw[raw['Time']>time_max].index)
    title_string = 'Time'
    # plot refractive index vs time
    plt.scatter(raw['Time'],raw['Refractive Index'],c='#264653')
    plt.tick_params(axis="y",direction="in")
    plt.tick_params(axis="x",direction="in")
    plt.xticks(size = 12)
    plt.yticks(size = 12)
    plt.xlabel("Time",fontsize=16)
    plt.ylabel("Refractive Index",fontsize=16)
    plt.title('Replotted')
    plt.show()
    # are you happy with the time?
    happy = input("Are you happy with the time interval [y/n]? ")
    
# subtract baseline
raw['Normalized Refractive Index'] = raw['Refractive Index'] - min(raw['Refractive Index'])

# rescale time axis
raw['log(M)'] = 13.9 - 2.02 * raw['Time'] + 0.164 * raw['Time']**2 - 0.00638 * raw['Time']**3

# plot subtracted baseline
plt.scatter(raw['log(M)'],raw['Normalized Refractive Index'],c='#264653')
plt.tick_params(axis="y",direction="in")
plt.tick_params(axis="x",direction="in")
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.xlabel("log(M)",fontsize=16)
plt.ylabel("Normalized Refractive Index",fontsize=16)
plt.show()

# normalize y axis
raw['Mass %'] = raw['Normalized Refractive Index']/(sum(raw['Normalized Refractive Index']))

# add column for M PS
raw['M (PS)'] = 10**raw['log(M)']

# add column for M PEP
raw['M (PEP)'] = (13.1/57.9*raw['M (PS)']**0.707)**(1/0.695)

# add column for number of carbons
raw['Num of C'] = raw['M (PEP)'] / 14

# add column for mass chains
rec_mass = float(input('Enter the recovered mass: '))
raw['Mass Chains'] = raw['Mass %'] * rec_mass

# add column for mol chains
raw['Mol Chains'] = raw['Mass Chains'] / raw['M (PEP)']

# add column for mol C-C bonds
raw['Mol C-C Bonds'] = (raw['Num of C'] - 1) * raw['Mol Chains']

# export data frame as xlsx
output_name = input_name + '_analyzed.xlsx'
raw.to_excel(output_name,index=False)

