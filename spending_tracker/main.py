import subprocess
import os
import csv
from datetime import datetime
from disp import *
import warnings

from shared_info import *

#function to let user choose what function to perform
def selector(): 
    print()
    selector = input("SELECT WHAT TO DO: \n \
                     Enter '1' for transaction entry through csv statement file \n \
                     Enter '2' to see spending overview: by category and income vs. expense\n \
                     Enter '3' to extract record for selected categories and date\n \
                     Enter '4' to update monthly expense data \n \
                     Enter '5' to compare total expense across each monthly period \n \
                     Enter '6' to see line graph comparing Covered Balance, Personal Balance, and Savings Balance over time \n \
                     Enter 'q' to quit: \n")
    return selector

#body-------------------------------------------------------------------------------------------------

if os.path.isfile(p_file_path): 
    from calculation import *

    user_sel = selector()

    while user_sel != 'q': 

        if user_sel == '1': 
            subprocess.run(["python", dep_path])

        elif user_sel == '2': 
            spending_overview()

        elif user_sel == '3': 
            print(categories_dict)
            print()
            
            p_or_c = input("If you want to extract covered spending data, enter 'c'. \n If you want to extract personal spending data, enter 'p'.\n If you want to select specific categories, press enter. \n")
            
            if p_or_c == 'p': 
                q_categories = personal_balance
            elif p_or_c == 'c': 
                q_categories = covered_balance
            else: 
                q_categories = input("Enter the character symbols for the categories you would like to extract. \n \
                For example, to select the car, study, and music categories: c,i,m \n \
                Your Entry: ")
                q_categories = q_categories.split(',')
                  
            q_date = input("Do you want to extract all record on the selected categories? Enter 'y' for yes, else enter: \n")

            extracted_df = pd.DataFrame()
            if q_date == 'y': 
                extracted_df = extract_all(q_categories)

            else: 
                print("Enter range of date between: " + str(p_df['Date Posted'][0]) + " to " + str(p_df['Date Posted'].iloc[-1]) + ". \n")
                q_range_start = input("Enter start date in form YYYY-MM-DD: \n")
                q_range_end = input("Enter end date in form YYYY-MM-DD: \n")
                extracted_df = extract_within_range(q_categories, q_range_start, q_range_end)

            extracted_df['label'] = extracted_df['label'].replace(categories_dict)
            list_categories = extracted_df['label'].unique().tolist()

            description = "THE SUMMED BALANCE OF THE CATEGORIES: " + str(list_categories) +  " IS:  $" + str(extracted_df[' Transaction Amount'].sum()) + ". \n"
            show_df_with_description(extracted_df, "Extracted Spending Data", description)

        elif user_sel == '4': 

            if os.path.isfile(m_file_path): 
                print()
                m_df = pd.read_csv(m_file_path)
                last_month = str(m_df['Month'].iloc[-1])
                day = 1
                last_month_date = datetime.strptime(f"{last_month}-{day}", "%Y-%m-%d").date()
                
                most_recent_date = str(p_df['Date Posted'].iloc[-1])
                most_recent_date = datetime.strptime(most_recent_date, "%Y-%m-%d").date()
                
                start_date = str(get_start_date(p_df['Date Posted'], last_month_date))
                end_date = str(get_end_date(p_df['Date Posted'], most_recent_date))
                
                added_month_df = calc_month_data(start_date, end_date)
                
                m_df_copy = m_df.drop(m_df.index[-1], inplace=True)

                m_df = m_df._append(added_month_df, ignore_index=True)
                
                                
            else: 
                print("monthly file initiated. \n")
                m_df = calc_month_data()
            
            m_df.to_csv(m_file_path, index = False)
                
            
        
        elif user_sel == '5': 

            if os.path.isfile(m_file_path): 
                display_df = pd.read_csv(m_file_path)
                show_df_with_description(display_df, "Monthly Spending Data")


            else: 
                print("Monthly record file does not exist, cannot display. \n")
                
        elif user_sel == '6': 
            if os.path.isfile(m_file_path): 
                month_df = pd.read_csv(m_file_path)
                show_c_p_s_line_graph(month_df, "Month", "Covered balance", "Personal balance", "Savings")

            else: 
                print("Monthly record file does not exist, cannot display. \n")
        
        
        else: 
            break      

        user_sel = selector()
else: 
    print()
    ans = input("Personal Record does not exist. If you want to initiate one, press 'y'. Otherwise press anything else to quit. \n")
    
    if ans == 'y': 
        subprocess.run(["python", dep_path])



