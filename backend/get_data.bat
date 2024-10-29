@echo off
REM 文字コード設定
chcp 65001

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
python "get_wethar.py"

IF ERRORLEVEL 1 (
    echo Failed to run Python script
    pause
    exit /b 1
)

echo Done