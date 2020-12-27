FROM ubuntu:20.04

LABEL maintainer="Seongcheol Jeon <saelly55@gmail.com>"
LABEL version="1.0"
LABEL title="SRT Translate"
LABEL description="subtitle(.srt) file translation"

ENV DEBIAN_FRONTEND=noninteractive

# add user
RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# libGL error : no matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# file copy
COPY ./test.py /tmp/test.py
COPY ./requirements.txt /tmp/requirements.txt

# install python3, PyQt5
RUN apt-get update && \
    apt-get install -y python3-pyqt5 python3-distutils curl vim && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    rm -f get-pip.py
RUN pip install -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

WORKDIR /home/qtuser

