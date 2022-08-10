import plotly.express as px
import pandas as pd

from datetime import datetime, timedelta

from kumareport.database import Database


def show_chart_plotly(days, tagname=None):
    date = datetime.now() - timedelta(days=days)

    db = Database.db

    excel = {}
    cur = db.cursor()
    if tagname == None or tagname == '':
        cur.execute('SELECT monitor.id, monitor.name from monitor JOIN monitor_tag on (monitor.id = monitor_tag.monitor_id) JOIN tag on (tag.id = monitor_tag.tag_id) where monitor.active = 1')
    else:
        cur.execute('SELECT monitor.id, monitor.name from monitor JOIN monitor_tag on (monitor.id = monitor_tag.monitor_id) JOIN tag on (tag.id = monitor_tag.tag_id) where tag.name = ? and monitor.active = 1', (tagname, ))
    result = cur.fetchall()
    
    for i in result:
        mon_id = i[0]
        mon_name = i[1]

        if result == None:
            continue
        else:
            if 'Id' not in excel:
                excel['Id'] = {}
            if 'Name' not in excel:
                excel['Name'] = {}
            if 'Uptime' not in excel:
                excel['Uptime'] = {}
            excel['Id'][i] = mon_id
            excel['Name'][i] = str(mon_name)
            excel['Uptime'][i] = int(db.percent_by_monitor_id(mon_id, date))

    data = pd.DataFrame.from_dict(excel)
    fig = px.bar(data, x='Name', y='Uptime', hover_data=['Name'])
    fig.show()