@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

REM ====== AJUSTE AQUI SE PRECISAR ======
set CHROME_EXE=C:\Program Files\Google\Chrome\Application\chrome.exe
set USER_DATA_DIR=C:\playwright-profile-youtube
set PROFILE_DIR=Default
set CDP_PORT=9222
set PY_SCRIPT=login.py
REM =====================================

REM cria pasta de logs
if not exist "logs" mkdir "logs"

REM timestamp (YYYYMMDD_HHMMSS)
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i
set LOGFILE=logs\rodar_videos_youtube_!TS!.log

echo ================================================== > "%LOGFILE%"
echo RODAR iniciado em %date% %time% >> "%LOGFILE%"
echo Pasta do projeto: %cd% >> "%LOGFILE%"
echo ================================================== >> "%LOGFILE%"

REM valida chrome.exe
if not exist "%CHROME_EXE%" (
  echo [ERRO] Chrome.exe nao encontrado em: %CHROME_EXE% >> "%LOGFILE%"
  echo Chrome.exe nao encontrado. Ajuste CHROME_EXE. Log: %LOGFILE%
  pause
  exit /b 1
)

REM valida script python
if not exist "%PY_SCRIPT%" (
  echo [ERRO] Script Python nao encontrado: %PY_SCRIPT% >> "%LOGFILE%"
  echo Script nao encontrado. Log: %LOGFILE%
  pause
  exit /b 1
)

REM (opcional) finalizar Chrome para evitar lock do perfil
taskkill /F /IM chrome.exe >> "%LOGFILE%" 2>&1

echo [INFO] Abrindo Chrome com CDP na porta %CDP_PORT%... >> "%LOGFILE%"
start "" "%CHROME_EXE%" ^
  --remote-debugging-port=%CDP_PORT% ^
  --user-data-dir="%USER_DATA_DIR%" ^
  --profile-directory="%PROFILE_DIR%" >> "%LOGFILE%" 2>&1

echo [INFO] Aguardando Chrome subir... >> "%LOGFILE%"
timeout /t 3 >nul

echo [INFO] Rodando Python: %PY_SCRIPT% >> "%LOGFILE%"
python "%PY_SCRIPT%" >> "%LOGFILE%" 2>&1
set EXITCODE=%ERRORLEVEL%

echo [INFO] Codigo de saida: %EXITCODE% >> "%LOGFILE%"

if not "%EXITCODE%"=="0" (
  echo [ERRO] Execucao falhou. Veja o log: %LOGFILE%
  echo Falha. Log: %LOGFILE%
  pause
  exit /b %EXITCODE%
)

echo ================================================== >> "%LOGFILE%"
echo Concluido com sucesso em %date% %time% >> "%LOGFILE%"
echo Log: %LOGFILE% >> "%LOGFILE%"
echo ================================================== >> "%LOGFILE%"

echo OK. Log: %LOGFILE%
pause
exit /b 0
