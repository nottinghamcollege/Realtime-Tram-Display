import sys
import json
import colorama as colour
import requests
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('atco_code', help='A valid ATCO Code e.g. 9400ZZNOHIG2')
args = parser.parse_args()

if args.atco_code is None:
    sys.exit('Please provide an ATCO Code')

def print_info(text):
    print(colour.Fore.WHITE + text)
def print_tram(text):
    print(colour.Fore.YELLOW + '[-] ' + text)
def print_good(text):
    print(colour.Fore.GREEN + '[+] ' + text)
def print_bad(text):
    print(colour.Fore.RED + '[!] '  + text)

tram_data = requests.get('https://robinhood.arcticapi.com/network/stops/' + args.atco_code + '/visits').json()

if '_links' in tram_data:
    stop_data = tram_data['_links']['naptan:stop']
    stop_common_name = stop_data['commonName']
    direction_indicator = stop_data['indicator']
    
    print_info(stop_common_name  + ' ' + direction_indicator)
    print_info(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print(' ')

    if '_embedded' in tram_data:
        visits = tram_data['_embedded']['timetable:visit']
        for visit in visits:
             if visit['isRealTime']:
                     print_tram('Destination: ' + visit['destinationName'])
                     if visit['expectedArrivalTime'] == visit['aimedArrivalTime']:
                            print_good('On time!')
                     else:
                            print_bad('Running late!')

                     print_info('Expected time of arrival: ' + visit['displayTime'])
                     print(' ')
else:
    sys.exit('No stop data was returned, are you sure this is a valid ATCO Code?')
