import MySQLdb
import gc
from qsoRowsAsAdif import qsoRowsAsAdif
from datetime import date, timedelta

databaseNames = {"log4om_ct7":"CT7/M0BLF/P","log4om_ei":"EI/M0BLF/P","log4om_ej":"EJ/M0BLF","log4om_f":"F/M0BLF","log4om_fp":"FP/M0BLF","log4om_g6uw":"G6UW","log4om_g6uwtf":"G6UW/TF","log4om_g7wjf":"G7WJF","log4om_gh6uw":"GH6UW","log4om_gj6uw":"GJ6UW","log4om_gm":"MM0BLF/P","log4om_gm6uw":"GM6UW/P","log4om_gp6uw":"GP6UW/P","log4om_gu6uw":"GU6UW/P","log4om_gw":"MW0BLF/P","log4om_jw":"JW/M0BLF","log4om_m0blf":"M0BLF","log4om_m4a":"M4A","log4om_on":"ON/M0BLF","log4om_oy":"OY/M0BLF/P","log4om_tf":"TF/M0BLF","log4om_ve2":"VE2/M0BLF/P","log4om_vp9":"VP9/M0BLF","log4om_w1":"W1/M0BLF/P","log4om_w6":"W6/M0BLF"}
today = date.today()
firstOfMonth = today.replace(day=1)
lastMonth = firstOfMonth - timedelta(days=1)
oneMonthAgo = lastMonth.strftime('%Y%m')
searchQslSentQuery = "SELECT `Call` FROM `log` WHERE QslSDate>" + oneMonthAgo + "00 LIMIT 1" 
dirList = open("/var/www/html/logs/qslssentbymonth/qslssentbymonth.txt","a")
print searchQslSentQuery
for useDb in databaseNames:
	db = MySQLdb.connect(host="[SERVER]", port=3306, user="[USER]", passwd="[PASSWORD]", db=useDb)
	cursor = db.cursor()
	cursor.execute(searchQslSentQuery)
	data = cursor.fetchall()
	if data != None:
		sentQslsQuery = "SELECT StationCallsign, QsoDate, `Call`, Band, `Mode`, QslSentVia, QslSDate FROM log WHERE QslSDate>" + oneMonthAgo + "00"
		adif = qsoRowsAsAdif(sentQslsQuery,useDb)
		if "<EOR>" in adif:
			f = open("/var/www/html/logs/qslssentbymonth/" + oneMonthAgo + "-" + databaseNames[useDb].replace("/","_") + ".adi","w")
			f.write(adif)
			dirList.write(oneMonthAgo + "-" + databaseNames[useDb].replace("/","_") + ".adi\n")
			f.close()
		adif = ""
	db.close()
	data = None
	gc.collect()
dirList.close()
