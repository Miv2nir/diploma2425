gunicorn setup - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu

run with gunicorn -c gunicorn_config.py  timesite.wsgi
if issues with deployment try run with gunicorn --bind 0.0.0.0:8000 timesite.wsgi

Note: if the npm run dev command fails try the following:
sudo sysctl fs.inotify.max_user_watches=524288
sudo sysctl -p