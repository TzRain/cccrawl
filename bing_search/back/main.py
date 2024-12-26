# bing_image_search.py
import requests
from PIL import Image
from io import BytesIO
import os
from concurrent.futures import ThreadPoolExecutor
from config import BING_SEARCH_V7_SUBSCRIPTION_KEY, BING_SEARCH_V7_ENDPOINT

def search_images(query, count=10, offset=0, image_type='photo', size='medium', min_height=None, min_width=None):
    headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_V7_SUBSCRIPTION_KEY}
    params = {
        "q": query,
        "count": count,
        "offset": offset,
        "imageType": image_type,
        "size": size
    }
    if min_height:
        params['minHeight'] = min_height
    if min_width:
        params['minWidth'] = min_width

    response = requests.get(BING_SEARCH_V7_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def download_image(img, save_dir):
    img_url = img['contentUrl']
    img_format = img['encodingFormat']
    save_path = os.path.join(save_dir, f'image_{img["imageId"]}.{img_format}')
    response = requests.get(img_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    image.save(save_path)
    print(f'Downloaded {save_path}')

def main(query, count=10, save_dir='images', min_height=None, min_width=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    results = search_images(query, count, min_height=min_height, min_width=min_width)
    images = results['value']
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_image, img, save_dir) for img in images]
        for future in futures:
            future.result()

if __name__ == "__main__":
    query = "puppies"
    main(query, min_height=500, min_width=500)