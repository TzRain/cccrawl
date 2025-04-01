import os
import yaml
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import cv2
import numpy as np
from tqdm import tqdm

max_example_images = 32
max_example_tasks = -1

# Example Usage
base_directory = "/mnt/vground/plot/screenspotpro/output"
target_directory = "/workspace/repo/cccrawl/tmp/SPP_casestudy_0"

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def extract_text(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    bottom_crop = gray[int(height * 0.6):, :]
    text = pytesseract.image_to_string(bottom_crop)
    text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
    return text

def get_tasks_from_directory(base_dir):
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

def process_tasks(base_dir):
    results = {}
    tasks = get_tasks_from_directory(base_dir)

    tasks = tasks[:max_example_tasks]
    
    for task in tqdm(tasks):
        task_dir = os.path.join(base_dir, task)
        results[task] = []
        
        image_files = [f for f in os.listdir(task_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

        image_files = image_files[:max_example_images]

        os.makedirs(os.path.join(target_directory, task), exist_ok=True)

        for image_file in image_files:
            image_path = os.path.join(task_dir, image_file)
            # copy image to local directory
            local_image_path = os.path.join(target_directory, task, image_file)
            os.system(f"cp {image_path} {local_image_path}")
            try:
                text = extract_text(local_image_path)
            except Exception as e:
                text = f"Error processing {image_file}: {e}"

            # save text to loacl directory
            text_path = os.path.join(target_directory, task, f"{image_file}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)
            results[task].append({image_file: text})
    
    yaml_path = os.path.join(target_directory, "results.yaml")
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(results, f, allow_unicode=True, default_flow_style=False, width=float("inf"))
    
    return yaml_path

os.makedirs(target_directory, exist_ok=True)
yaml_output = process_tasks(base_directory)
print(f"OCR results saved to: {yaml_output}")
