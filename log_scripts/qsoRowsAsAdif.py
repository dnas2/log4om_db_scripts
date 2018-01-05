import MySQLdb

def qsoRowsAsAdif(sqlQuery,useDb):
	# Parse columns
	fromPos = sqlQuery.lower().find(" from")
	columns = sqlQuery[0:fromPos]
	columns = columns.lower().replace("select ","")
	columns = columns.strip()
	columns = columns.replace(" ","")
	columnsAr = columns.split(",")
	columnsNum = len(columnsAr)
	# Do work
	adifStr = columns + "\n<USERDEF1:32:S>PLACEHASH\n<EOH>\n"
	db = MySQLdb.connect(host="[SERVER]", port=3306, user="[USER]", passwd="[PASSWORD]", db=useDb)
	if (db):
		print ("Connected to " + useDb)
	else:
		print ("Not connected")
		return None
	cursor = db.cursor()
	cursor.execute(sqlQuery)
	print ("Running query " + sqlQuery)
	data = cursor.fetchall()
	if data == None:
		return None
	for row in data:
    		for i in range(0,len(row)):
			adifFieldName = columnsAr[i].upper()
			adifFieldName = adifFieldName.replace("`","")
			if "MD5" in adifFieldName:
				adifFieldName = "PLACEHASH"
			if adifFieldName == "QSODATE": adifFieldName = "QSO_DATE"
			if adifFieldName == "TIMEON":  adifFieldName = "TIME_ON"
			if adifFieldName == "STATIONCALLSIGN": adifFieldName = "STATION_CALLSIGN"
			if adifFieldName == "MYSOTAREF": adifFieldName = "MY_SOTA_REF"
			if adifFieldName == "QSLSENTVIA": adifFieldName = "QSL_SENT_VIA"
			if adifFieldName == "MYGRIDSQUARE": adifFieldName = "MY_GRIDSQUARE"
			if adifFieldName == "MYIOTA": adifFieldName = "MY_IOTA"
			if adifFieldName == "RSTSENT": adifFieldName = "RST_SENT"
			if adifFieldName == "RSTRCVD": adifFieldName = "RST_RCVD"
			if adifFieldName == "STXSTRING": adifFieldName = "STX_STRING"
			if adifFieldName == "SRXSTRING": adifFieldName = "SRX_STRING"
			adifValue = row[i]
			if adifValue == '\x01': adifValue = "1"
			if adifValue == '\x00': adifValue = "0"
			if (len(adifValue) > 0):
				adifStr += "<" + adifFieldName + ":" + str(len(row[i])) + ">" + adifValue + " "
 		adifStr += "<EOR>\n"

	db.close()
	print adifStr
	return adifStr

