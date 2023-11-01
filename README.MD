1. Install deps:

```
pip install -r requirements.txt
```

2. Run broker:

```
docker run -d -p 5672:5672 rabbitmq
```

3. Run beat process.

```
celery -A celery_periodic_tasks beat

```

4. Run worker process.

```celery -A celery_periodic_tasks worker```

5. Run Django web server.

```python manage.py runserver```