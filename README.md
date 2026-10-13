wget -O stats.csv check-in-desk:8888/stats?format=csv\&start=2023-07-01

Per Andy Nelson: Yeah you could do that with a local daemon that fetches the daily logs

Python modules that allow for terminal commands:
'''
import subprocess as sp

process = sp.Popen(["your_cmd"]...)
process.wait() #Waits for command completion
'''