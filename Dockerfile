# start from base
FROM python:3.9

RUN apt-get update
RUN pip install --upgrade pip

WORKDIR /usr/src

## copy our application code
COPY src .
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Assign execution permissions
RUN chmod +x app.py

RUN adduser  --disabled-login worker
USER worker
CMD [ "python", "./app.py" ]
