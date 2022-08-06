#!/bin/sh

mkdir -p ~/.streamlit

printf "[server]
port=%s
enableCORS=true
enableXsrfProtection=false
headless=true" "$PORT" >~/.streamlit/config.toml
