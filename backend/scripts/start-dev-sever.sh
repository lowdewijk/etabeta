#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )/.."
ETABETA_LOG_TYPE=dev python -m uvicorn etabeta.main:app --reload --env-file .env