import subprocess
import os
from calculation import *
from shared_info import *
current_directory = os.path.dirname(os.path.abspath(__file__))

dep = "data_entry_process.py"
dep_path = os.path.join(current_directory, dep)

# ERROR HANDLE: throw error for date entered out of bound, ask user to input correct date in range and display date range in record

def selector(): 
    print()
    selector = input("SELECT WHAT TO DO: \n \
                     Enter '1' for transaction entry through csv statement file \n \
                     Enter '2' to see spending overview: by category and income vs. expense\n \
                     Enter '3' to extract record for selected categories and date\n \
                     Enter '4' to save newest monthly expense data \n \
                     Enter '5' to compare total expense across each monthly period \n \
                     Enter 'q' to quit: \n")
    return selector

#body

user_sel = selector()
extracted_df = pd.DataFrame()

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
        print('run 4\n')  
    elif user_sel == 'q': 
        break      

    user_sel = selector()

