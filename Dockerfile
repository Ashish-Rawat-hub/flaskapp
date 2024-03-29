# syntax=docker/dockerfile:1
  
FROM python:3.9.2

WORKDIR flaskapp

COPY req.txt req.txt

RUN pip3 install -r req.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
