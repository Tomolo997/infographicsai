#!/bin/bash
cd /root/infographs/app
source /root/infographs/env/bin/activate
gunicorn app.wsgi:application --bind localhost:8000 --log-level debug