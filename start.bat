@echo off
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" 192.168.0.3:8000/

cmd /k "cd /d d:\MyDoc\PythonDjango\venv\Scripts & activate & cd /d d:\MyDoc\PythonDjango & python manage.py runserver 192.168.0.3:8000" 