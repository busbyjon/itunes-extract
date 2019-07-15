#!/usr/bin/env python

import xml.etree.ElementTree as ET
import csv
import re
import json
import pandas as pd

from mitmproxy import ctx


class iTunesProcess:


    def __init__(self):
        print("Started")
        self.all_purchases = []



    def response(self, flow):
        if '/commerce/account/purchases' in flow.request.path:
            print("Found a record")
            try:
                # try to parse and extract, ignore on error
                print("Got a record")
                content = flow.response.content
                content_parsed = json.loads(content)
                try:
                    self.all_purchases.append(content_parsed['data']['attributes']['purchases'])
                except Exception as e:
                    print('Failed: ', str(e))
                print(content_parsed['data']['attributes']['purchases'])
            except:
                pass

    def done(self):
        print("Done")
        items = []
        invoices = []
        #print(self.all_purchases)
        for purchase_group in self.all_purchases:
            for purchase in purchase_group:
                invoices.append({'id': purchase['id'], 'date':purchase['invoice-date'], 'total':purchase['total']})
                for item in purchase['items']:
                    items.append({'invoice-id': purchase['id'], 'item-type': item['kind'], 'artist-name':item['artist-name'], 'item-name':item['item-name']})

        #print(invoices)
        #print(items)

        try:
            invoices_df = pd.DataFrame.from_dict(invoices)
            invoices_df.to_csv("invoices.csv")

            items_df = pd.DataFrame.from_dict(items)
            items_df.to_csv('items.csv')
        except Exception as e:
            print('Failed: ', str(e))


addons = [
    iTunesProcess()
]