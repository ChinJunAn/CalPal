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
                FOOD TEXT NOT NULL,
                CALORIES REAL NOT NULL);''')
    conn.execute('''CREATE TABLE CALORIESOUT
            (TIME TEXT PRIMARY KEY NOT NULL,
                CALORIES REAL NOT NULL);''')
    conn.close()

def insertCaloriesIn(caloriesIn, item):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()   
    cursor.execute("INSERT INTO CALORIESIN (TIME, FOOD, CALORIES) VALUES (?, ?, ?)",(formatted_datetime, item, caloriesIn))
    conn.commit()
    conn.close()

def revertCaloriesIn():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Check if the table is not empty
    cursor.execute("SELECT count(*) FROM CALORIESIN;")
    count = cursor.fetchone()[0]
    print(count)
    if count > 0:
        # Remove the latest entry from the table
        cursor.execute("DELETE FROM CALORIESIN WHERE rowid = (SELECT max(rowid) FROM CALORIESIN);")
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

def revertCaloriesOut():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Check if the table is not empty
    cursor.execute("SELECT count(*) FROM CALORIESOUT;")
    count = cursor.fetchone()[0]
    if count > 0:
        # Remove the latest entry from the table
        cursor.execute("DELETE FROM CALORIESOUT WHERE rowid = (SELECT max(rowid) FROM CALORIESOUT);")
    conn.commit()
    conn.close()

def updateGraph():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Retrieve data from the first table
    cursor.execute("SELECT TIME, FOOD, CALORIES FROM CALORIESIN")
    data_table1 = cursor.fetchall()

    # Retrieve data from the second table
    cursor.execute("SELECT TIME, CALORIES FROM CALORIESOUT")
    data_table2 = cursor.fetchall()

    conn.close()

    df_table1 = pd.DataFrame(data_table1, columns=['TIME', 'FOOD', 'CALORIES'])
    df_table2 = pd.DataFrame(data_table2, columns=['TIME', 'CALORIES'])

    np_table1 = df_table1.to_numpy()
    np_table2 = df_table2.to_numpy()

    # Combine TIME and FOOD for the x-axis labels
    x_labels_table1 = [f"{time} - {food}" for time, food in zip(np_table1[:, 0], np_table1[:, 1])]

    plt.figure(figsize=(10, 10))  # Adjust the figure size as needed
    plt.plot(np_table1[:, 0], np_table1[:, 2], label='Calories-In', marker='o')
    plt.plot(np_table2[:, 0], np_table2[:, 1], label='Calories-Out', marker='x')
    
    plt.xlabel('Time and Food')
    plt.ylabel('Calories')
    plt.xticks(np_table1[:, 0], x_labels_table1, rotation=10)
    plt.legend()  # Show the legend with labels for each line
    plt.grid(True)  # Add a grid if desired
    plt.savefig('static/line_graph.png')