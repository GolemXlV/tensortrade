FROM tensorflow/tensorflow:2.1.0-gpu-py3

WORKDIR /

COPY . ./

SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install -yq --assume-yes --no-install-recommends \
  wget \
  zip \
  git \
  ssh \
  python3-pip \
  python3-dev \
  python3-setuptools

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz &&\
  tar xzvf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib && \
  ./configure && \
  make && \
  make install && \
  cd .. && \
  rm -rf ta-lib*

RUN apt-get update -y && \
  apt-get install pandoc -y && \
  apt-get install python3-mpi4py -y && \
  apt-get install libsm6 libxext6 libxrender-dev rsync -y


RUN pip install --upgrade pip
RUN pip install -e .[tf,ccxt,stochastic,docs,tests]
RUN pip install -r ./requirements.txt
RUN pip install -r ./examples/requirements.txt
