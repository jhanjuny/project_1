@echo off
set msg=Auto commit %date% %time%
git add .
git commit -m "%msg%"
git push