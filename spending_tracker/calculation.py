import pandas as pd
import numpy as np
import os
from datetime import datetime
from shared_info import *

current_directory = os.path.dirname(os.path.abspath(__file__))
p_file_path = os.path.join(current_directory, "personal_record.csv")
p_df = pd.read_csv(p_file_path)

# 1. expense across all categories for all transactions in record
def spending_overview(): 
    grouped_df = p_df.groupby('label')[' Transaction Amount'].sum().reset_index()
    grouped_df = grouped_df.fillna(0)

    covered_sum = 0
    for label in grouped_df['label']: 
        if label in covered_balance: 
            condition = grouped_df['label'] == label
            selected_row = grouped_df[condition]
            covered_sum = covered_sum + selected_row[' Transaction Amount'].values[0]

    personal_sum = 0
    for label in grouped_df['label']:
        if label in personal_balance: 
            condition = grouped_df['label'] == label
            selected_row = grouped_df[condition]
            personal_sum = personal_sum + selected_row[' Transaction Amount'].values[0]


    grouped_df['label'] = grouped_df['label'].replace(categories_dict)

    print("SPENDING OVERVIEW: ")
    print(grouped_df)
    print()
    print("COVERED BALANCE: $" + str(round(covered_sum, 2)))
    print("PERSONAL BALANCE: $" + str(round(personal_sum, 2)))

    if  (grouped_df['label'] == label).any(): 
        print("There is undetermined spending/income, resolve ASAP. ")
    





