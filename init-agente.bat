@echo off
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Ambiente virtual nao encontrado. Crie-o e instale requirements.txt primeiro.
    pause
    exit /b 1
)

"venv\Scripts\python.exe" -m crawler.crawler
if errorlevel 1 (
    echo A automacao terminou com erro. Confira as mensagens acima.
    pause
)
