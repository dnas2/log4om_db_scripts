import MySQLdb
import gc
from qsoRowsAsAdif import qsoRowsAsAdif
from datetime import date, timedelta

databaseNames = {"log4om_m0blf":"M0BLF"}
today = date.today()
firstOfMonth = today.replace(day=1)
lastMonth = firstOfMonth - timedelta(days=1)
oneMonthAgo = lastMonth.strftime('%Y%m')
thisMonth = firstOfMonth.strftime('%Y%m')
searchContestsQuery = "SELECT DISTINCT(ContestId) FROM `log` WHERE QsoDate>" + oneMonthAgo + "00 AND QsoDate<" + thisMonth + "00 AND ContestId IS NOT NULL AND ContestId!='' " 
dirList = open("/var/www/html/logs/contests/contests.txt","a")
print searchContestsQuery
for useDb in databaseNames:
	db = MySQLdb.connect(host="[SERVER]", port=3306, user="[USER]", passwd="[PASSWORD]", db=useDb)
	cursor = db.cursor()
	cursor.execute(searchContestsQuery)
	data = cursor.fetchall()
	if data != None:
		for contestRow in data:
			contestQsosQuery = "SELECT StationCallsign, QsoDate, TimeOn, `Call`, Band, `Mode`, RstSent, Srx, SrxString, RstRcvd, Stx, StxString, Contest FROM log WHERE ContestId='" + contestRow[0] + "' AND QsoDate>" + oneMonthAgo + "00 AND QsoDate<" + thisMonth + "00"
			adif = qsoRowsAsAdif(contestQsosQuery,useDb)
			if "<EOR>" in adif:
				f = open("/var/www/html/logs/contests/" + oneMonthAgo + "-" + databaseNames[useDb].replace("/","_") + "-" + contestRow[0] + ".adi","w")
				f.write(adif)
				dirList.write(oneMonthAgo + "-" + databaseNames[useDb].replace("/","_") + "-" + contestRow[0] + ".adi\n")
				f.close()
			adif = ""
	db.close()
	data = None
	gc.collect()
dirList.close()
