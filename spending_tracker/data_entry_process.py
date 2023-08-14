import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import timedelta
from shared_info import *

print()
print("1. Please put the CSV statement file in the folder where this budget_console_app is located. \n")

p_filename = 'personal_record.csv'
statement_filename = input("2. Enter name of the csv file, including the extension: \n")

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, statement_filename)
p_file_path = os.path.join(current_directory, p_filename)


df = pd.read_csv(file_path, skiprows = [0, 1])

df[['Date Posted']] = df[['Date Posted']].applymap(str).applymap(lambda s: datetime.strptime(s, "%Y%m%d").date())
df['label'] = np.nan

s_date_start = df.loc[0, 'Date Posted']
s_date_end = df['Date Posted'].iloc[-1]

print("*THIS STATEMENT CONTAINS TRANSACTION RECORDS FROM: " + str(s_date_start) + " TO " + str(s_date_end) + "*\n")

#if the personal record csv exists:
if os.path.isfile(p_file_path): 
    p_df = pd.read_csv(p_file_path)
    last_date = str(p_df['Date Posted'].iloc[-1])
    last_date = datetime.strptime(last_date, "%Y-%m-%d").date()

    print("The last transaction found in personal record was on: " + str(last_date) + ". Do you want to use the day after this as the starting date? \n")
    ans = input("Enter 'y' for yes, otherwise hit enter: ")
    
    if ans == 'y': 
        p_date_start = last_date + timedelta(days = 1)
    else: 
        p_date_start = input("3. Enter start date as yyyy-mm-dd to save in personal record for further analysis: \n")
        p_date_start = datetime.strptime(p_date_start, "%Y-%m-%d").date()

else: 
    p_date_start = input("3. Enter start date as yyyy-mm-dd to save in personal record for further analysis: \n")
    p_date_start = datetime.strptime(p_date_start, "%Y-%m-%d").date()

print("Do you want to record all transactions up to the most recent date in this statement?  \n")
ans = input("Enter 'y' for yes, otherwise hit enter: ")

if ans == 'y': 
    p_date_end = s_date_end

else: 
    p_date_end = input("Enter end date: \n")
    p_date_end = datetime.strptime(p_date_end, "%Y-%m-%d").date()

p_date_start = get_start_date(df['Date Posted'], p_date_start)
p_date_end = get_end_date(df["Date Posted"], p_date_end)

#find index of the first row that contains p_date_start
row_start = df[df['Date Posted'] == p_date_start].first_valid_index()

#find index of the last row that contains p_date_end
row_end = df[df['Date Posted'] == p_date_end].last_valid_index()

#Enter label information and store to df, from row_start to row_end
for i in range(row_start, row_end + 1): 
    print()
    print("Labels: " + str(categories_dict) + "\n")
    print(df.iloc[i])
    label = input("Enter label for current transaction: ")
    df.at[i, 'label'] = label

#Create new_df to be saved in other csv file with the rows of df between index row_start and row_end
new_df = df.loc[row_start:row_end].copy()

#In case if I get a new card some time later
new_df = df.sort_values(by = 'Date Posted')

#Prompt to create new csv file to save record or append to previous csv file
if os.path.isfile(p_file_path): 
    new_df.to_csv(p_file_path, mode = 'a', header = False, index = False)
    print()
    print ("PERSONAL RECORD EXISTS, ABOVE ENTRIES APPENDED TO THE FILE. \n ")
else: 
    new_df.to_csv(p_file_path, index = False)
    print()
    print("PERSONAL RECORD INITIALIZED, ABOVE ENTRIES ADDED TO PERSONAL RECORD. \n")





                                                         