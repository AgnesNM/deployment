web: gunicorn deployment_project.wsgi --bind 0.0.0.0:$PORT --log-file -
worker: celery -A deployment_project worker --loglevel=info
