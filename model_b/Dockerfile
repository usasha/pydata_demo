FROM python:3.6.6-jessie

RUN mkdir -p /app/src \
    && chown -R nobody:nogroup /app
VOLUME /app/data

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

USER nobody
WORKDIR /app/src
COPY . /app/src/
EXPOSE 5000
CMD ["python", "var_namer.py"]
