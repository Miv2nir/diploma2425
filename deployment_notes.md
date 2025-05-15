gunicorn setup - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu

run with gunicorn -c gunicorn_config.py  timesite.wsgi
if issues with deployment try run with gunicorn --bind 0.0.0.0:8000 timesite.wsgi