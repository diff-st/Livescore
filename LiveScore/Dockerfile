FROM python:3.12

WORKDIR /LiveScore
COPY . .
RUN ["pip", "install", "-r", "requirements.txt"]

EXPOSE 8888

CMD ["python", "app.py"]