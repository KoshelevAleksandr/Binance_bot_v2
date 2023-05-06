@echo off

call %~dp0bot\venv\Scripts\activate

python %~dp0bot\binance_bot.py

pause