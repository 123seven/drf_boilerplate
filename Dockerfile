FROM ubuntu:16.04
FROM daocloud.io/python:3.6

# bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# 维护者
MAINTAINER seven <zhuhao@ouchteam.com>

# Time
ENV TZ "Asia/Shanghai"
ENV TERM xtermENV TERM xterm

# Add
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
ADD deploy/sources.list /etc/apt/sources.list

# Packages
RUN apt-get update

# Language
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV TZ=:/etc/localtime

# PIP Mirror
RUN mkdir -p /root/.pip/
ADD deploy/pip.conf /root/.pip/

# PIP Package Prerequisites
RUN apt-get install -y build-essential libmysqlclient-dev libjpeg-dev libpng-dev zlib1g-dev libtiff-dev libtiff5 libfreetype6 \
    libwebp-dev


# project dir
RUN rm -rf /data/ && mkdir -p /data/
WORKDIR /data/

# log dir
RUN mkdir -p /data/code/log/


ADD requirements.txt /data/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uwsgi

ENTRYPOINT ["uwsgi", "--ini", "/data/code/deploy/uwsgi.ini"]