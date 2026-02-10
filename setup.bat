@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist "logs" mkdir "logs"

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i
set LOGFILE=logs\setup_!TS!.log

echo ================================================== > "%LOGFILE%"
echo SETUP iniciado em %date% %time% >> "%LOGFILE%"
echo Pasta do projeto: %cd% >> "%LOGFILE%"
echo ================================================== >> "%LOGFILE%"

echo [INFO] Verificando Python...
where python >> "%LOGFILE%" 2>&1
if errorlevel 1 (
  echo [ERRO] Python nao encontrado no PATH. Instale o Python e marque "Add Python to PATH". >> "%LOGFILE%"
  echo Python nao encontrado. Veja o log: %LOGFILE%
  pause
  exit /b 1
)

python --version >> "%LOGFILE%" 2>&1
pip --version >> "%LOGFILE%" 2>&1

echo [INFO] Criando ambiente virtual (.venv)...
if not exist ".venv" (
  python -m venv .venv >> "%LOGFILE%" 2>&1
  if errorlevel 1 (
    echo [ERRO] Falha ao criar venv. >> "%LOGFILE%"
    echo Falha ao criar venv. Veja o log: %LOGFILE%
    pause
    exit /b 1
  )
) else (
  echo [INFO] .venv ja existe, pulando criacao. >> "%LOGFILE%"
)

echo [INFO] Ativando venv...
call ".venv\Scripts\activate.bat" >> "%LOGFILE%" 2>&1

echo [INFO] Atualizando pip...
python -m pip install --upgrade pip >> "%LOGFILE%" 2>&1

if not exist "requirements.txt" (
  echo [ERRO] requirements.txt nao encontrado na pasta do projeto. >> "%LOGFILE%"
  echo requirements.txt nao encontrado. Veja o log: %LOGFILE%
  pause
  exit /b 1
)

echo [INFO] Instalando dependencias do requirements.txt...
pip install -r requirements.txt >> "%LOGFILE%" 2>&1
if errorlevel 1 (
  echo [ERRO] Falha ao instalar dependencias (pip). >> "%LOGFILE%"
  echo Falha ao instalar dependencias. Veja o log: %LOGFILE%
  pause
  exit /b 1
)

echo [INFO] Instalando browsers do Playwright...
python -m playwright install >> "%LOGFILE%" 2>&1
if errorlevel 1 (
  echo [ERRO] Falha ao instalar browsers do Playwright. >> "%LOGFILE%"
  echo Falha ao instalar Playwright browsers. Veja o log: %LOGFILE%
  pause
  exit /b 1
)

echo ================================================== >> "%LOGFILE%"
echo SETUP concluido com sucesso em %date% %time% >> "%LOGFILE%"
echo ================================================== >> "%LOGFILE%"

echo Setup concluido com sucesso.
echo Log: %LOGFILE%
pause
exit /b 0
