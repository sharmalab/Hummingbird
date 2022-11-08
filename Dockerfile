FROM cellprofiler/cellprofiler:4.0.6

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /hummingbird
COPY server /hummingbird

USER root

RUN useradd hummingbird && chown -R hummingbird /hummingbird

USER hummingbird

CMD ["gunicorn", "--timeout=180", "--workers=20", "--bind=0.0.0.0:8081", "--access-logfile=-", "Server:app"]
