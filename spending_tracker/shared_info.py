from datetime import datetime
import os


p_filename = 'personal_record.csv'
current_directory = os.path.dirname(os.path.abspath(__file__))
p_file_path = os.path.join(current_directory, p_filename)

m_file_name = 'monthly_record.csv'
m_file_path = os.path.join(current_directory, m_file_name)

dep = "data_entry_process.py"
dep_path = os.path.join(current_directory, dep)

categories_dict = {
    'h' : "Hoyoverse Games",
    'g' : "Non-Hoyoverse Games",
    'c' : "car/transport 汽车/交通费用",
    'l' : "leisure events",
    's' : "study",
    'm' : "music",
    'd' : "drinks personal",
    'f' : "food personal",
    'n' : "necessary items/fees 生活刚需费用",
    'o' : "other personal items/fees",
    'i' : "income", 
    'r' : "reimbursement from dad 妈咪爹地给的money",
    'sv' : "savings: transferred to savings acc",
    'osv' : "out of savings: to chequing" 
}

covered_balance = ['n', 's', 'r', 'c']
personal_balance = ['h', 'g', 'l', 'm', 'd', 'f', 'o', 'i', 'sv', 'osv']

#get a start date within the bounds from input and is also the nearest day to the start date in which transaction happens
def get_start_date(df_date_col, given_start_date):
    if (df_date_col != given_start_date).all(): 
        next_date = None
        for date in df_date_col: 
            if date > given_start_date: 
                return date 
    return given_start_date

#get an end date within the bounds from input and is also the nearest day to the end date in which day in which transaction happens
def get_end_date(df_date_col, given_end_date):           
    if (df_date_col != given_end_date).all(): 
        prev_date = None
        for date in df_date_col: 
            if date < given_end_date: 
                prev_date = date
            else: 
                return prev_date
    return given_end_date