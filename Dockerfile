FROM ubuntu:24.04
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3.12
RUN apt-get install -y python3-pip

COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages

COPY script.py .
CMD ["python3", "script.py"]