FROM python:3.11

WORKDIR /app

COPY requirements.txt /app
COPY .env /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "run.py"]
