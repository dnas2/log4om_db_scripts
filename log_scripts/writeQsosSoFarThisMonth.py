import MySQLdb
from qsoRowsAsAdif import qsoRowsAsAdif
from datetime import date, timedelta

today = date.today()
thisMonth = today.strftime('%Y%m')
qsosQuery = "SELECT StationCallsign,`Call`,Band,`Mode`,QsoDate,TimeOn,Contest,MyGridSquare,Myiota,MySotaRef FROM log WHERE QsoDate>" + thisMonth + "00 ORDER BY QsoDate,TimeOn,`Call`"
adif = qsoRowsAsAdif(qsosQuery,"log4om_m0blf")
if "<EOR>" in adif:
	f = open("/var/www/html/logs/m0blfbymonth/" + thisMonth + ".adi","w")
	f.write(adif)
	f.close()



