FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt
COPY *.py /app/
COPY .env /app/

CMD [ "python", "main.py" ]
