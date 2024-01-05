#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )/.."
python -m uvicorn main:app --reload --env-file .env