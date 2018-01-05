import MySQLdb
import gc
from qsoRowsAsAdif import qsoRowsAsAdif
from datetime import date, timedelta

databaseNames = ["log4om_m0blf", "log4om_gm", "log4om_gw", "log4om_f", "log4om_tf", "log4om_fp"]
oneWeekAgoDate = date.today() - timedelta(7)
oneWeekAgo = oneWeekAgoDate.strftime('%Y%m%d')
searchSotaActivationsQuery = "SELECT QsoDate,MySotaRef FROM `log` WHERE MySotaRef!='' AND MySotaRef IS NOT NULL AND QsoDate>" + oneWeekAgo + " GROUP BY QsoDate,MySotaRef "
dirList = open("/var/www/html/logs/sota/sota.txt","a")
print searchSotaActivationsQuery
for useDb in databaseNames:
	db = MySQLdb.connect(host="[SERVER]", port=3306, user="[USER]", passwd="[PASSWORD]", db=useDb)
	cursor = db.cursor()
	cursor.execute(searchSotaActivationsQuery)
	data = cursor.fetchall()
	if data != None:
		for row in data:
    			qsoDate = row[0]
			sotaRef = row[1]
			sotaQsosQuery = "select StationCallsign,`Call`,QsoDate,TimeOn,Band,`Mode`,MySotaRef from log where QsoDate=" + qsoDate + " and MySotaRef='" + sotaRef + "' order by QsoDate,TimeOn;"
			f = open("/var/www/html/logs/sota/" + qsoDate + '-' + sotaRef.replace("/","_") + ".adi", 'w')
			adif = qsoRowsAsAdif(sotaQsosQuery,useDb)
			f.write(adif)
			dirList.write(qsoDate + "-" + sotaRef.replace("/","_") + ".adi\n")
			f.close()
	db.close()
	gc.collect()
dirList.close()
