
import requests
from util import camel_to_snake, snake_to_camel
from dataclasses import dataclass
import urllib.parse
import os, json
from config import BING_SEARCH_V7_ENDPOINT, BING_SEARCH_V7_SUBSCRIPTION_KEY, NEEDED_KEYS

from app_list import QUERY_LIST

# Define a dataclass to encapsulate the query parameters for Bing Image Search API
@dataclass
class BingImageSearchParams:
    
    q: str = None            # Search query term, this is a required field
    offset: int = 0          # Pagination offset, indicates from which result to start
    count: int = 35          # Number of results to return per page, default is 35
    
    # Basic parameters
    cc: str = None           # Country/Region code, e.g., 'US' for United States
    id: str = None           # Image ID to ensure a specific image appears first in the results
    mkt: str = None          # Market (region), e.g., 'en-US' for US market
    safeSearch: str = None  # SafeSearch level, options are 'Off', 'Moderate', 'Strict'
    setLang: str = None      # Language of the results, e.g., 'en' for English

    # Advanced parameters
    aspect: str = None             # Filter by aspect ratio: 'Square', 'Wide', 'Tall', or 'All'
    color: str = None              # Filter by color: 'ColorOnly', 'Monochrome'
    freshness: str = None          # Filter by freshness: 'Day', 'Week', 'Month'
    height: int = None             # Filter by height (in pixels)
    imageContent: str = None       # Filter by content type: 'Face', 'Portrait'
    imageType: str = None          # Filter by image type: 'AnimatedGif', 'Clipart', 'Photo', etc.
    license: str = None            # Filter by license type: 'Any', 'Public', 'Share', 'Modify', etc.
    maxFileSize: int = None        # Filter by max file size (in bytes)
    maxHeight: int = None          # Filter by max height (in pixels)
    maxWidth: int = None           # Filter by max width (in pixels)
    minFileSize: int = None        # Filter by min file size (in bytes)
    minHeight: int = None          # Filter by min height (in pixels)
    minWidth: int = None           # Filter by min width (in pixels)
    size: str = None               # Filter by size: 'Small', 'Medium', 'Large', 'Wallpaper', or 'All'
    width: int = None              # Filter by width (in pixels)

    def to_query_string(self):
        params = {key: value for key, value in self.__dict__.items() if value is not None}
        return urllib.parse.urlencode(params)

    @property
    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


@dataclass
class BingImageSearchHeaders:
    Accept: str = None # Default media type, specify "application/ld+json" for JSON-LD
    Accept_Language: str = None       # Comma-delimited list of languages, e.g., 'en-US,en;q=0.9'
    Content_Type: str = None          # Optional, specify the request content type (e.g., 'application/json')
    Ocp_Apim_Subscription_Key: str = None  # Required: Subscription key from Azure Portal
    Pragma: str = None                # Optional: 'no-cache' to prevent cached content
    User_Agent: str = None            # Optional: User agent string for client device (browser type)
    X_MSEdge_ClientID: str = None     # Optional: Client ID for consistent user experience across requests
    X_MSEdge_ClientIP: str = None     # Optional: Client IP address (for location-based results)
    X_Search_Location: str = None     # Optional: User's location info for local content, e.g., 'lat:47.6097;long:-122.3331;re:22'

    def to_headers(self):
        assert self.Ocp_Apim_Subscription_Key is not None, "Subscription key is required"
        # Filter out None values and create a dictionary of headers
        headers = {key.replace('_', '-'): value for key, value in self.__dict__.items() if value is not None}
        return headers

    @property
    def to_dict(self):
        return {key.replace('_', '-'): value for key, value in self.__dict__.items() if value is not None}

def search_images(
        query,
        count=64,
        offset=0,
        headers: BingImageSearchHeaders=None,
        params: BingImageSearchParams=None
    ):

    if headers is None:
        headers = BingImageSearchHeaders(Ocp_Apim_Subscription_Key=BING_SEARCH_V7_SUBSCRIPTION_KEY)
    if params is None:
        params = BingImageSearchParams(q=query, count=count, offset=offset)
    
    params.q = query
    if params.count is None: params.count = count
    if params.offset is None: params.offset = offset

    headers_dict = headers.to_dict
    params_dict = params.to_dict
    
    try:
        response = requests.get(BING_SEARCH_V7_ENDPOINT, headers=headers_dict, params=params_dict)
        response.raise_for_status()

        response = response.json()
        results = response['value']
        filter_results = [{k:v for k,v in result.items() if k in NEEDED_KEYS} for result in results]
    except Exception as ex:
        print(ex)
        filter_results = []

    return filter_results

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Bing Image Search API")
    parser.add_argument("--count", type=int, help="Number of results to return per query", default=2048)
    parser.add_argument("--batch", type=int, help="Number of results per batch", default=32)
    parser.add_argument("--save_dir", type=str, help="Path to save the results", default="webc/urls")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    
    args = parse_args()

    exampe_query_list = QUERY_LIST

    header = BingImageSearchHeaders(
        Ocp_Apim_Subscription_Key=BING_SEARCH_V7_SUBSCRIPTION_KEY
    )

    params = BingImageSearchParams(
        license="All",
        maxFileSize=520192,  # 520,192 bytes
        minHeight=200,
        minWidth=200,
    )

    print(f'expect {args.count} results for each query')
    
    for query in exampe_query_list:
        file_name = f'url_{query.index}_{query}.json'
        
        results = []
        for i in range(0, args.count, args.batch):
            result = search_images(query=query.query,count=args.batch,offset=i,headers=header,params=params)
            results.extend(result)
        
        # Save the results to a file
        with open(os.path.join(args.save_dir, file_name), 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Saved {len(results)} results to {file_name}")

    print(results)

    