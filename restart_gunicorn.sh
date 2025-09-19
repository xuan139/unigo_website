#!/bin/bash
# restart_gunicorn.sh
# 描述: 停止当前运行的 Gunicorn 并启动新的进程

APP_MODULE="app:app"
BIND_ADDR="0.0.0.0:5050"
WORKERS=4
ACCESS_LOG="gunicorn_access.log"
ERROR_LOG="gunicorn_error.log"

echo "Stopping existing Gunicorn processes..."
pkill -f gunicorn

echo "Starting Gunicorn..."
gunicorn -w $WORKERS -b $BIND_ADDR $APP_MODULE \
    --access-logfile $ACCESS_LOG \
    --error-logfile $ERROR_LOG -D

echo "Gunicorn restarted successfully."
