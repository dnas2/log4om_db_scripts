#!/usr/bin/python

import sys
import MySQLdb

filepath = sys.argv[1]
database = sys.argv[2]

print "Connect to database " + database
print "Using ADIF file " + filepath

db = MySQLdb.connect(host = "[SERVER]",
                     user = "[USER]",
                     passwd = "[PASSWORD]",
                     db = database)
cur = db.cursor()

reached_eoh = False
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
        if (reached_eoh == True):
                qsoData = line.split("<")
                qso = {}
                for qsoField in qsoData:
                        if (":" in qsoField):
                                endFieldKeyPos = qsoField.find(":")
                                startFieldValuePos = qsoField.find(">")
                                qsoFieldKey = qsoField[0:endFieldKeyPos].lower()
                                qsoFieldVal = qsoField[(startFieldValuePos+1):]
                                qso[qsoFieldKey] = qsoFieldVal
                #for key in qso:
                        #print key + " : " + qso[key]
                update =  "UPDATE `log` SET "
                update += "QslRcvd = '" + qso['qsl_rcvd'] + "', "
                update += "QslRDate = '" + qso['qslrdate'] + "', "
                update += "QslRcvdVia = '" + qso['qsl_rcvd_via'] + "', "
                update += "QslSentVia = '" + qso['qsl_sent_via'] + "', "
                update += "QslSent = '" + qso['qsl_sent'] + "'"
                if "email" in qso:
                        update += ", Email = '" + qso['email'] + "'"
                if "address" in qso:
                        update += ", Address = '" + qso['address'] + "'"
                if "notes" in qso:
                        update += ", Notes = '" + qso['notes'] + "'"
                update += " WHERE"
                update += " (`Call`='" + qso['call'] + "' AND"
                update += " QsoDate=" + qso['qso_date'] + " AND"
                update += " TimeOn=" + qso['time_on'] + " AND"
                update += " Band='" + qso['band'].lower() + "' AND"
                update += " `Mode`='" + qso['mode'] + "') LIMIT 1;"
                cur.execute(update)
		print("Affected Rows = {}".format(cur.rowcount))
		db.commit()
		print update
        if ("<EOH>" in line):
                reached_eoh = True
        line = fp.readline()
        cnt += 1
db.close()

