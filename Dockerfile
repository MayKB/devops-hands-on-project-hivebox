FROM ubuntu:24.04

WORKDIR /

RUN apt-get update -y \ 
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN apt-get upgrade -y
RUN apt-get install --no-install-recommends -y python=3.12  \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN apt-get install --no-install-recommends -y python3-pip=26

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY script.py .
CMD ["python3", "script.py"]