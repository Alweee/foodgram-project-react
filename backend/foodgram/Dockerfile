FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

RUN python3 manage.py migrate

RUN python3 manage.py collectstatic --no-input

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
