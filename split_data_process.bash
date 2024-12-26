SCRIPT_FILE=${1:-"tests/getwebds_pf.py"}
NUM_PROCESS=${2:-4}
START_IDX=${3:-0}

# 存储每个后台进程的 PID
PIDS=()

# Run data process in different GPUs at the same time
for i in $(seq 0 $((NUM_PROCESS-1)))
do
    python ${SCRIPT_FILE} --split_idx_list $((i + START_IDX)) $((i + START_IDX + 1)) ${EX_ARGS} &
    PIDS+=($!)  # 捕获后台进程的 PID 并存储在数组中
done

echo "To stop all processes, run the following command:"
echo "kill ${PIDS[@]}"

# 捕获终止信号并停止所有进程
trap "echo 'Stopping all processes'; for PID in ${PIDS[@]}; do kill $PID; done; exit" SIGINT SIGTERM

# 等待所有后台进程完成
for PID in "${PIDS[@]}"
do
    wait $PID
done

echo "All processes stopped."