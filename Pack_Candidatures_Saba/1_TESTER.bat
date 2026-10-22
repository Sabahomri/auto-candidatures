@echo off
cd /d "%~dp0"
echo === TEST : aucun mail ne sera envoye ===
where py >nul 2>nul && (py envoyer_candidatures.py --test) || (python envoyer_candidatures.py --test)
pause
