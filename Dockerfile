FROM python:3.7-slim
MAINTAINER "Manabu TERADA" <terada@cmscom.jp>

RUN apt-get update -y
RUN apt-get install -y build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev zlib1g-dev libreadline-gplv2-dev libpq-dev

RUN mkdir /code
RUN mkdir /code/log
WORKDIR /code

RUN pip install -U pip setuptools
ADD requirements.txt .
ADD . /code/
RUN pip install -e . -c requirements.txt

#RUN pip freeze > /work/requirements.txt

EXPOSE 8080
CMD ["uwsgi","--emperor","/code/uwsgi.ini", "--logto", "/code/log/emperor.log"]
# CMD ["/bin/sh"]