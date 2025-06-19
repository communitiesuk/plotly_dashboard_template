setlocal enabledelayedexpansion

set ARG=%1

if NOT "%ARG%"=="auto" set ARG=manual

set CONDAPATH=D:\Python37
rem Replace "housing" with the name of the conda environment on the line below and remove rem:
rem set ENVPATH=D:\Users\%USERNAME%\.conda\envs\housing
rem Amend path to the directory of the local version of the azure repo in dashboard scripts:
rem cd /D "D:\Users\%USERNAME%\housing_azure\housing\"
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
call cds_to_prd_blob_azure.bat || echo "Upload to prd failed, continuing..."
echo "finished prd, moving on to dev"
rem Amend path to the directory of the local version of the azure repo in dashboard scripts:
rem cd /D "D:\Users\%USERNAME%\housing_azure\housing\"
call cds_to_dev_blob_azure.bat || echo "Upload to dev failed, continuing..."
echo "finished dev, moving on to tst"
rem Amend path to the directory of the local version of the azure repo in dashboard scripts:
rem cd /D "D:\Users\%USERNAME%\housing_azure\housing\"
call cds_to_tst_blob_azure.bat || echo "Upload to tst failed, continuing..."
echo "finished test"
endlocal
call conda.bat deactivate
exit