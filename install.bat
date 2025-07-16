@echo off
echo Installing TopV Adaptor Python dependencies...

echo.
echo Checking Python version...
python --version

echo.
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Installation completed!
echo.
echo To start the service:
echo   start.bat
echo.
echo To test the API:
echo   test-api.bat
echo.
pause 