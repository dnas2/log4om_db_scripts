year_week_ago=$(date +"%Y" -d "3 weeks ago")
mnth_week_ago=$(date +"%m" -d "3 weeks ago")
date_week_ago=$(date +"%d" -d "3 weeks ago")
curl --data "fEmail=[CLUBLOG_EMAIL]&fPassword=[CLUBLOG_PASSWORD]&login=Login Now" --cookie-jar ./clublog https://secure.clublog.org/login.php
curl --cookie ./clublog --data "submit=Download QSL ADIF&call=FP/M0BLF&type=dxqsl&startyear=${year_week_ago}&startmonth=${mnth_week_ago}&startday=${date_week_ago}&endyear=0&endmonth=0&endday=0&adifmode=0" -i -o qslr/fp-m0blf.adi https://secure.clublog.org/getadif.php
curl --cookie ./clublog --data "submit=Download QSL ADIF&call=JW/M0BLF&type=dxqsl&startyear=${year_week_ago}&startmonth=${mnth_week_ago}&startday=${date_week_ago}&endyear=0&endmonth=0&endday=0&adifmode=0" -i -o qslr/jw-m0blf.adi https://secure.clublog.org/getadif.php
curl --cookie ./clublog --data "submit=Download QSL ADIF&call=TF/M0BLF&type=dxqsl&startyear=${year_week_ago}&startmonth=${mnth_week_ago}&startday=${date_week_ago}&endyear=0&endmonth=0&endday=0&adifmode=0" -i -o qslr/tf-m0blf.adi https://secure.clublog.org/getadif.php
curl --cookie ./clublog --data "submit=Download QSL ADIF&call=VP9/M0BLF&type=dxqsl&startyear=${year_week_ago}&startmonth=${mnth_week_ago}&startday=${date_week_ago}&endyear=0&endmonth=0&endday=0&adifmode=0" -i -o qslr/vp9-m0blf.adi https://secure.clublog.org/getadif.php

