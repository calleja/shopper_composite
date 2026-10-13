You are a python and data pipeline expert. 


## Objective
Surface and store shopper visits data. Once stored, this dataset will be surfaced on Apache Superset. The source of the data are log files retrievable via `wget` stored on a connected virtual private cloud network DigitalOcean droplet ("plum"). 
The solution must be memory light: the available processing and storage resource (a digitalOcean droplet) is of size 2 vCPUs / 4 GB RAM / 50 GB Disk.

Schedule a daily automatic ingest of data.

Establish a simple logging feature using the 'logging' library of python. 

## Deliverable
Propose a project structure, stack, and workflow that is scheduled to run on a daily basis. 

Include testing with pytest: test 'membership_ard' database connection

## Technology Infrastructure
DigitalOcean droplet: a Virtual private cloud network containing two droplets: 'radish' (processing and storage) and 'plum' (source).
MySQL server: this is already running on the 'radish' digitalocean server. The ingested data will land in a pre-existing database called "membership_ard".

## Logger properties
The logging handler routes the logs to a file (specified by absolute path) on a directory on the droplet. Log level set at "WARN".

## ETL process
To be handled in python.
Proposed:
  1. Obtain the latest date available on the table in membership_ard (this will serve as the "date" argument to the `wget` command
  2. Execute the `wget` download with the appropriate arguments

Data format of the csv report produced by the http/ftp service on 'plum': 
date str
ghfc integer
trial integer
psfc integer
cbfc integer
visitor integer

  3. transform the data as necessary 

  'date' needs to be loaded as a date field in mysql. No other transforming needs to be performed.
ex. csv output file: 
date,ghfc,trial,psfc,cbfc,visitor
2023-02-01,0,0,0,0,0
2023-02-02,0,0,0,0,0
2023-02-03,5,0,16,3,1

  4. Load the data into the membership_ard database table

## Considerations
  - Scheduling options: daemon, shell script, python 'subprocess' library
  - myql database residing in 'radish' server 
  - dashboard service: This data will be surfaced on Apache Superset - a dashboard service hosted on a web server also in 'radish'
  - Extremely limited RAM on the server
  - data ingest: The data ingest is very light with just one record of 6 columns logged each day in the 'plum' server
  - Dashboard demand (users and concurrent sessions) are extremely light: just one or two users log in per day, and never more than three concurrent users.
  - preference for python 'uv' package. Modularize the functions and operations of the workflow.
  - database credentials: a "secrets" file will be stored and available on a directory in 'radish'

## Database details
  - write mode for Mysql injection: append
  - MySQL connection: the full workflow will involve two actions
    1. query the date for the latest record (sorting by date)
    2. append the newest downloaded data to the table
All database connections must be closed properly - preferably with 'with' resource handling
Consider leaving the database connection open until both database operations finish (close early if there is an error that will prevent the second operation)

## Helpful commands
Command to fetch the report from the data source (connected VPC network droplet)
`wget -O stats.csv check-in-desk:8888/stats?format=csv\&start=2023-07-01`

parameters
  - format: keep csv for now (I'm not aware of other options)
  - start: date that marks the first date queried of the report; assume the report will return all logs (in the form of a csv) from that date to the last available date (can assume it will be as of prior day from run date)

## Resources
logging to physical files in python's logger library:
https://signoz.io/guides/python-logging-create-log-if-not-exists-or-open-and-continue-logging-if-it-does/
python 'subprocess' library: https://www.digitalocean.com/community/tutorials/python-system-command-os-subprocess-call

