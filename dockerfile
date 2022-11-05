FROM python:3.8-slim
LABEL org.opencontainers.image.authors="DimCyan"
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN mkdir /ffserver \
    /ffserver/bucket 
WORKDIR /ffserver
ADD . /ffserver/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["python", "-u", "main.py"]