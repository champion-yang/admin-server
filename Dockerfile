FROM python:3.6

RUN echo "Asia/Shanghai" > /etc/timezone \
 && rm /etc/localtime && dpkg-reconfigure -f noninteractive tzdata


COPY requirements.txt /app/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir --upgrade pip \
 && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir wheel \
 && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r /app/requirements.txt \
 && rm -rf ~/.cache/pip

COPY . /app/
WORKDIR /app
ENV PYTHONPATH=/app
ENV FLASK_APP=flasky.py


EXPOSE 5004
#ENTRYPOINT []
CMD ["flask","run","-h","0.0.0.0","-p","8000"]