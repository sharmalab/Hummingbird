FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update           && \
    apt-get -y upgrade          && \
    apt-get -y install 		\
    python3.8 make gcc build-essential libgtk-3-dev \
    python3-pip openjdk-11-jdk-headless default-libmysqlclient-dev libnotify-dev libsdl2-dev \
	automake 		\
	autotools-dev 		\
	g++ 			\
	git 			\
	libcurl4-gnutls-dev wget	\
	libfuse-dev 		\
	libssl-dev 		\
	libxml2-dev 		\
	pkg-config		\
	sysstat			\
	curl

RUN export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
RUN export PATH=$PATH:/home/ubuntu/.local/bin

RUN wget https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04/wxPython-4.1.0-cp38-cp38-linux_x86_64.whl
RUN pip3 install wxPython-4.1.0-cp38-cp38-linux_x86_64.whl

RUN git clone https://github.com/CellProfiler/CellProfiler.git && \
  cd CellProfiler && git checkout v4.2.4 && \
  pip3 install .

WORKDIR /usr/local/src
RUN git clone https://github.com/s3fs-fuse/s3fs-fuse.git
WORKDIR /usr/local/src/s3fs-fuse
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install

# Install AWS CLI, boto3, and pandas

RUN pip3 install awscli boto3 pandas

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN git clone https://github.com/CellProfiler/CellProfiler-plugins.git
WORKDIR /home/ubuntu/CellProfiler-plugins

WORKDIR /hummingbird
COPY server /hummingbird

USER root

RUN useradd hummingbird && chown -R hummingbird /hummingbird

USER hummingbird

CMD ["python", "server.py"]
# CMD ["gunicorn", "--timeout=180", "--workers=20", "--bind=0.0.0.0:8081", "--access-logfile=-", "server:app"]
