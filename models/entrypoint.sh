#!/bin/bash
set -e

# Activate conda environment
source /opt/miniconda/etc/profile.d/conda.sh
conda activate vllm
pip install vllm==0.9.0.1 --extra-index-url https://download.pytorch.org/whl/cu128
pip install flashinfer-python
#pip install flash-attn

# Jalankan vLLM dengan API key dari environment
exec vllm serve "${MODEL_NAME}" \
  --dtype "${DATA_TYPE}" \
  --api-key "${VLLM_API_KEY}" \
  --limit-mm-per-prompt "${LIMIT_PER_PROMPT}" \
  --port "${PORT}" \
  --disable-log-stats \
  --gpu-memory-utilization "${MEMORY_UTILIZATION}"
  #--tool-call-parser "${TOOL_CALL_PARSER}" \
  #--enable-auto-tool-choice \
  #--swap-space "${SWAP_SPACE}" \
  #--quantization "${QUANTIZATION}" \
  #--gpu-memory-utilization "${MEMORY_UTILIZATION}" \
 