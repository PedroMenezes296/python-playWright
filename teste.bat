@echo off

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\playwright-profile-youtube" ^
  --profile-directory="Default"

timeout /t 3 >nul

python login2.py
