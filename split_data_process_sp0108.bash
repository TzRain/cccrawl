SCRIPT_FILE=${1:-"tests/getwebds_pf.py"}
NUM_PROCESS=${2:-4}
START_IDX=${3:-0}

# 存储每个后台进程的 PID
PIDS=()

START_IDX_LIST=(2 14 15 18 24 25 30 31 32 33 34 39 56 60 61 62 64 65 66 67 68 69 82 86 93 99 104 116 136 147 158 164 170 174 176 183 189 198 209 228)

# Run data process in different GPUs at the same time
for i in $(seq 0 $((NUM_PROCESS-1)))
do
    REAL_IDX=${START_IDX_LIST[$((i + START_IDX))]}
    python ${SCRIPT_FILE} --split_idx_list  ${REAL_IDX} $((REAL_IDX + 1)) ${EX_ARGS} &
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