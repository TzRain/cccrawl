
# OMNI_PARSER FOR OFFICE
- follow the https://github.com/microsoft/OmniParser to prepare OmniParser and put it into ./OmniParser
- the weigth path selection show in `bing_search/models.py`
- running script :
```
    cd /workspace/repo/cccrawl
    FILE_ROOT=/workspace/tmp/Adobe_Photoshop_2025/Adobe_Photoshop_2025_supp
    python -m torch.distributed.launch --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=localhost --master_port=29500 bing_search/script/run_parser.py --data_root_type bing_search --org_data_root $FILE_ROOT --save_data_root $FILE_ROOT/image_parsed --metadata_path $FILE_ROOT/merged_data.csv
```