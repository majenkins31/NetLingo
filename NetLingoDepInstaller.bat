@echo off && echo Installing dependencies... && if exist requirements.txt (python -m pip install -r requirements.txt) else (echo requirements.txt not found. Please make sure it is in the same directory as this script. && pause && exit /b 1) && echo All dependencies are installed. && pause