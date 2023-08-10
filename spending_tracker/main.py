import subprocess
import os
from calculation import *
current_directory = os.path.dirname(os.path.abspath(__file__))

dep = "data_entry_process.py"
dep_path = os.path.join(current_directory, dep)



def selector(): 
    print()
    selector = input("SELECT WHAT TO DO: \n \
                     Enter '1' for transaction entry through csv statement file \n \
                     Enter '2' to see spending overview: by category and income vs. expense\n \
                     Enter '3' to extract record for selected categories and date\n \
                     Enter '4' to compare total expense across each monthly period \n \
                     Enter '5' to see undetermined items and add description \n \
                     Enter 'q' to quit: \n")
    return selector

#body

user_sel = selector()

while user_sel != 'q': 

    if user_sel == '1': 
        subprocess.run(["python", dep_path])

    elif user_sel == '2': 
        spending_overview()

    elif user_sel == '3': 
        print('run 3\n')
    elif user_sel == '4': 
        print('run 4\n')  
    elif user_sel == 'q': 
        break      

    user_sel = selector()

