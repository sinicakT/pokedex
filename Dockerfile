FROM python:3.12-bullseye

RUN apt-get update -y

# Add requirements
ADD requirements.txt /srv/project/requirements.txt

RUN apt-get update -y && apt-get install -y gettext vim libpq-dev python3-dev

# Install application requirements
RUN pip3 install gunicorn
RUN pip3 install psycopg2
RUN pip3 install setuptools

RUN pip3 install --exists-action=w -r /srv/project/requirements.txt

# Create django user, will own the Django app
RUN adduser --no-create-home --disabled-login --group --system django

RUN mkdir -p /srv/media-files

# Add code
ADD .. /srv/project

WORKDIR /srv/project