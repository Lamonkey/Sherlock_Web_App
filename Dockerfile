FROM python:3.10.8-bullseye

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["./gunicorn.sh"]