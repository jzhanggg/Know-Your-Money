import subprocess
import os
import csv
from datetime import datetime
from shared_info import *

dep = "data_entry_process.py"
dep_path = os.path.join(current_directory, dep)

# ERROR HANDLE: throw error for date entered out of bound, ask user to input correct date in range and display date range in record
# problems solve: quit anywhere during the process
# problem solve: after data entry, must restart entire program to ensure that data is updated
# problem solve: table too wide, does not show in cosole, need pop up


def selector(): 
    print()
    selector = input("SELECT WHAT TO DO: \n \
                     Enter '1' for transaction entry through csv statement file \n \
                     Enter '2' to see spending overview: by category and income vs. expense\n \
                     Enter '3' to extract record for selected categories and date\n \
                     Enter '4' to update monthly expense data \n \
                     Enter '5' to compare total expense across each monthly period \n \
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
            q_categories = input("Enter the character symbols for the categories you would like to extract. \n \
            For example, to select the car, study, and music categories: c,i,m \n \
            Your Entry: ")
            q_categories = q_categories.split(',')
            
            q_date = input("Do you want to extract all record on the selected categories? Enter 'y' for yes, else enter: \n")

            extracted_df = pd.DataFrame()
            if q_date == 'y': 
                extracted_df = extract_all(q_categories)
                print(extracted_df)

            else: 
                q_range_start = input("Enter start date in form YYYY-MM-DD: \n")
                q_range_end = input("Enter end date in form YYYY-MM-DD: \n")
                extracted_df = extract_within_range(q_categories, q_range_start, q_range_end)
                print(extracted_df)

            print()
            for key in q_categories: 
                print(categories_dict[key])
            print("THE SUMMED BALANCE OF THE ABOVE CATEGORIES IS:  $" + str(extracted_df[' Transaction Amount'].sum()) + ". \n")
                
        elif user_sel == '4': 
            m_file_name = 'monthly_record.csv'
            m_file_path = os.path.join(current_directory, m_file_name)
            
            if os.path.isfile(m_file_path): 
                print()
                m_df = pd.read_csv(m_file_path)
                last_month = str(m_df['Month'].iloc[-1])
                day = 1
                last_month_date = datetime.strptime(f"{last_month}-{day}", "%Y-%m-%d")
                
                most_recent_date = str(p_df['Date Posted'].iloc[-1])
                most_recent_date = datetime.strptime(most_recent_date, "%Y-%m-%d").date()
                
                start_date = get_start_date(p_df['Date Posted'], last_month_date)
                end_date = get_end_date(p_df['Date Posted'], most_recent_date)
                
                added_month_df = calc_month_data(start_date, end_date)
                
                m_df.drop(m_df.index[-1], inplace=True)
                
                m_df = m_df.append(added_month_df, ignore_index=True)
                
                
                
                #very unfinished, replace old m_df csv with new one
                

                
            else: 
                print("monthly file does not exist \n")
                #create new monthly data file
                
                m_df = calc_month_data()
                
                
                m_df.to_csv(p_file_path, index = False)
                
            
        
        elif user_sel == '5': 
            print("5 \n")
            
        elif user_sel == 'q': 
            break      

        user_sel = selector()
else: 
    print()
    ans = input("Personal Record does not exist. If you want to initiate one, press 'y'. Otherwise press anything else to quit. \n")
    
    if ans == 'y': 
        subprocess.run(["python", dep_path])








