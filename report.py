from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Error
import sys


def show_chart_plotly(ids, days):
    import plotly.express as px
    import pandas as pd

    date = datetime.now() - timedelta(days=days)

    excel = {}
    for i in ids:
        cur = conn.cursor()
        cur.execute("SELECT name FROM monitor WHERE id=?", (i, ))
        result = cur.fetchone()
        if result == None:
            continue
        else:
            if 'Id' not in excel:
                excel['Id'] = {}
            if 'Name' not in excel:
                excel['Name'] = {}
            if 'Uptime' not in excel:
                excel['Uptime'] = {}
            excel['Id'][i] = i
            excel['Name'][i] = str(result[0])
            excel['Uptime'][i] = int(percent_by_monitor_id(i, date))

    data = pd.DataFrame.from_dict(excel)
    fig = px.bar(data, x='Name', y='Uptime', hover_data=['Name'])
    fig.show()

    return data


def show_chart_matplotlib(ids):
    import matplotlib.pyplot as plt

    lefts = []
    counter = 1
    percents = {}
    names = {}

    for i in ids:
        cur = conn.cursor()
        cur.execute("SELECT name FROM monitor WHERE id=?", (i, ))
        result = cur.fetchone()
        if result == None:
            continue
        else:
            lefts.append(counter)
            counter += 1
            names[i] = result[0]
            percents[i] = int(percent_by_monitor_id(i))
    
    left = list(lefts)
    height = list(percents.values())
    tick_label = list(lefts)
    
    plt.bar(left, height, tick_label = tick_label, width = 0.8, color = ['green'])
    plt.xlabel('Systems')
    plt.ylabel('UpTime')
    plt.title('HeartBeat')
    plt.show()


def create_connection(kumadb):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(kumadb)
    except Error as e:
        print(e)

    return conn


def count_heartbeat_by_status(monitor_id, status, date):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM heartbeat WHERE monitor_id=? AND status=? AND time>?", (monitor_id, status, date))
    result = cur.fetchone()

    return result[0]


def percent_by_monitor_id(monitor_id, date):
    rows = count_heartbeat_by_monitor_id(monitor_id, date)
    result = count_heartbeat_by_status(monitor_id, 1, date)

    if rows == 0:
        return 0

    percentage = (result / rows) * 100
    return percentage


def count_heartbeat_by_monitor_id(monitor_id, date):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM heartbeat WHERE monitor_id=? AND time>?", (monitor_id, date))

    rows = cur.fetchone()

    return rows[0]
 

def main(args):
    global conn

    if len(args) != 2:
        print('Usage: python report.py UPTIME_KUMA_DATABASE_FILE')
        exit(1)

    DATABASE = args[1]

    # create a database connection
    conn = create_connection(DATABASE)
    with conn:
        ids = [35, 77, 78, 80, 81, 83, 84, 85, 39, 108, 7, 102, 103, 89, 94, 95, 131, 130, 132, 100, 75, 2, 87, 92] # list of IDs of monitors to report
        days = 30 # days to report
        data = show_chart_plotly(ids, days)

        uptime_sum = 0
        for i in data['Uptime'].index:
            uptime_sum += data['Uptime'][i]
        print(uptime_sum / len(ids))

        
if __name__ == '__main__':
    main(sys.argv)