# python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root /mnt/vground/bing_search_data/others0/image --save_data_root /mnt/vground/bing_search_data/others0/image_parsed --metadata_path /mnt/vground/bing_search_data/others0/meta.csv


# python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root /workspace/repo/cccrawl/tmp/360zip --save_data_root /workspace/repo/cccrawl/tmp/360zip/image_parsed --metadata_path /workspace/repo/cccrawl/tmp/360zip/merged_data.csv



# FILE_ROOT=/workspace/repo/cccrawl/tmp/Clipchamp

# python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root $FILE_ROOT --save_data_root $FILE_ROOT/image_parsed --metadata_path $FILE_ROOT/merged_data.csv



# FILE_ROOT=/workspace/tmp/Adobe_Photoshop_2025/Adobe_Photoshop_2025_basic

# python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root $FILE_ROOT --save_data_root $FILE_ROOT/image_parsed --metadata_path $FILE_ROOT/merged_data.csv


# FILE_ROOT=/workspace/tmp/Adobe_Photoshop_2025/Adobe_Photoshop_2025_variance

# python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root $FILE_ROOT --save_data_root $FILE_ROOT/image_parsed --metadata_path $FILE_ROOT/merged_data.csv


# FILE_ROOT=/workspace/tmp/Adobe_Photoshop_2025/Adobe_Photoshop_2025_floating

# python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root $FILE_ROOT --save_data_root $FILE_ROOT/image_parsed --metadata_path $FILE_ROOT/merged_data.csv

# FILE_ROOT=/workspace/tmp/Adobe_Photoshop_2025_full

# python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root $FILE_ROOT --save_data_root $FILE_ROOT/image_parsed --metadata_path $FILE_ROOT/merged_data.csv


# FILE_ROOT=/mnt/vground/Adobe_Photoshop_2025/Adobe_Photoshop_2025_supp


# python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root $FILE_ROOT --save_data_root $FILE_ROOT/image_parsed --metadata_path $FILE_ROOT/merged_data.csv

FILE_ROOT=/workspace/tmp//Adobe_Photoshop_2025/Adobe_Photoshop_2025_supp

python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root $FILE_ROOT --save_data_root $FILE_ROOT/image_parsed --metadata_path $FILE_ROOT/merged_data.csv