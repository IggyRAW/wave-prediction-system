@echo off
REM 仮想環境を有効化
echo Activating virtual environment...
call .venv\Scripts\activate

IF ERRORLEVEL 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

REM Pythonスクリプトを実行
echo Running Python script...
python "main.py"

IF ERRORLEVEL 1 (
    echo Failed to run Python script
    pause
    exit /b 1
)

echo Done