FROM python:3.11

WORKDIR /app

COPY requirements.txt /app
COPY .env /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python3", "run.py"]
