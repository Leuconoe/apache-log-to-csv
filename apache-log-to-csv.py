#!/usr/bin/env python
# coding: utf-8

"""
Small tool to convert Apache log files to csv.
Written by Paul Biester (http://isonet.fr)
This package is © 2014 Paul Biester, released under the terms of the GNU GPL v3 (or at your option a later version)

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = "Paul Biester"
__copyright__ = "Copyright 2014, Paul Biester"
__credits__ = [""]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Paul Biester"
__email__ = "p.biester@isonet.fr"
__status__ = "Beta"

import csv
import apache_log_parser
import argparse

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
def main(**kwargs):
#def main():
    bcolors = Colors()
    #kwargs = {}
    #kwargs['format'] = "%a %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""
    #kwargs['input'] = 'apache.log'
    #kwargs['output'] = kwargs['input']+'.csv'
    print('Converting, please wait...')
    line_parser = apache_log_parser.make_parser(kwargs['format'])
    ######################
    #test = '100,200,100,200 - - [07/Sep/2021:06:25:07 +0000] "GET https://abcde.com HTTP/1.1" 403 498 "-" "Mozilla/5.0 Safari/537.36"'
    #line_parser = apache_log_parser.make_parser("%a %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"")
    #log_line_data = line_parser(test)
    #print(log_line_data)
    ######################
    header = True
    with open(kwargs['input'], 'rb') as inFile, open(kwargs['output'], 'w', newline='') as outFile:
        lines = inFile.readlines()
        writer = csv.writer(outFile)
        for line in lines:
            if line and len(line)>4:
                line = line.decode().replace('\n','')
                try:
                    log_line_data = line_parser(line)
                except apache_log_parser.LineDoesntMatchException as ex:
                    print(bcolors.FAIL + 'The format specified does not match the log file. Aborting...' + bcolors.ENDC)
                    print('Line: ' + ex.log_line + 'RegEx: ' + ex.regex)
                    return
                except TypeError as ex:
                    print(bcolors.FAIL + 'TypeError. Aborting...' + bcolors.ENDC)
                    print(line)
                    return
                
                if header:
                    writer.writerow(log_line_data.keys())
                    header = False     
                
                writer.writerow(log_line_data.values())                
                
    print(bcolors.OKGREEN + 'Conversion finished.' + bcolors.ENDC)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Apache logs to csv')
    parser.add_argument('format', type=str, help='Apache log format (see http://httpd.apache.org/docs/2.2/logs.html)')
    parser.add_argument('input', type=str, help='Input log file ex. /var/log/apache/access.log')
    parser.add_argument('output', type=str, help='Output csv file ex. ~/accesslog.csv')
    args = parser.parse_args()
    main(**vars(args))
