# start from base
FROM python:3.9

WORKDIR /usr/src

# copy our application code
COPY ./requirements.txt .
COPY ./backend.py .
COPY ./templates ./templates

RUN apt-get update
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Assign execution permissions
RUN chmod +x backend.py

CMD [ "python", "./backend.py" ]