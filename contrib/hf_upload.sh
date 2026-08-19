#!/usr/bin/env bash
# Upload one file to a Hugging Face dataset, retrying transient failures.
#
# Why this exists: `hf upload` of a multi-GB file fails intermittently inside
# the xet transfer layer — the observed failure is
#
#     RuntimeError: Internal error: timed out reading request body
#
# raised from huggingface_hub/_commit_api.py:_upload_xet_files. It is a
# transport timeout, not a rejected upload, and it killed a 26-minute sync
# job that had already pulled and decompressed everything. Retrying is the
# correct response; without it one flaky chunk discards the whole job.
#
# The last attempt disables xet entirely (HF_HUB_DISABLE_XET=1) so a
# persistent xet-side problem still completes over plain HTTP LFS rather
# than failing the run.
#
# Usage: hf_upload.sh <repo> <local-path> <remote-path> [extra hf args...]
set -euo pipefail

repo="$1"
local_path="$2"
remote_path="$3"
shift 3

attempts="${HF_UPLOAD_ATTEMPTS:-4}"
delay="${HF_UPLOAD_RETRY_DELAY:-30}"

if [[ ! -f "$local_path" ]]; then
  echo "hf_upload: no such file: $local_path" >&2
  exit 1
fi

size="$(du -h "$local_path" | cut -f1)"
for attempt in $(seq 1 "$attempts"); do
  # Final attempt: take xet out of the picture.
  if (( attempt == attempts )); then
    echo "hf_upload: final attempt for $remote_path with xet disabled"
    export HF_HUB_DISABLE_XET=1
  fi
  echo "hf_upload: $remote_path ($size) attempt $attempt/$attempts"
  if hf upload --quiet --repo-type dataset "$@" "$repo" "$local_path" "$remote_path"; then
    echo "hf_upload: $remote_path ok"
    exit 0
  fi
  if (( attempt < attempts )); then
    echo "hf_upload: attempt $attempt failed; sleeping ${delay}s" >&2
    sleep "$delay"
    delay=$(( delay * 2 ))
  fi
done

echo "::error::hf_upload: $remote_path failed after $attempts attempts" >&2
exit 1
