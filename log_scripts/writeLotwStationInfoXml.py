import MySQLdb
import gc
databases = {"log4om_m0blf":"G","log4om_gw":"GW","log4om_gm":"GM","log4om_m4a":"G:M4A"}
outputXml = "<StationDataFile>\n"
sqlQuery = "SELECT DISTINCT(MD5(CONCAT_WS('-',StationCallsign,UPPER(MyGridSquare),Myiota))) AS PlaceHash,StationCallsign,UPPER(MyGridSquare),Myiota From `log` WHERE StationCallsign != '' AND MyGridSquare != '' GROUP BY StationCallsign,MyGridSquare,Myiota"
for database in databases:
	db = MySQLdb.connect(host="[SERVER]", port=3306, user="[USER]", passwd="[PASSWORD]", db=database)
	if (db):
		print ("Connected to " + database)	
		cursor = db.cursor()
		cursor.execute(sqlQuery)
		print ("Running query " + sqlQuery)
		data = cursor.fetchall()
		if data != None:
			for row in data:
				outputXml += "  <StationData name=\"" + row[0] + "\">\n"
				outputXml += "    <CALL>" + row[1] + "</CALL>\n"
				outputXml += "    <GRIDSQUARE>" + row[2] + "</GRIDSQUARE>\n"
				if (len(row[3])>0):
					outputXml += "    <IOTA>" + row[3] + "</IOTA>\n"
				if (databases[database] == "G"):
					outputXml += "    <CQZ>14</CQZ>\n    <ITUZ>27</ITUZ>\n    <DXCC>223</DXCC>\n"
				if (databases[database] == "G:M4A"):
					outputXml += "    <CQZ>14</CQZ>\n    <ITUZ>27</ITUZ>\n    <DXCC>223</DXCC>"
				if (databases[database] == "GW"):
					outputXml += "    <CQZ>14</CQZ>\n    <ITUZ>27</ITUZ>\n    <DXCC>294</DXCC>\n"
				if (databases[database] == "GM"):
					outputXml += "    <CQZ>14</CQZ>\n    <ITUZ>27</ITUZ>\n    <DXCC>279</DXCC>\n"
				outputXml += "  </StationData>\n"
		db.close()
	gc.collect()
outputXml += "</StationDataFile>"
f = open("/var/www/html/logs/forlotw/station_data","w")
f.write(outputXml)
f.close()
print ("Written file")
