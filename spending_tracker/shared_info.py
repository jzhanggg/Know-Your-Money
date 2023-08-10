from datetime import date
from datetime import timedelta

categories_dict = {
    'h' : "Hoyoverse Games",
    'g' : "Non-Hoyoverse Games",
    'c' : "car",
    'l' : "leisure events",
    's' : "study",
    'm' : "music",
    'd' : "drinks",
    'n' : "necessary items/fees",
    'o' : "other personal items/fees",
    'i' : "income", 
    'r' : "reimbursement from dad",
    'sv' : "savings: transferred to savings acc",
    'u' : "undetermined, ATTENTION NEEDED"
}

covered_balance = ['n', 's', 'r', 'c']
personal_balance = ['h', 'g', 'l', 'm', 'd', 'o', 'i', 'sv']
temp_exclusion = ['u']

def get_start_date(df_date_col, given_start_date):
    if (df_date_col != given_start_date).all(): 
        next_date = None
        for date in df_date_col: 
            if date > given_start_date: 
                return date 
    return given_start_date

def get_end_date(df_date_col, given_end_date):           
    if (df_date_col != given_end_date).all(): 
        prev_date = None
        for date in df_date_col: 
            if date < given_end_date: 
                prev_date = date
            else: 
                return prev_date
    return given_end_date