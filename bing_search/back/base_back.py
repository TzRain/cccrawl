# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import os
from pprint import pprint
import requests

'''
This sample makes a call to the Bing Image Search API with a text query and returns relevant images with data.
Documentation: https: // docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/
'''

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
# subscriptionKey = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
subscriptionKey = "b2df87ded3c7412e959be43508e0cd2b"
print(subscriptionKey)
# endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/bing/v7.0/images/search"
# endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
endpoint = "https://api.bing.microsoft.com/v7.0/search"
print(endpoint)

# Query to search for
query = "office word screenshot"

# Construct a request
mkt = 'en-US'
params = {'q': query, 'mkt': mkt}
headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

# Call the API
try:
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    print("\nHeaders:\n")
    print(response.headers)

    print("\nJSON Response:\n")
    pprint(response.json())
except Exception as ex:
    raise ex