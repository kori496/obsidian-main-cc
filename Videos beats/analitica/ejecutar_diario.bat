@echo off
cd /d "%~dp0"
if not exist datos mkdir datos
echo ===== %date% %time% ===== >> datos\log.txt
python yt_stats.py --auto >> datos\log.txt 2>&1
python importar_tiktok.py >> datos\log.txt 2>&1

python importar_instagram.py >> datos\log.txt 2>&1
