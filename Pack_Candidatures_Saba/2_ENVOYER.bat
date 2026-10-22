@echo off
cd /d "%~dp0"
echo === ENVOI REEL - laisse cette fenetre ouverte (environ 2h40) ===
where py >nul 2>nul && (py envoyer_candidatures.py) || (python envoyer_candidatures.py)
pause
