import requests
import sqlite3
import json

endpoint = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
series_id = "CUUR0000SA0L1E"


conn = sqlite3.connect('currency.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Inflation
        (cpi REAL, date TEXT)''')


headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": [series_id], "startyear":"2014", "endyear":"2018"})
p = requests.post(endpoint, data=data, headers=headers)
json_data = json.loads(p.text)

values = json_data['Results']['series'][0]['data']

for i in values:
    date = i["year"] + "-" + i["period"][1:] + "-01"
    c.execute(('INSERT INTO Inflation (cpi,date) VALUES (?,?)'),
              (float(i["value"]), date))

conn.commit()
