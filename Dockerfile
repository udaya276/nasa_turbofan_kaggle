FROM python:3.8.16
WORKDIR /app
COPY . /app
RUN apt update -y && apt install awscli -y

RUN pip install -r requirements.txt
CMD ["python3", "main.py"]


