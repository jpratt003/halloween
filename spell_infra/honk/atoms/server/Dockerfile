FROM python:3.11 as prod

RUN pip install python-socketio eventlet requests

WORKDIR /app

COPY . /app

CMD ["python","-u", "main.py"]
