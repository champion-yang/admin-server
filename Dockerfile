FROM python:3.6

RUN echo "Asia/Shanghai" > /etc/timezone \
 && rm /etc/localtime && dpkg-reconfigure -f noninteractive tzdata


COPY requirements.txt /app/
RUN pip install --upgrade pip \
 && pip install wheel \
 && pip install -r /app/requirements.txt \
 && rm -rf ~/.cache/pip

COPY . /app/
WORKDIR /app
ENV PYTHONPATH=/app
ENV FLASK_APP=flasky.py


EXPOSE 5004
#ENTRYPOINT []
CMD ["flask","run","-h","0.0.0.0","-p","8000"]