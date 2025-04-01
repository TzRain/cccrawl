import os, sys, json, time, datetime, requests


import pandas as pd

element_path = f'/mnt/vground/Adobe_Photoshop_2025/Adobe_Photoshop_2025_supp'

json_dir = f'{element_path}/meta'
json_file_list = os.listdir(json_dir)
json_file_list.sort()

print(f"Found {len(json_file_list)} files in {json_dir}")

merged_json_data = []
for json_file in json_file_list:
	print('prcessing', json_file)
	if not json_file.endswith('.json'):
		continue
	json_file_path = os.path.join(json_dir, json_file)
	with open(json_file_path, 'r') as f:
		json_data = json.load(f)
	print(json_file_path)
	merged_json_data.extend(json_data)
	
with open(f'{element_path}/meta.json', 'w') as f:
	json.dump(merged_json_data, f, ensure_ascii=False)

print (f"Saved {len(merged_json_data)} results to {element_path}/meta.json")

# convert to pd.DataFrame
df = pd.DataFrame(merged_json_data)
print(df.head())
print(df.columns)
print(df.dtypes)
print('len(df)', len(df))
df.to_csv(f'{element_path}/meta.csv', index=False)

print (f"Saved {len(merged_json_data)} results to {element_path}/meta.csv")