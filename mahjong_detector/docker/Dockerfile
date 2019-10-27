FROM tensorflow/tensorflow:1.12.0-devel-py3
MAINTAINER rio.kurihara

#  install jupyter dependencies
RUN apt-get update && apt-get install -y \
    git \
    less \
    vim \
    man \
    wget \
    cmake \
    byobu \
    tmux \
    htop \
    language-pack-ja \
    unzip \
    cmake \
    libgtk2.0-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    python3-numpy \
    python-tk \
    nscd \
    graphviz \
    python3-pip \
    protobuf-compiler \
    python-pil \
    python-lxml \
    python-tk \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

# locale setting
ENV LANG ja_JP.UTF-8
RUN update-locale LANG=$LANG

# install keras
RUN pip3 install keras==2.2.0
ENV KERAS_BACKEND=tensorflow


# install other packages
RUN pip3 install jupyter
RUN pip3 install https://github.com/ipython-contrib/jupyter_contrib_nbextensions/tarball/master \
    && jupyter contrib nbextension install --user \
    && jupyter nbextension enable collapsible_headings/main

# pycuda taken out due to error(for tensorflow 1.8.0)
RUN pip3 install matplotlib scipy scikit-learn scikit-image seaborn h5py pydot-ng click pillow lxml pulp slackbot mahjong kaggle
RUN pip3 install gensim opencv-python

# install tmux
RUN apt-get install -y tmux
