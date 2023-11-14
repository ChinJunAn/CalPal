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
                ACTIVITY TEXT NOT NULL,
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

def getTotalCaloriesIn():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()   
    cursor.execute("SELECT SUM(CALORIES) FROM CALORIESIN;")
    sum = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()
    return sum

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

def insertCaloriesOut(caloriesOut, activity):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()   
    cursor.execute("INSERT INTO CALORIESOUT (TIME, ACTIVITY, CALORIES) VALUES (?, ?, ?)",(formatted_datetime, activity, caloriesOut))
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

def getTotalCaloriesOut():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()   
    cursor.execute("SELECT SUM(CALORIES) FROM CALORIESOUT;")
    sum = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()
    return sum

def checkAggregate():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
        (SELECT COUNT(*) FROM CALORIESIN) > 0 AND
        (SELECT COUNT(*) FROM CALORIESOUT) > 0 AS both_tables_have_entries;
    """)
    result = cursor.fetchone()
    both_tables_have_entries = bool(result[0])
    conn.close()
    return both_tables_have_entries

def updateGraph():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Retrieve data for calories taken in
    cursor.execute("SELECT TIME, CALORIES FROM CALORIESIN")
    data_calories_in = cursor.fetchall()

    # Retrieve data for calories burnt
    cursor.execute("SELECT TIME, CALORIES FROM CALORIESOUT")
    data_calories_out = cursor.fetchall()

    conn.close()

    # Create dataframes for each dataset
    df_calories_in = pd.DataFrame(data_calories_in, columns=['TIME', 'CALORIES_IN'])
    df_calories_out = pd.DataFrame(data_calories_out, columns=['TIME', 'CALORIES_OUT'])

    # Merge data on the 'TIME' column to align the time values
    merged_data = pd.merge(df_calories_in, df_calories_out, on='TIME', how='outer')

    # Sort the merged dataframe based on the 'TIME' column
    merged_data.sort_values(by='TIME', inplace=True)

    # Cumulative sum for calories taken in and calories burnt
    merged_data['CUMULATIVE_CALORIES_IN'] = merged_data['CALORIES_IN'].cumsum()
    merged_data['CUMULATIVE_CALORIES_OUT'] = merged_data['CALORIES_OUT'].cumsum()

    # Interpolate to fill missing values and create a smooth line
    merged_data.interpolate(inplace=True)
    np_merged = merged_data.to_numpy()

    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

    # Plot the cumulative line for calories taken in
    plt.plot(np_merged[:, 0], np_merged[:, 3], label='Cumulative Calories-In', marker='o', color='blue', linestyle='-')

    # Plot the cumulative line for calories burnt
    plt.plot(np_merged[:, 0], np_merged[:, 4], label='Cumulative Calories-Out', marker='x', color='red', linestyle='-')

    plt.xlabel('Time')
    plt.ylabel('Cumulative Calories')
    plt.legend()  # Show the legend with labels for each line
    plt.grid(True)  # Add a grid if desired
    plt.title('Cumulative Calories In and Out Over Time')
    plt.savefig('static/line_graph.png')
