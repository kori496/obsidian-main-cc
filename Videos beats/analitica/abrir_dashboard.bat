@echo off
cd /d "%~dp0"
echo Panel en http://localhost:8080  (cierra esta ventana para detenerlo)
start "" cmd /c "timeout /t 2 >nul & start http://localhost:8080"
php -S localhost:8080 -t web
