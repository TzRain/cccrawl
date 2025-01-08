import sys, os
import time

if __name__ == "__main__":
    sys.path.append(os.getcwd())

import json
from PIL import Image
import pandas as pd
import requests
from io import BytesIO
from util import camel_to_snake, snake_to_camel, name_to_path

from bing_search.models import ScreenshotChecker

screenshot_checker = ScreenshotChecker()

headers_list = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1'
    },
    {

    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    },
]

def download_images(data_dict, save_base_folder, **kwargs):

    processed_url = set()

    os.makedirs(save_base_folder, exist_ok=True)

    """
    itemexmpale 
    {
        "name": "Microsoft 365 Word user interface on Windows 10 and on Mac - Windows 10",
        "thumbnailUrl": "https://tse2.mm.bing.net/th?id=OIP.ImcvAlMp43xiZsqaiO_3xgHaEN&pid=Api",
        "contentUrl": "http://www.geekstogo.com/forum/uploads/monthly_12_2020/post-277731-0-08325300-1607559747.png",
        "hostPageUrl": "http://www.geekstogo.com/forum/topic/375530-microsoft-365-word-user-interface-on-windows-10-and-on-mac/",
        "width": 1200,
        "height": 683
    }
    """
    new_data_dict = []
    print(f'load {len(data_dict)} images urls')

    processed_count = 0

    TIME_MARKER = time.time()

    skip_beacuse_of_error = 0
    skip_beacuse_of_duplicate = 0

    for item in data_dict:
        content_url = item['contentUrl']

        if content_url in processed_url:
            skip_beacuse_of_duplicate += 1
            continue

        processed_url.add(content_url)

        processed_count += 1

        flag = False
        error_list = []

        for headers in headers_list:
            try:
                response = requests.get(content_url, headers=headers, stream=True)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                score = screenshot_checker.predict(image) #
                image_name = content_url.split("/")[-1].split("?")[0] #
                save_path = os.path.join(save_base_folder, image_name) #

                post_fix = 1

                while os.exists(save_path):
                    image_name = image_name.split(".")[0] + f"_{post_fix}." + image_name.split(".")[1]
                    save_path = os.path.join(save_base_folder, image_name)
                    post_fix += 1

                image.convert("RGB").save(save_path)
                
                item.update({
                    "image_path": save_path,
                    'image_name': image_name,
                    "score": score
                })
                item.update(kwargs)

                new_data_dict.append(item)
                flag = True
                break
            
            except Exception as e:
                error_list.append(e)
        
        if not flag:
            print(f"Error downloading {content_url}, error list: {error_list}")
            skip_beacuse_of_error += 1
        
        if processed_count % 32 == 0:
            print(f"Processed {processed_count}/{len(data_dict)} images, time elapsed: {time.time() - TIME_MARKER} s")
            TIME_MARKER = time.time()
    
    print(f"Downloaded {len(new_data_dict)} images")
    print(f"Processed set with {processed_count} images")
    print(f"Skipped {skip_beacuse_of_error} images because of error")
    print(f"Skipped {skip_beacuse_of_duplicate} images because of duplicate")
        
    return new_data_dict


def run_download_images(meta_root, base_save_path, split_idx_list):
    results = []

    json_files = sorted([os.path.join(meta_root, json_file) for json_file in os.listdir(meta_root) if json_file.endswith('.json')])
    
    print (f"Downloading images from {split_idx_list[0]} to {split_idx_list[1]} from total {len(json_files)} files")

    json_files = json_files[split_idx_list[0]:split_idx_list[1]]
    
    for json_path in json_files:
        
        try:
            
            with open(json_path, 'r') as f:
                data_dict = json.load(f)

            json_file = os.path.basename(json_path)

            index_str = json_file.split('_')[1:4]
            index_str = '_'.join(index_str)

            cate, app, query = '_'.join(json_file.split('_')[4:]).split('.')[0].split('-')[:3]

            print(f'Processing index {index_str}, cate: {cate}, app: {app}, query: {query}')

            save_path = os.path.join(base_save_path, "image", f"{index_str}")
            result = download_images(data_dict, save_path, cate=cate, app=app, query=query)

            results.append(result)

        except Exception as e:
            print(f"Error processing {json_path}: {e}")
    
    # save
    save_path = os.path.join(base_save_path, f"meta_data_{split_idx_list[0]}to{split_idx_list[1]}.csv")
    df = pd.DataFrame(results)
    df.to_csv(save_path)

def parser_args():
    import argparse
    parser = argparse.ArgumentParser(description='Download images from Bing search API')
    parser.add_argument('--meta_root', type=str, default='/mnt/lmm/jialiang/data/webc/top50_q5_urls', help='Root folder of meta data')
    parser.add_argument('--base_save_path', type=str, default='/mnt/vground/bing_search_data/top50_q5_images', help='Base folder to save images')
    parser.add_argument('--split_idx_list',nargs=2, type=int, default=[0,1], help='List of start and end index of json files to download images')
    args = parser.parse_args()
    print(args)
    return args

if __name__ == "__main__":

    args = parser_args()

    run_download_images(
        meta_root=args.meta_root,
        base_save_path=args.base_save_path,
        split_idx_list=args.split_idx_list
    )