FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY main.py .
COPY --from=docker:dind /usr/local/bin/docker /usr/local/bin/docker

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0", "main:app" ]
