@echo off

pushd %~dp0
set script_path=%CD%/main.py
popd

python script_path