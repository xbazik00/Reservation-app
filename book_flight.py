#!/usr/bin/env python

'''
    Goal of this application is to find the shortest or the cheapest flight. This flight can
    be booked afterwards.
    :Author: Martin Bazik
    :Date: 14.2.2018
'''

import http.client
import argparse
import json
import datetime

def validate(date_text):
    """
        Validates the date
        :param date_text: string value of the date
        :return: datetime object
    """

    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def parse_args():
    """
        Parses parameters from command line
        :return: arguments
    """

    parser = argparse.ArgumentParser(description="""Input the correct arguments
        to find the flight you want to book.""")
    parser.add_argument('--date', required=True)
    parser.add_argument('--from', dest='fly_from', required=True)
    parser.add_argument('--to', required=True)

    # Argument group representing one-way or return
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--one-way', dest='return_days', action='store_const', const=None)
    group.add_argument('--return', dest='return_days', type=int)

    # Argument group representing cheapest or fastest route option
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--cheapest', dest='is_cheapest', action='store_true', default=True)
    group.add_argument('--fastest', dest='is_cheapest', action='store_false')

    # Amount of luggage
    parser.add_argument('--bags', type=int, default=0)

    return parser.parse_args()


def main():
    """
        Main function
    """

    args = parse_args()

    # Reservation request
    request = '/flights?v=3'

    # Validates and formats the date
    try:
        date = validate(args.date).strftime("%d/%m/%Y")
    except ValueError:
        print("0")
        exit(1)

    # Date
    request += "&dateFrom=" + date + "&dateTo=" + date

    # Starting and destination airport
    request += "&flyFrom=" + args.fly_from
    request += "&to=" + args.to

    # Time spent in destination
    if args.return_days:
        request += "&daysInDestinationFrom=" + str(args.return_days)
        request += "&daysInDestinationTo=" + str(args.return_days)

    # If the cheapest oprion was chosen
    if not args.is_cheapest:
        request += "&sort=duration"

    # Sends GET request
    conn = http.client.HTTPSConnection("api.skypicker.com")
    conn.request('GET', request)
    response = conn.getresponse()

    # Error response
    if response.status != 200:
        print("0")
        exit(1)

    data = response.read()
    data_arr = json.loads(data)

    # No data received
    if not data_arr['data']:
        print("0")
        exit(1)

    # Debug, to check the fastest and cheapest route
    #for i in data_arr['data']:
    #    print("Duration: %d; Price: %d" % (i["duration"]["total"], i["price"]))

    # Used currency
    payload = '{"currency": "EUR", '

    # Booking done by booking token
    payload += '"booking_token": "%s", ' % (data_arr['data'][0]['booking_token'])

    # Number of bags
    payload += '"bags":"%d", ' % (args.bags)

    # Passengers identity
    payload += '"passengers":[ { "lastName":"Janko", "firstName":"Mrkvicka", '
    payload += '"email":"janko.mrkvicka@test.com", "title":"Mr", "documentID":"EA123123", '
    payload += '"birthday":"1990-01-01" } ] }'

    # Content of the request is in json
    headers = {"Content-type": "application/json"}

    # POST request for booking the flight
    conn = http.client.HTTPConnection("128.199.48.38:8080")
    conn.request('POST', '/booking', payload, headers)
    response = conn.getresponse()

    # Error response
    if response.status != 200:
        print("0")
        exit(1)

    data = response.read()
    json_data = json.loads(data)

    # Invalid amount of luggage
    if 'bags' in json_data.keys():
        print("0")
        exit(1)

    if json_data['status'] == "confirmed":
        # Reservation number PNR
        print(json_data['pnr'])
    else:
        print("0")
        exit(1)


if __name__ == '__main__':
    main()
