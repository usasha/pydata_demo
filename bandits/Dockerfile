FROM python:3.6.6-jessie

RUN mkdir -p /app/src \
    && chown -R nobody:nogroup /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

VOLUME /app/data
VOLUME /var/run/docker.sock

WORKDIR /app/src
COPY . /app/src/
CMD ["python", "bandits.py"]
