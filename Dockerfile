FROM python:3.7.1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["gunicorn", "-w", "4", "-k", "meinheld.gmeinheld.MeinheldWorker", "-b", ":8888", "main:app"]
