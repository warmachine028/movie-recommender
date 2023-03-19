#!/bin/sh
echo "Hello, Streamlit!"
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
mkdir -p ~/.streamlit

printf "[server]
port=%s
enableCORS=true
enableXsrfProtection=false
headless=true" "$PORT" >~/.streamlit/config.toml