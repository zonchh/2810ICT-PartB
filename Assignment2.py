import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt
# plt.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# initialise the tkinter GUI
root = tk.Tk()
root.title('Victoria Crash Analysis Tool')
root.geometry("1000x800")  # set the root dimensions
root.pack_propagate(False)  # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0)  # makes the root window fixed in size.

#####################
### SEARCH FRAME ###
#####################
# Frame for load and searching
search_frame = tk.LabelFrame(root, text="Search Criteria")
search_frame.place(height=150, width=350)

# StartDate
tk.Label(search_frame, text='Enter Start Date:').place(rely=0.0, relx=0)
startdate = tk.Entry(search_frame)
startdate.insert(tk.END, "01-07-2016")
startdate.place(rely=0.0, relx=0.3)
ttk.Label(search_frame, text='DD-MM-YYYY').place(rely=0.0, relx=0.6)

# EndDate
tk.Label(search_frame, text='Enter End Date:').place(rely=0.2, relx=0)
enddate = tk.Entry(search_frame)
enddate.insert(tk.END, "01-11-2016")
enddate.place(rely=0.2, relx=0.3)
ttk.Label(search_frame, text='DD-MM-YYYY').place(rely=0.2, relx=0.6)

# Keyword
ttk.Label(search_frame, text='Keyword Search:').place(rely=0.4, relx=0)
keyword = tk.Entry(search_frame)
keyword.place(rely=0.4, relx=0.3)
ttk.Label(search_frame, text='Searches the').place(rely=0.35, relx=0.6)
ttk.Label(search_frame, text='ACCIDENT_TYPE field.').place(rely=0.47, relx=0.6)

# Display keywords
button2 = tk.Button(search_frame, text="List of Possible Keywords", command=lambda: Load_keywords())
button2.place(rely=0.7, relx=0.55)

# Search button
button3 = tk.Button(search_frame, text="Show Data", command=lambda: Load_csv_data())
button3.place(rely=0.7, relx=0.3)

####################
### REPORT FRAME ###
####################
# Frame for load and searching
report_frame = tk.LabelFrame(root, text="Reports")
report_frame.place(height=150, width=300, rely=0.0, relx=0.5)

# Show chart
button3 = tk.Button(report_frame, text="Accidents Per Hour", command=lambda: show_plot_1())
button3.place(rely=0.0, relx=0.0)
button4 = tk.Button(report_frame, text="Effect of Alcohol on Occurrence of Road Accidents", command=lambda: show_plot_2())
button4.place(rely=0.2, relx=0.0)
button5 = tk.Button(report_frame, text="Trends of Accidents Influenced by Alcohol", command=lambda: show_plot_3())
button5.place(rely=0.4, relx=0.0)
button6 = tk.Button(report_frame, text="Days of the Week with Most Accidents", command=lambda: show_plot_4())
button6.place(rely=0.6, relx=0.0)

#####################
### RESULTS FRAME ###
#####################
# Frame for Results
resultsFrame = tk.LabelFrame(root, text="Results")
resultsFrame.place(height=645, width=999, rely=0.20, relx=0)

# Treeview Widget
tv1 = ttk.Treeview(resultsFrame)
tv1.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).
treescrolly = tk.Scrollbar(resultsFrame, orient="vertical", command=tv1.yview)  # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(resultsFrame, orient="horizontal", command=tv1.xview)  # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

def show_plot_4():
    # R6.1 The software shall analyse which days of the week have the most traffic accidents.
    file_path = 'Crash Statistics Victoria.csv'
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_csv(excel_filename)
        df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'], dayfirst=True) # Convert the ACCIDENT_DATE to a DateTime
        startdatevalue = startdate.get()
        enddatevalue = enddate.get()
        keywordValue = keyword.get()
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                mask = ((df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) &
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))) & \
                       df['ACCIDENT_TYPE'].str.contains(keywordValue)
            else:
                mask = (df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) & \
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))

            df = df.loc[mask]
        else:
            if keywordValue != '':
                mask = (df['ACCIDENT_TYPE'].str.contains(keywordValue))
                df = df.loc[mask]

        # Create the plot
        plt.clf()  # Clear the plot if it already exists
        # Add series plot for Alcohol based accidents
        dfDay = df
        dfDay = dfDay.groupby(['DAY_OF_WEEK'])['OBJECTID'].size().reset_index(name='counts')
        plt.pie(dfDay['counts'],
                labels= dfDay['DAY_OF_WEEK'],
                startangle=45,
                shadow=True,
                autopct='%1.2f%%')
        plt.suptitle('Days of the Week with Most Accidents', fontsize=15)
        # Setup subtitle
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                plt.title(
                    'Between ' + startdatevalue + ' and ' + enddatevalue + ' and Accident Type like ' + keywordValue,
                    fontsize=12)
            else:
                plt.title('Between ' + startdatevalue + ' and ' + enddatevalue, fontsize=12)
        # plot the graph
        plt.show()


    except ValueError:
        tk.messagebox.showerror("Information", "An error occurred: " + ValueError)
    return None

def show_plot_3():
    # R5.2 The software shall analyse the trends of alcohol on the occurrence of road accidents.
    file_path = 'Crash Statistics Victoria.csv'
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_csv(excel_filename)
        df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'], dayfirst=True) # Convert the ACCIDENT_DATE to a DateTime
        startdatevalue = startdate.get()
        enddatevalue = enddate.get()
        keywordValue = keyword.get()
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                mask = ((df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) &
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))) & \
                       df['ACCIDENT_TYPE'].str.contains(keywordValue)
            else:
                mask = (df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) & \
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))

            df = df.loc[mask]
        else:
            if keywordValue != '':
                mask = (df['ACCIDENT_TYPE'].str.contains(keywordValue))
                df = df.loc[mask]

        # Create the plot
        plt.clf()  # Clear the plot if it already exists
        # Add series plot for Alcohol based accidents
        dfAlcohol = df
        dfAlcohol = dfAlcohol.loc[dfAlcohol['ALCOHOLTIME'] == 'Yes']
        dfAlcohol = dfAlcohol.groupby(['ACCIDENT_TYPE'])['OBJECTID'].size().reset_index(name='counts')
        plt.pie(dfAlcohol['counts'],
                labels= dfAlcohol['ACCIDENT_TYPE'],
                startangle=45,
                shadow=True,
                autopct='%1.2f%%')
        plt.suptitle('Trends of Accidents Influenced by Alcohol', fontsize=15)
        # Setup subtitle
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                plt.title(
                    'Between ' + startdatevalue + ' and ' + enddatevalue + ' and Accident Type like ' + keywordValue,
                    fontsize=12)
            else:
                plt.title('Between ' + startdatevalue + ' and ' + enddatevalue, fontsize=12)
        # plot the graph
        plt.show()


    except ValueError:
        tk.messagebox.showerror("Information", "An error occurred: " + ValueError)
    return None

def show_plot_2():
    # R5.1 The software shall analyse the effect of alcohol on the occurrence of road accidents.
    file_path = 'Crash Statistics Victoria.csv'
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_csv(excel_filename)
        df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'], dayfirst=True) # Convert the ACCIDENT_DATE to a DateTime
        startdatevalue = startdate.get()
        enddatevalue = enddate.get()
        keywordValue = keyword.get()
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                mask = ((df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) &
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))) & \
                       df['ACCIDENT_TYPE'].str.contains(keywordValue)
            else:
                mask = (df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) & \
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))

            df = df.loc[mask]
        else:
            if keywordValue != '':
                mask = (df['ACCIDENT_TYPE'].str.contains(keywordValue))
                df = df.loc[mask]

        # Create the plot
        plt.clf()  # Clear the plot if it already exists
        # Add series plot for Alcohol based accidents
        dfAlcohol = df
        dfAlcohol = dfAlcohol.loc[dfAlcohol['ALCOHOLTIME'] == 'Yes']
        dfAlcohol = dfAlcohol.groupby(['ACCIDENT_DATE'])['OBJECTID'].size().reset_index(name='counts')
        plt.plot(dfAlcohol['ACCIDENT_DATE'], dfAlcohol['counts'], label='Alcohol Related', color='red')
        plt.suptitle('Effect of Alcohol on Occurrence of Road Accidents', fontsize=15)
        # Setup subtitle
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                plt.title(
                    'Between ' + startdatevalue + ' and ' + enddatevalue + ' and Accident Type like ' + keywordValue,
                    fontsize=12)
            else:
                plt.title('Between ' + startdatevalue + ' and ' + enddatevalue, fontsize=12)
        #plt.show()
        # Add series plot for non Alcohol based accidents
        dfNoAlcohol = df
        dfNoAlcohol = dfNoAlcohol.loc[dfNoAlcohol['ALCOHOLTIME'] == 'No']
        dfNoAlcohol = dfNoAlcohol.groupby(['ACCIDENT_DATE'])['OBJECTID'].size().reset_index(name='counts')
        plt.plot(dfNoAlcohol['ACCIDENT_DATE'], dfNoAlcohol['counts'], label='Not Alcohol Related', color='green')
        # Add Legend
        plt.legend(title='Status')
        # Add axis labels
        plt.ylabel('Accidents', fontsize=12)
        plt.xlabel('Dates', fontsize=12)
        # plot the graph
        plt.show()


    except ValueError:
        tk.messagebox.showerror("Information", "An error occurred: " + ValueError)
    return None


def show_plot_1():
    # R3.1 The software shall display the average amount of traffic accidents in each hour of the day in relation to a user-input time frame.
    file_path = 'Crash Statistics Victoria.csv'
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_csv(excel_filename)
        #df['ACCIDENT_TIME'] = pd.to_datetime(str(df['ACCIDENT_DATE']) + str(df['ACCIDENT_TIME']), format = '%d-%m-%Y%H.%M.%S', dayfirst=True)
        df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'], dayfirst=True) # Convert the ACCIDENT_DATE to a DateTime
        #df['HOUR_OF_DAY'] = pd.date_range('ACCIDENT_TIME', periods=24, freq='60min')
        startdatevalue = startdate.get()
        enddatevalue = enddate.get()
        keywordValue = keyword.get()
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                mask = ((df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) & \
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))) & \
                       df['ACCIDENT_TYPE'].str.contains(keywordValue)
            else:
                mask = (df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) & \
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))

            df = df.loc[mask]
        else:
            if keywordValue != '':
                mask = (df['ACCIDENT_TYPE'].str.contains(keywordValue))
                df = df.loc[mask]

        # Create the plot
        plt.clf()  # Clear the plot if it already exists
        df = df.groupby(['ACCIDENT_DATE'])['OBJECTID'].size().reset_index(name='counts')
        # https://matplotlib.org/stable/tutorials/introductory/pyplot.html
        plt.bar(df['ACCIDENT_DATE'], df['counts'] / 24)  # Group by ACCIDENT_DATE and divide count of OBJECTID by 24 hours to get accidents per day
        plt.suptitle('Accidents Per Hour', fontsize=15)
        # Setup subtitle
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                plt.title('Between ' + startdatevalue + ' and ' + enddatevalue + ' and Accident Type like ' + keywordValue, fontsize=12)
            else:
                plt.title('Between ' + startdatevalue + ' and ' + enddatevalue, fontsize=12)
        # Add axis labels
        plt.ylabel('Daily Accidents per hour', fontsize=12)
        plt.xlabel('Dates', fontsize=12)
        # plot the graph
        plt.show()

    except ValueError:
        tk.messagebox.showerror("Information", "An error occurred: " + ValueError)
    return None

def Load_keywords():
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = 'Crash Statistics Victoria.csv'
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_csv(excel_filename)

    except ValueError:
        tk.messagebox.showerror("Information", "An error occurred: " + ValueError)
        return None


    # Handle creation of the data view
   # clear_grid_data()
    df = (df['ACCIDENT_TYPE'].unique())
    keywordlist = '\n'.join(df.tolist())
    tk.messagebox.showinfo("Keyword List", keywordlist)

    return None

def Load_csv_data():
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = 'Crash Statistics Victoria.csv'
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_csv(excel_filename)
        df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'], dayfirst=True) # Convert the ACCIDENT_DATE to a DateTime
        startdatevalue = startdate.get()
        enddatevalue = enddate.get()
        keywordValue = keyword.get()
        if startdatevalue != '' and enddatevalue != '':
            if keywordValue != '':
                mask = ((df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) & \
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))) & \
                       df['ACCIDENT_TYPE'].str.contains(keywordValue)
            else:
                mask = (df['ACCIDENT_DATE'] > datetime.strptime(startdatevalue, '%d-%m-%Y')) & \
                       (df['ACCIDENT_DATE'] <= datetime.strptime(enddatevalue, '%d-%m-%Y'))

            df = df.loc[mask]
        else:
            if keywordValue != '':
                mask = (df['ACCIDENT_TYPE'].str.contains(keywordValue))
                df = df.loc[mask]

    except ValueError:
        tk.messagebox.showerror("Information", "An error occurred: " + ValueError)
        return None

    df = df.sort_values(by=['ACCIDENT_DATE'], ascending=False)

    # Handle creation of the data view
    clear_grid_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

    return None

def clear_grid_data():
    tv1.delete(*tv1.get_children())
    return None


root.mainloop()