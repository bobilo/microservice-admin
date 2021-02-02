# pull official base image
FROM python:3.6

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update
RUN apt-get -y install postgresql gcc python3-dev musl-dev

# install dependencies
RUN python3 -m pip install --upgrade pip setuptools wheel
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy entry file to project directory
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# copy project
COPY . /app

EXPOSE 8020

# run entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]