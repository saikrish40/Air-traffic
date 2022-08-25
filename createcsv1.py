import sys
import csv
import os
import sqlite3

con = sqlite3.connect('Project.db')

cur = con.cursor()
cur.execute('SELECT * FROM traffic;')
rows = cur.fetchall()
fp = open('traffic1.csv', 'w')
myFile = csv.writer(fp)
myFile.writerows(rows)
fp.close()
print('traffic1.csv file successfully created')
con.commit()
