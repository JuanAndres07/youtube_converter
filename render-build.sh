#!/usr/bim/env bash
# Script de build para render: instala ffmpeg y dependencias
set -e errexit

# Instala ffmpeg
apt-get update && apt-get install -y ffmpeg