#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )/.."
python -m uvicorn src.app.main:app --reload --env-file .env --log-config dev-logging.ini