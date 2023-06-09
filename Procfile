release: pip install flit==3.8.0
web: flit install --deps=production; python3 src/onetime/entrypoints/web/manage.py collectstatic; cd src/onetime/entrypoints/web/; gunicorn --reload app.wsgi