import argparse
from argparse import ArgumentParser
from datetime import datetime


def create_argparser():

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--advance-time", help="date is advanced by number of days", type=str)

    subparsers = parser.add_subparsers(dest='command')

    buy = subparsers.add_parser('buy', help="buy command includes product_name, price, and expiration_date for the product", description='subparser description')
    buy.add_argument('--product-name', type = str, required=True)
    buy.add_argument('--price', type=float, required=True)
    buy.add_argument("--expiration-date", type=lambda dt: datetime.strptime(dt, '%Y-%m-%d'), required=True)
    
    sell = subparsers.add_parser('sell', help="sell command includes product_name, price for the product", description='subparser description')
    sell.add_argument('--product-name',type = str, required=True)
    sell.add_argument('--price', type=float, required=True)

    report = subparsers.add_parser('report',help ="reports inventory details, revenue details and profit details for the", description='subparser description')
    report.add_argument('report-type', type=str, nargs='+')

    report.add_argument('--now', action='store_true')
    report.add_argument('--yesterday', action='store_true')

    report.add_argument('--today',action='store_true')
    report.add_argument('--date', type=lambda dt: datetime.strptime(dt, '%Y-%m'), nargs='?')
   
    return parser.parse_args()
