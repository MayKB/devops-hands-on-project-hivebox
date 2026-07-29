FROM python@sha256:423ed6ab25b1921a477529254bfeeabf5855151dc2c3141699a1bfc852199fbf

WORKDIR /app

COPY requirements/app-requirements.txt .
RUN pip install --only-binary :all: --require-hashes --no-cache-dir -r app-requirements.txt \
    && addgroup nonrootg \
    && adduser nonrootu \
    && usermod -a -G nonrootg nonrootu
USER nonrootu

COPY script.py .
CMD ["flask", "--app", "script", "run", "--host", "0.0.0.0"]

HEALTHCHECK CMD command