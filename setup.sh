#!/bin/sh

mkdir -p ~/.streamlit

printf "[server]
port = %s
enableCORS = false
enableXsrfProtection=false
headless = true" "$PORT" >~/.streamlit/config.toml
