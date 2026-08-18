@echo off
cd /d "%~dp0"
if not exist cert.pem (
  echo cert.pem introuvable. Lis README.md - Option C.
  pause
  exit /b 1
)
if not exist key.pem (
  echo key.pem introuvable. Lis README.md - Option C.
  pause
  exit /b 1
)
python serve.py --https cert.pem key.pem
pause
