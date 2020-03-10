import sys
import json
import colorama as colour
import requests
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('atco_code', help='A valid ATCO Code e.g. 9400ZZNOHIG2')
parser.add_argument('limit', help='The amount of times to return e.g. 4', nargs='?', type=int, default=5)
args = parser.parse_args()

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
    stop_name = tram_data['_links']['naptan:stop']['commonName']
    indicator = tram_data['_links']['naptan:stop']['indicator']

    print_info(stop_name + ' ' + indicator)
    print_info(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print(' ')

    if '_embedded' in tram_data:
        visits = tram_data['_embedded']['timetable:visit']
        for visit in visits[:args.limit]:
            print_tram('Destination: ' + visit['destinationName'])
            
            if visit['isRealTime']:
                if visit['expectedArrivalTime'] == visit['aimedArrivalTime']:
                    print_good('On time!')
                else:
                    print_bad('Running late!')

            else:
                print_info('Note: Arrival time displayed is not in real time.')
                                
            print_info('Expected time of arrival: ' + visit['displayTime'])
            print(' ') 
else:
    sys.exit('No stop data was returned, are you sure this is a valid ATCO Code?')
