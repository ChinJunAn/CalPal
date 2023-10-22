import sqlite3
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def createDB():
    try:
        os.remove('database.db')
    except OSError:
        pass
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE CALORIESIN
            (TIME TEXT PRIMARY KEY NOT NULL,
                CALORIES REAL NOT NULL);''')
    conn.execute('''CREATE TABLE CALORIESOUT
            (TIME TEXT PRIMARY KEY NOT NULL,
                CALORIES REAL NOT NULL);''')
    conn.close()

def insertCaloriesIn(caloriesIn):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()   
    cursor.execute("INSERT INTO CALORIESIN (TIME, CALORIES) VALUES (?, ?)",(formatted_datetime, caloriesIn))
    conn.commit()
    conn.close()

def insertCaloriesOut(caloriesOut):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()   
    cursor.execute("INSERT INTO CALORIESOUT (TIME, CALORIES) VALUES (?, ?)",(formatted_datetime, caloriesOut))
    conn.commit()
    conn.close()
    
def updateGraph():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Retrieve data from the first table
    cursor.execute("SELECT TIME, CALORIES FROM CALORIESIN")
    data_table1 = cursor.fetchall()

    # Retrieve data from the second table
    cursor.execute("SELECT TIME, CALORIES FROM CALORIESOUT")
    data_table2 = cursor.fetchall()

    conn.close()

    df_table1 = pd.DataFrame(data_table1, columns=['x', 'y1'])
    df_table2 = pd.DataFrame(data_table2, columns=['x', 'y2'])

    np_table1 = df_table1.to_numpy()
    np_table2 = df_table2.to_numpy()

    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.plot(np_table1[:, 0], np_table1[:, 1], label='Calories-In', marker='o')
    plt.plot(np_table2[:, 0], np_table2[:, 1], label='Calories-Out', marker='x')
    plt.xlabel('Time')
    plt.ylabel('Calories')
    #plt.title('Line Graph with Two Lines')
    plt.legend()  # Show the legend with labels for each line
    plt.grid(True)  # Add a grid if desired
    plt.savefig('static/line_graph.png')