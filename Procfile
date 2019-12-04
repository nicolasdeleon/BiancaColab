release: python manage.py migrate
release: python manage.py makemigrations BarEvento
python manage.py migrate BarEvento
web: gunicorn backBone_Bianca.wsgi
