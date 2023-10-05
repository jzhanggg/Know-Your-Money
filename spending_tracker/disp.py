import pandas as pd
import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
import matplotlib.pyplot as plt


class DataFrameTableApp(tk.Frame):
    def __init__(self, parent=None, dataframe=None, description=None):
        tk.Frame.__init__(self, parent)
        self.dataframe = dataframe
        self.description = description
        self.parent = parent
        self.main = self._frame = ttk.Frame(self.parent)
        self.main.pack(fill='both', expand=True)

        # Create a frame to hold the description label and the table
        self.content_frame = ttk.Frame(self.main)
        self.content_frame.pack(fill='both', expand=True)
        
        # Create a label widget for the description and add it to the content frame
        self.description_label = tk.Label(self.content_frame, text=self.description, wraplength=300)
        self.description_label.pack()

        # Create a frame to hold the table
        self.table_frame = ttk.Frame(self.content_frame)
        self.table_frame.pack(fill='both', expand=True)

        # Create the table using PandasTable
        self.table = Table(self.table_frame, dataframe=self.dataframe, cellwidth=250, cellheight=50)
        self.table.show()

def show_df_with_description(display_df, str_title, description = None): 
    display_df = display_df.applymap(lambda x: '{:.2f}'.format(x) if isinstance(x, (int, float)) else x)

    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    root = tk.Tk()
    root.title(str_title)
    
    app = DataFrameTableApp(root, dataframe=display_df, description=description)
    app.pack(fill='both', expand=True)
    
    root.mainloop()
    
def show_c_p_s_line_graph(month_df, month_col_name, covered_balance_col_name, personal_balance_col_name, savings_col_name): 
    plt.figure(figsize=(10, 6))

    plt.plot(month_df[month_col_name], month_df[covered_balance_col_name], label='Covered Balance')
    plt.plot(month_df[month_col_name], month_df[personal_balance_col_name], label='Personal Balance')
    plt.plot(month_df[month_col_name], month_df[savings_col_name], label='Savings Balance')

    plt.xlabel('Time Period in Months')
    plt.ylabel('Money in CDN')
    plt.title('Graph of Covered Balance, Personal Balance, and Savings Balance')
    plt.legend()  

    plt.show()







