NUM_PROCESS=${1:-4}
START_IDX=${2:-0}

python bing_search/download.py --meta_root /mnt/lmm/jialiang/data/webc/top65_urls --base_save_path /mnt/vground/bing_search_data/top65 --split_idx_list $((START_IDX)) $((START_IDX + NUM_PROCESS))