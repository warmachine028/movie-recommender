#!/bin/bash

mkdir -p ~/.streamlit

printf "[server]
port = %s
enableCORS = false
headless = true" "$PORT" >~/.streamlit/config.toml
