import MySQLdb
from qsoRowsAsAdif import qsoRowsAsAdif
from datetime import date, timedelta
databases= {"log4om_m0blf":"G","log4om_gw":"GW","log4om_gm":"GM","log4om_m4a":"G-M4A"}
placesByDxcc = {}
sortedByPlace = {}
today = date.today()
firstOfMonth = today.replace(day=1)
lastMonth = firstOfMonth - timedelta(days=1)
oneMonthAgo = lastMonth.strftime('%Y%m')
thisMonth = firstOfMonth.strftime('%Y%m')
qsosQuery = "SELECT StationCallsign,`Call`,QsoDate,TimeOn,Band,`Mode`, MD5(CONCAT_WS('-',StationCallsign,UPPER(MyGridSquare),Myiota)) AS PlaceHash FROM log WHERE QsoDate>" + oneMonthAgo + "00 AND QsoDate<" + thisMonth + "00"
for useDb in databases:
	adif = qsoRowsAsAdif(qsosQuery,useDb)
	adifSplit = adif.split("\n")
	for line in adifSplit:
		if "<EOR>" in line:
			placehashPos = line.find("PLACEHASH")
			if (placehashPos > 0):
				placehash = line[(placehashPos+13):(placehashPos+45)]
				if (placehash in sortedByPlace):
					sortedByPlace[placehash] += line + "\n"
				else:
					sortedByPlace[placehash] = line + "\n"
					placesByDxcc[placehash] = databases[useDb]
	line = ""
for place in sortedByPlace:
	print ("Got place " + place)
	f = open("/var/www/html/logs/forlotw/" +  oneMonthAgo + "-" + placesByDxcc[place] +  "-" + place + ".adi","w")
	f.write(sortedByPlace[place])
	f.close()



