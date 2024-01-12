#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )/.."
python -m uvicorn etabeta.main:app --reload --env-file .env --log-config dev-logging.ini