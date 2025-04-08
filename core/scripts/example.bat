:: FlexQuery Execute Script
::
:: This script is used to execute a FlexQuery commands within virtual environment with FlexQuery package installed.
:: 
:: Command to execute: flexquery query --env PROD --write-csv
::   - This command will run a query in the PROD environment 
::   - User can select the query to run from the list of queries in the queries_library folder
::   - The results will be written to a CSV file in output folder

@echo off

setlocal enabledelayedexpansion

:: Check if we're already in a virtual environment
if defined VIRTUAL_ENV (
    echo Using active virtual environment: %VIRTUAL_ENV%
) else (
    :: Try to find and activate a virtual environment
    if exist ".venv\Scripts\activate.bat" (
        echo Activating virtual environment...
        call .venv\Scripts\activate.bat
    ) else if exist "venv\Scripts\activate.bat" (
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    ) else (
        echo No virtual environment found, add virtual environment and install FlexQuery package.
        echo.
    )
)

:: Execute flexquery with command
echo.
echo Running: flexquery run --env PROD --write-csv
echo.
flexquery run --env PROD --write-csv

:: Check for errors
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Command failed with error code: %ERRORLEVEL%
    echo.
)

:: Always pause at the end to see results
echo.
echo Press any key to exit...
pause > nul

endlocal
exit /b %ERRORLEVEL%