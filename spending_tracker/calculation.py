import pandas as pd
import numpy as np
import os
from datetime import datetime
from shared_info import *
import tkinter as tk
from tkinter import scrolledtext

#if p_df does not exist run data entry process

current_directory = os.path.dirname(os.path.abspath(__file__))
p_file_path = os.path.join(current_directory, "personal_record.csv")
p_df = pd.read_csv(p_file_path)
p_df[['Date Posted']] = p_df[['Date Posted']].applymap(str).applymap(lambda s: datetime.strptime(s, "%Y-%m-%d").date())

def get_covered_balance(g_df): 
    covered_sum = 0

    for label in g_df['label']: 
        if label in covered_balance: 
            condition = g_df['label'] == label
            selected_row = g_df[condition]
            covered_sum = covered_sum + selected_row[' Transaction Amount'].values[0]
    
    return covered_sum

def get_personal_balance(g_df): 
    personal_sum = 0

    for label in g_df['label']:
        if label in personal_balance: 
            condition = g_df['label'] == label
            selected_row = g_df[condition]
            personal_sum = personal_sum + selected_row[' Transaction Amount'].values[0]

    return personal_sum

def get_savings(g_df): 
    savings = 0
    
    for label in g_df['label']:
        if label in ['sv', 'osv']: 
            condition = g_df['label'] == label
            selected_row = g_df[condition]
            savings = savings - selected_row[' Transaction Amount'].values[0]

    return savings

    

# 2. spending overview
def spending_overview(): 
    grouped_df = p_df.groupby('label')[' Transaction Amount'].sum().reset_index()

    covered_sum = get_covered_balance(grouped_df)
    personal_sum = get_personal_balance(grouped_df)

    grouped_df['label'] = grouped_df['label'].replace(categories_dict)

    print("SPENDING OVERVIEW from: " + str(p_df['Date Posted'][0]) + " to " + str(p_df['Date Posted'].iloc[-1]) + ". \n")
    print(grouped_df)
    print()
    print("COVERED BALANCE: $" + str(round(covered_sum, 2)))
    print("PERSONAL BALANCE: $" + str(round(personal_sum, 2)))

    if  (grouped_df['label'] == 'undetermined, ATTENTION NEEDED').any(): 
        print("There is undetermined spending/income, resolve ASAP. ")

# 3. Extract all record for selected categories
def extract_all(selected_labels_list): 
    condition = p_df['label'].isin(selected_labels_list)
    filtered_rows = p_df[condition]
    extracted_df = pd.DataFrame(filtered_rows)
    return extracted_df

# 3. Extract record for selected categories between a specific date range
def extract_within_range(selected_labels_list, str_given_start, str_given_end): 
    str_given_start = datetime.strptime(str_given_start, "%Y-%m-%d").date()
    str_given_end = datetime.strptime(str_given_end, "%Y-%m-%d").date()

    p_date_start = get_start_date(p_df['Date Posted'], str_given_start)
    p_date_end = get_end_date(p_df["Date Posted"], str_given_end)
    row_start = p_df[p_df['Date Posted'] == p_date_start].first_valid_index()
    row_end = p_df[p_df['Date Posted'] == p_date_end].last_valid_index()

    condition = p_df['label'].isin(selected_labels_list) & (p_df.index >= row_start) & (p_df.index <= row_end)
    filtered_rows = p_df[condition]
    extracted_df = pd.DataFrame(filtered_rows)
    return extracted_df

# 4. Save newest monthly data to csv
def calc_month_data(str_date_start = None, str_date_end = None): 
    
    if str_date_start is None and str_date_end is None:  
        filtered_df = p_df
    else: 
        date_start = datetime.strptime(str_date_start, "%Y-%m-%d").date()
        date_end = datetime.strptime(str_date_end, "%Y-%m-%d").date()
        filtered_df = p_df[(p_df['Date Posted'] >= date_start) & (p_df['Date Posted'] <= date_end)]
    
    pd.to_datetime(filtered_df['Date Posted'])
    unique_months = pd.to_datetime(filtered_df['Date Posted']).dt.to_period('M').unique()

    columns = list(categories_dict.values())
    
    columns.append("Covered balance")
    columns.append("Personal balance")
    columns.append("Savings")
    columns.insert(0, "Month")
    month_df = pd.DataFrame(columns = columns)

    month_df_i_count = 0

    for month in unique_months: 
        month_df = month_df._append(pd.Series([0] * len(columns), index=columns), ignore_index=True)
        condition = pd.to_datetime(filtered_df['Date Posted']).dt.to_period('M') == month
        sec_df = filtered_df[condition]
        sec_grouped_df = sec_df.groupby('label')[' Transaction Amount'].sum().reset_index()

        condition_accum = pd.to_datetime(p_df['Date Posted']).dt.to_period('M') <= month
        accum_df = p_df[condition_accum]
        accum_g_df = accum_df.groupby('label')[' Transaction Amount'].sum().reset_index()

        covered_sum = get_covered_balance(accum_g_df)
        personal_sum = get_personal_balance(accum_g_df)
        savings = get_savings(accum_g_df)
        month_df.loc[month_df_i_count, 'Covered balance'] = covered_sum
        month_df.loc[month_df_i_count, 'Personal balance'] = personal_sum
        month_df.loc[month_df_i_count, 'Savings'] = savings

        month_df.loc[month_df_i_count, 'Month'] = str(month)

        sec_grouped_df['label'] = sec_grouped_df['label'].replace(categories_dict)

        sec_grouped_df = sec_grouped_df.T

        new_cols = sec_grouped_df.iloc[0]
        sec_grouped_df = sec_grouped_df.iloc[1:].reset_index(drop = True)
        sec_grouped_df.columns = new_cols
        
        for category in sec_grouped_df.columns: 
            if category in month_df.columns: 
                month_df.loc[month_df_i_count, category] = sec_grouped_df.loc[0, category]

        month_df_i_count = month_df_i_count + 1
    
    month_df.fillna(0)
    
    return month_df

            



























