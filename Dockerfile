# start from base
FROM python:3.9

RUN adduser -D worker
USER worker
WORKDIR /usr/src

## copy our application code
COPY src .
COPY requirements.txt .

RUN apt-get update
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Assign execution permissions
RUN chmod +x app.py

CMD [ "python", "./app.py" ]
