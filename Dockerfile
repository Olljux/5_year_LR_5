FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install grpcio grpcio-tools

EXPOSE 50051

CMD ["python", "server.py"]