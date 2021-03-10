# fr

- [Python3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)

## 使用

```bash
pip install -r requirements.txt

# development or production
export APP_ENV=development

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic

python manage.py createsuperuser

python manage.py runserver
```