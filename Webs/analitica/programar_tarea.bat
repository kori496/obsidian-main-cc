@echo off
REM Crea (o reemplaza) la tarea diaria de Windows que ejecuta yt_stats.py.
REM Doble clic una sola vez. Si el PC esta apagado a la hora, corre al encenderlo.
set "TAREA=lagrim-stats YouTube"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$a=New-ScheduledTaskAction -Execute '%~dp0ejecutar_diario.bat' -WorkingDirectory '%~dp0'; $t=New-ScheduledTaskTrigger -Daily -At 12:00; $s=New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries; Register-ScheduledTask -TaskName '%TAREA%' -Action $a -Trigger $t -Settings $s -Force | Out-Null; Write-Host 'Tarea creada: todos los dias a las 12:00.'"
echo.
echo Para probarla ya:  schtasks /Run /TN "%TAREA%"
echo Para quitarla:     schtasks /Delete /TN "%TAREA%" /F
pause
