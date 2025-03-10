@echo off
echo Setting up Django project...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
echo Setup completed!
