import MySQLdb
from qsoRowsAsAdif import qsoRowsAsAdif
from datetime import date, timedelta
import calendar

def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return date(year,month,day)

today = date(1997,10,1)
while (today<date(2017,12,26)):
	firstOfMonth = today.replace(day=1)
	lastMonth = firstOfMonth - timedelta(days=1)
	oneMonthAgo = lastMonth.strftime('%Y%m')
	thisMonth = firstOfMonth.strftime('%Y%m')
	qsosQuery = "SELECT StationCallsign,`Call`,Band,`Mode`,QsoDate,TimeOn,Contest,MyGridSquare,Myiota,MySotaRef FROM log WHERE QsoDate>" + oneMonthAgo + "00 AND QsoDate<" + thisMonth + "00 ORDER BY QsoDate,TimeOn,`Call`"
	adif = qsoRowsAsAdif(qsosQuery,"log4om_m0blf")
	if "<EOR>" in adif:
		f = open("/var/www/html/logs/m0blfbymonth/" + oneMonthAgo + ".adi","w")
		f.write(adif)
		f.close()
	today=add_months(today,1)


