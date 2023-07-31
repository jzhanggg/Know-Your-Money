import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

print()
print("1. Please put the CSV statement file in the folder where this budget_console_app is located. \n")

file_path = input("2. Enter name of the csv file, including the extension (if does not work, copy and paste file path here): ")
df = pd.read_csv(file_path, skiprows = [0, 1])

df[['Date Posted']] = df[['Date Posted']].applymap(str).applymap(lambda s: datetime.strptime(s, "%Y%m%d").date())

s_date_start = df.loc[0, 'Date Posted']
s_date_end = df['Date Posted'].iloc[-1]

print("*This statement contains transaction records from: " + str(s_date_start) + " to " + str(s_date_end) + "*\n")

p_date_start = input("3. Enter start date as yyyy-mm-dd to save in personal record for further analysis: \n")
p_date_start = datetime.strptime(p_date_start, "%Y-%m-%d").date()
p_date_end = input("Enter end date: ")
p_date_end = datetime.strptime(p_date_end, "%Y-%m-%d").date()

'''get a start date within the bounds from input and is also the nearest day to the start date in which transaction happens'''
if (df['Date Posted'] != p_date_start).all(): 
    next_date = None
    for date in df['Date Posted']: 
        if date > p_date_start: 
            next_date = date
            p_date_start = next_date
            break  

'''get an end date within the bounds from input and is also the nearest day to the end date in which day in which transaction happens'''
if (df['Date Posted'] != p_date_end).all(): 
    prev_date = None
    for date in df['Date Posted']: 
        if date < p_date_end: 
            prev_date = date
        else: 
            p_date_end = prev_date
            break




categories_dict = {
    'h' : "Hoyoverse Games",
    'g' : "Non-Hoyoverse Games",
    'c' : "car",
    'r' : "recreational events",
    's' : "study",
    'm' : "music",
    'd' : "drinks",
    'n' : "necessary food + drinks",
    'o' : "other",
    'i' : "income"
}

p_cols = [df.columns, 'label']
p_df = pd.DataFrame(columns = p_cols)

'''find index of the first row that contains p_date_start'''
row_start = df.index[df['Date Posted'] == p_date_start]

'''find index of the last row that contains p_date_end'''
row_end = df[df['Date Posted'] == p_date_end].last_valid_index()

'''Enter label information and store to dataframe, from row_start to row_end'''


'''Enter label information from second row of p_date_end to the last row that has p_date_end'''

'''Prompt to create new csv file to save record or append to previous csv file'''


'''Display spending by category from personal csv record'''







                                                         