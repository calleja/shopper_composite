wget -O stats.csv check-in-desk:8888/stats?format=csv\&start=2023-07-01

Per Andy Nelson: Yeah you could do that with a local daemon that fetches the daily logs

Python modules that allow for terminal commands:
'''
import subprocess as sp

process = sp.Popen(["your_cmd"]...)
process.wait() #Waits for command completion
'''

shopper_log table schema:
date: date (format ='YYYY-MM-DD')
ghfc: smallint
trial: smallint
psfc: smallint
cbfc: smallint
visitor: smallint

CREATE TABLE IF NOT EXISTS shopper_log
(date date UNIQUE KEY,
ghfc smallint,
trial smallint,
psfc smallint,
cbfc smallint,
visitor smallint);

first date of data from check-in desk:
2023-02-03,5,0,16,3,1

INSERT INTO shopper_log (date, ghfc, trial, psfc, cbfc, visitor) VALUES ('2023-02-03',5,0,16,3,1);