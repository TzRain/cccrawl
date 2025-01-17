import os, sys

from tqdm import tqdm

target_cwd = os.getcwd()
sys.path.append(target_cwd)
sys.path.append(os.path.join(target_cwd, 'OmniParser'))

import base64
import io
import pandas as pd
from PIL import Image
from bing_search.models import OmniParserModel
import json
from bing_search.util import generativedatasets_get_dir, generativedatasets_path_to_info, bing_search_download_get_dir

def parser_args():
    import argparse
    parser = argparse.ArgumentParser(description='OmniParser')
    #data_root_type:
    parser.add_argument('--data_root_type', type=str, default='generativedatasets') # 'generativedatasets' or 'bing_search'
    parser.add_argument('--org_data_root', type=str, default='/mnt/vground/generativedatasets/generativedatasets/gold_en/collection=base/data/office/')
    parser.add_argument('--save_data_root', type=str, default='/mnt/vground/generativedatasets/generativedatasets_processed/gold_en/collection=base/data/office/')
    args = parser.parse_args()
    # script:
    # python bing_search/script/omni_parser.py --data_root_type bing_search --org_data_root /mnt/vground/bing_search_data/top50_q5_images/image --save_data_root /mnt/vground/bing_search_data/top50_q5_images/image_parsed

    # python bing_search/script/omni_parser.py --data_root_type bing_search --org_data_root /mnt/vground/bing_search_data/top50_q5_images/image --save_data_root /mnt/vground/bing_search_data/top50_q5_images/image_parsed

    return args

if __name__ == "__main__":

    args = parser_args()

    model = OmniParserModel()
    if args.data_root_type == 'generativedatasets':
        dirs, meta = generativedatasets_get_dir(args.org_data_root)
    elif args.data_root_type == 'bing_search':
        dirs = bing_search_download_get_dir(args.org_data_root)
    
    print(f'Found {len(dirs)} dirs')
    meta_data = []
    for dir_idx, dir in enumerate(dirs):
        image_paths = [os.path.join(dir, file_name) for file_name in os.listdir(dir) if file_name.endswith('.png')]
        
        print(f'Found {len(image_paths)} images in {dir}, {dir_idx}/{len(dirs)}')
        
        dir_info = generativedatasets_path_to_info(dir)
        app = dir_info['app']

        for image_path in tqdm(image_paths):
            try:
                
                results = model.process_image(image_path)
                dino_labled_img = results['dino_labled_img']
                parsed_content_list = results['parsed_content_list']
                w, h = results['image_size']
                image = Image.open(io.BytesIO(base64.b64decode(dino_labled_img)))
                image_save_path = image_path.replace(args.org_data_root, args.save_data_root).replace('.png', '_parsed.png')
                save_dir = os.path.dirname(image_save_path)
                os.makedirs(save_dir, exist_ok=True)
                image.save(image_save_path)
                def convert(parsed_content_list,image_path, app, w, h):
                    results = []
                    for item in parsed_content_list:
                        result = {
                            'img_filename': image_path.replace(args.org_data_root, ''),
                            'bbox': [
                                int(item['bbox'][0] * w),
                                int(item['bbox'][1] * h),
                                int(item['bbox'][2] * w),
                                int(item['bbox'][3] * h)
                            ],
                            'instruction': item['content'],
                            'data_app': app,
                            'data_source': item['type'],
                            'resolution': (w,h)
                        }
                        results.append(result)
                    return results
                results = convert(parsed_content_list, image_path, app, w, h)
                # save results to json
                json_save_path = image_save_path.replace('.png', '_parsed.json')
                with open(json_save_path, 'w') as f:
                    json.dump(results, f)
                meta_data.extend(results)

            except Exception as e:
                print(f'Error processing {image_path}: {e}')

    df = pd.DataFrame(meta_data)
    df.to_csv(os.path.join(args.save_data_root, 'metadata.csv'), index=False)
    
    print(f'Saved metadata to {os.path.join(args.save_data_root, "metadata.csv")}')
    print('Done!')
