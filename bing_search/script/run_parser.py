import os, sys
import torch
import torch.distributed as dist
from torch.utils.data import Dataset, DataLoader
from torch.nn.parallel import DistributedDataParallel as DDP

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
    parser.add_argument('--data_root_type', type=str, default='generativedatasets') # 'generativedatasets' or 'bing_search'
    parser.add_argument('--org_data_root', type=str, default='/mnt/vground/generativedatasets/generativedatasets/gold_en/collection=base/data/office/')
    parser.add_argument('--save_data_root', type=str, default='/mnt/vground/generativedatasets/generativedatasets_processed/gold_en/collection=base/data/office/')
    parser.add_argument('--metadata_path', type=str, default='/mnt/vground/bing_search_data/top65/meta.csv')
    parser.add_argument('--local-rank', type=int, default=0)  # Add this line
    args = parser.parse_args()
    return args

class ImageDataset(Dataset):
    def __init__(self, metadata_path):
        self.metadata = pd.read_csv(metadata_path)
        assert 'image_path' in self.metadata.columns
        assert 'app' in self.metadata.columns

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        return dict(self.metadata.iloc[idx])

def process_image(model, image_path, org_data_root, save_data_root, app):
    with torch.no_grad():
        try:
            results = model.process_image(image_path)
            dino_labled_img = results['dino_labled_img']
            parsed_content_list = results['parsed_content_list']
            w, h = results['image_size']
            image = Image.open(io.BytesIO(base64.b64decode(dino_labled_img)))
            # add 'parsed' before the file extension
            image_save_path = image_path.replace(org_data_root, save_data_root)
            image_save_path = '.'.join(image_save_path.split('.')[:-1]) + '_parsed.' + image_save_path.split('.')[-1]
            save_dir = os.path.dirname(image_save_path)
            os.makedirs(save_dir, exist_ok=True)
            image.save(image_save_path)
            def convert(parsed_content_list, image_path, app, w, h):
                results = []
                for item in parsed_content_list:
                    result = {
                        'img_filename': image_path.replace(org_data_root, ''),
                        'bbox': [
                            int(item['bbox'][0] * w),
                            int(item['bbox'][1] * h),
                            int(item['bbox'][2] * w),
                            int(item['bbox'][3] * h)
                        ],
                        'instruction': item['content'],
                        'data_app': app,
                        'data_source': item['type'],
                        'resolution': (w, h)
                    }
                    results.append(result)
                return results
            results = convert(parsed_content_list, image_path, app, w, h)
            # Save the parsed results to a json file by replacing the file extension with '_parsed.json'
            json_save_path = '.'.join(image_save_path.split('.')[:-1]) + '_parsed.json'
            with open(json_save_path, 'w') as f:
                json.dump(results, f)
            return results
        except Exception as e:
            print(f'Error processing {image_path}: {e}')
            return []

def main():
    args = parser_args()
    print(args)

    dist.init_process_group(backend='nccl')
    local_rank = args.local_rank
    torch.cuda.set_device(local_rank)
    device = torch.device('cuda', local_rank)

    model = OmniParserModel()
    model.to(device)

    # Check if the model has parameters requiring gradients
    if any(p.requires_grad for p in model.parameters()):
        model = DDP(model, device_ids=[local_rank])

    dataset = ImageDataset(args.metadata_path)
    sampler = torch.utils.data.distributed.DistributedSampler(dataset)
    dataloader = DataLoader(dataset, batch_size=1, sampler=sampler)

    print(f'Found {len(dataloader)} images')
    print(f'Processing images...{len(dataloader)}')
    meta_data = []

    for image_meta in tqdm(dataloader):
        app = image_meta['app'][0] # batch size fixed to 1
        image_path = image_meta['image_path'][0]
        
        if not os.path.isabs(image_path):
            image_path = os.path.join(args.org_data_root, image_path)

        results = process_image(model, image_path, args.org_data_root, args.save_data_root, app)
        meta_data.extend(results)

    # Gather meta_data from all processes
    all_meta_data = [None for _ in range(dist.get_world_size())]
    dist.all_gather_object(all_meta_data, meta_data)

    # Flatten the list of lists
    meta_data = [item for sublist in all_meta_data for item in sublist]

    # Save metadata to json
    if local_rank == 0:
        with open(os.path.join(args.save_data_root, 'parsed_results.json'), 'w') as f:
            json.dump(meta_data, f)

        df = pd.DataFrame(meta_data)
        df.to_csv(os.path.join(args.save_data_root, 'parsed_results.csv'), index=False)
        print(f'len(meta_data): {len(meta_data)}')
        print(f'Saved metadata to {os.path.join(args.save_data_root, "parsed_results.csv")}')
        print('Done!')

if __name__ == "__main__":
    main()
