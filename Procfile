release: python manage.py syncdb
release: python manage.py makemigrations BarEvento
release: python manage.py migrate BarEvento
web: gunicorn backBone_Bianca.wsgi
