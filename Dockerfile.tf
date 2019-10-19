FROM tensorflow/tensorflow:1.12.0-py3

RUN mkdir /code
RUN mkdir /code/log
WORKDIR /code

RUN pip install -U pip setuptools
ADD requirements.txt .
ADD . /code/
RUN pip install -e . -c requirements-detector.txt

#RUN pip freeze > /work/requirements.txt

# EXPOSE 8080
CMD ["python","mahjong_sample_web_app/detector/detector.py"]
# CMD ["uwsgi","--emperor","/code/uwsgi.ini", "--logto", "/code/log/emperor.log"]
# CMD ["/bin/sh"]