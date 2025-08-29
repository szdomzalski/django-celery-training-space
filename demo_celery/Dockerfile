FROM python:3.12.3-alpine

WORKDIR /usr/src/app

# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
 # Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app/

RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]