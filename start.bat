@echo off
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" 127.0.0.1:8000/

cmd /k "cd /d d:\MyDoc\PythonDjango\venv\Scripts & activate & cd /d d:\MyDoc\PythonDjango & python manage.py runserver 127.0.0.1:8000" 