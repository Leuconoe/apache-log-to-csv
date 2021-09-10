# apache-log-to-csv

## Small tool to convert Apache log files to csv.

I'm using [apache-log-parser](https://github.com/rory/apache-log-parser), you may need to install it.

Tested with Python 2.7.6

## Usage

	apache-log-to-csv.py [-h] [-v] format input output
	
- Format: [Apache log format](http://httpd.apache.org/docs/2.2/logs.html). Example: ```%a %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"```
- Input: Path to the Apache log file. Example: ```/var/log/apache/access.log``` 
- Output: Desired output path for the csv file. Example: ```~/access.csv``` 
