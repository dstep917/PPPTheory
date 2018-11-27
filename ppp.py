import requests
import sqlite3

endpoint = "http://data.fixer.io/api/"
access_key = "?access_key=bbb321bafac491552eaffdfda81ed717"
bases = ["USD"]

conn = sqlite3.connect('currency.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Currency
        (base TEXT, non_ref TEXT, value REAL, date TEXT)''')

for i in range(2004,2018):
    for j in range(1,13):
        for b in bases:
            date = str(i) + "-" + str(j).zfill(2) + "-01"
            r = requests.get(endpoint + date + access_key)
            if r.status_code != 200:
                print("Error:\n" + repr(r))

            js = r.json()
            if not js['success']:
                print(endpoint + date + access_key)
                print(r.json())

            rates = js['rates']
            for r in rates.keys():
                n = rates[r]
                c.execute(('INSERT INTO Currency (base,non_ref,value,date) VALUES (?,?,?,?)'),
                          (b, r, n, date))

conn.commit()
            

            

##r = requests.get((endpoint + "{YYYY}-{MM}-{DD}" + access_key).format(
##    YYYY = "2000",
##    MM = "01",
##    DD = "01"))
