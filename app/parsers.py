import argparse
from argparse import ArgumentParser
from datetime import datetime


def create_argparser():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--advance-time", help="Number of days in future", type=str)

    subparsers = parser.add_subparsers(dest='command')

    buy = subparsers.add_parser('buy')
    buy.add_argument('--product-name', help='Name of the product', type = str, required=True)
    buy.add_argument('--price', help="buying price of the product", type=float, required=True)
    buy.add_argument("--expiration-date", help="product expiry date in '%Y-%m-%d' format", type=lambda dt: datetime.strptime(dt, '%Y-%m-%d'), required=True)
    
    sell = subparsers.add_parser('sell')
    sell.add_argument('--product-name',help='Name of the product', required=True)
    sell.add_argument('--price', help="Selling price of the product", type=float, required=True)

    report = subparsers.add_parser('report')
    report.add_argument('report-type',help ="report type", type=str, nargs='+')

    report.add_argument('--now', help ="report till current time", action='store_true')
    report.add_argument('--yesterday',help ="report till yesterday", action='store_true')

    report.add_argument('--today',help ="report till today",action='store_true')
    report.add_argument('--date',help ="report till specified date", type=lambda dt: datetime.strptime(dt, '%Y-%m'), nargs='?')
   
    return parser.parse_args()
